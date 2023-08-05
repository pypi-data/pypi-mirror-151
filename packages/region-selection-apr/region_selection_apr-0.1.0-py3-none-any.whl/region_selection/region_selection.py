#!/usr/bin/env python

import os
import sys
import heapq
import click
import timeit
import bisect
import collections
import numpy as np
import pandas as pd
import pyranges as pr
import bottleneck as bn
from io import StringIO
from enum import Enum, EnumMeta, unique

APP_NAME = 'region_selection'

class SelectionMethodMeta(EnumMeta): 
    def __contains__(cls, item): 
        return item in [v.value for v in cls.__members__.values()]
    
@unique
class SelectionMethod(Enum, metaclass=SelectionMethodMeta):
    pq = "pq"
    wis = "wis"
    maxmean = "maxmean"

class SelectionMethodDescription(Enum, metaclass=SelectionMethodMeta):
    pq = "Priority-Queue (PQ)"
    wis = "Weighted Interval Scheduler (WIS)"
    maxmean = "Max-Mean Sweep (MaxMean)"

class Selection:
    def __init__(self, **kwargs):
        self._method = kwargs['method'] if 'method' in kwargs else None
        self._input_fn = kwargs['input_fn'] if 'input_fn' in kwargs else None
        self._bin_size = kwargs['bin_size'] if 'bin_size' in kwargs else None
        self._exclusion_span = kwargs['exclusion_span'] if 'exclusion_span' in kwargs else None
        self._window_span = None

    @classmethod
    def write(self, odf):
        o = StringIO()
        odf.to_csv(o, sep='\t', index=False, header=False)
        sys.stdout.write('{}'.format(o.getvalue()))

    @classmethod
    def run(self, inst, method, idf):
        if not inst._window_span and not inst._method == 'wis':
            inst._window_span = inst._exclusion_span // inst._bin_size
            if inst._method == 'maxmean':
                inst._window_span = inst._window_span // 2
            sys.stderr.write('[{}] Bin size (nt): {}\n'.format(APP_NAME, inst._bin_size))
            sys.stderr.write('[{}] Exclusion span (nt): {}\n'.format(APP_NAME, inst._exclusion_span))
            sys.stderr.write('[{}] Exclusion bins: {}\n'.format(APP_NAME, inst._window_span))
        try:
            sys.stderr.write('[{}] Method: {}\n'.format(APP_NAME, SelectionMethodDescription[method].value))
            start = timeit.default_timer()
            run = getattr(self, method)
            result = run(inst, idf)
            end = timeit.default_timer()
            sys.stderr.write('[{}] Method (runtime in sec): {}\n'.format(APP_NAME, end - start))
            return result
        except TypeError:
            sys.stderr.write('[{}] Something went wrong with method {}\n'.format(APP_NAME, method))
        return None

    @classmethod
    def read(self, inst, method, input_fn):
        df = None
        sys.stderr.write('[{}] Reading input file into dataframe...\n'.format(APP_NAME))
        if method == 'pq' or method == 'maxmean':
            df = pd.read_csv(input_fn, sep='\t', header=None, names=['Chromosome', 'Start', 'End', 'Score'])
        elif method == 'wis':
            df = pr.read_bed(input_fn)
        sys.stderr.write('[{}] Read dataframe\n'.format(APP_NAME))
        return df

    '''
    Assume a genome-wide signal vector S, and a window of size k.

    1. In a continuous sliding window, calculate max() over S within size k
    windows -- make sure the estimator is in the center, i.e. k/2 to the left
    and k/2 to the right. This will result in a step-like signal, indicating
    regions containing high local maxima, i.e. peaks.
    
    2. In the same way, calculate mean() over S within size k windows. This
    constitutes a smooth estimator for regions with generally higher signals
    and will be used to break ties.
    
    3. Order the genome by 1) (primary) and 2) (secondary) -- this way, 2) breaks
    ties in 1), since there will be many of those. Walk through the ordered
    list in a descending manner, and remove elements/windows that overlap
    higher scoring ones.
    '''
    @classmethod
    def maxmean(self, inst, df):
        n = len(df.index)
        r = np.zeros(n, dtype=np.bool_)
        df["IndexOfMaxVal"] = -1
    
        w = df.loc[:, "Score"].to_numpy()

        fws = 2 * inst._window_span
        est_max = bn.move_max(w[inst._window_span-1:], window=fws, min_count=inst._window_span+1)
        est_max = np.append(est_max, np.repeat(np.nan, inst._window_span - 1))
        est_mean = bn.move_mean(w[inst._window_span-1:], window=fws, min_count=inst._window_span+1)
        est_mean = np.append(est_mean, np.repeat(np.nan, inst._window_span - 1))

        df["EstMax"] = est_max
        df["EstMean"] = est_mean
    
        df["OriginalIndex"] = range(n)
        
        df_copy = df.copy()
        
        df.sort_values(["EstMax", "EstMean"], ascending=[False, False], inplace=True)
        
        df = df.reset_index(drop=True)

        '''
        We don't need a heap queue as the sort order is already set.
        We just need to walk through the data frame row by row, test that
        the interval is not excluded (and append it, if so, and exclude
        all intervals over the range). We omit intervals with a zero score,
        and we omit those edge intervals that had a NaN max or mean score.
        '''
        q = []
        for i, v in enumerate(df.index):
            if df.iloc[v]["Score"] == 0 or np.isnan(df.iloc[v]["EstMax"]) or np.isnan(df.iloc[v]["EstMean"]):
                continue
            original_i = df.iloc[v]["OriginalIndex"]
            start_i = (original_i - inst._window_span) if (original_i - inst._window_span) > 0 else 0
            stop_i = (original_i + inst._window_span + 1) if (original_i + inst._window_span + 1) <= n else n
            if not np.any(r[start_i : stop_i]):
                np.put(r, np.arange(start_i, stop_i), True)
                q.append(v)
                vals_over_span = df_copy[start_i : stop_i]["Score"].values
                df.at[i, "IndexOfMaxVal"] = np.argmax(vals_over_span)
        '''
        We drop some extra columns and replace the original scores with the
        maximum score over the window.
        '''
        df = df.iloc[q].sort_values(by=["OriginalIndex"])
        df["Score"] = df["EstMax"]
        df = df.drop(columns=["EstMax", "EstMean", "OriginalIndex", "IndexOfMaxVal"])
        return df
    
    '''
    In this approach, we use a weighted-interval scheduling algorithm to 
    find an optimal packing of non-overlapping/disjoint/"mutually compatible"
    elements, which are sorted lexicographically, i.e. by BEDOPS 'sort-bed' or
    similar.
    
    This uses dynamic programming with optimization from genomic intervals 
    ordered by their stop position. Based on how we are creating our input, 
    we can safely assume the stop position is sorted. If windows are of odd 
    sizes, we may need to add sorting for a general use case down the road.
    
    Iteration is used to walk forwards through an ideal score path, and then 
    backwards from the last interval. The backwards pass draws a list of high-
    scoring intervals, with scores and windows optimally distributed over the 
    input space. Iteration uses significantly less memory than recursion.

    Notes
    -----
    To handle multiple chromosomes, we convert input from a UCSC-like chromosomal
    coordinate system to an "absolute" coordinate system. This lets us order 
    coordinates linearly, from left to right, scanning for optimal weight solutions
    over the whole genome.
    '''
    @classmethod
    def wis(self, inst, df):
        '''
        Use merged intervals to build absolute coordinate space later on.
        '''
        d = df
        m = d.merge()
        df = d.as_df()
        df = df.rename(columns={"Name" : "Score"})
        n = len(df.index)
        '''
        Build accumulated sizes dictionary for calculating absolute coordinates.
        '''
        acc_chr = m.as_df().loc[:, 'Chromosome'].copy().values
        acc_abs = np.concatenate([[0], m.as_df().loc[:, 'End'].copy().values[:-1]])
        j = len(acc_abs) - 1
        while j > 0:
            acc_abs[j] = np.sum(acc_abs[0:j+1])
            j -= 1
        acc = dict(zip(acc_chr, acc_abs))
        '''
        For every interval j, compute the rightmost disjoint interval i, where i < j.
        '''
        s = df.loc[:, 'Start'].copy().values
        e = df.loc[:, 'End'].copy().values
        '''
        We first need to translate the start (s) and end (e) genomic coordinates to
        absolute coordinate space. This lets us search for an optimal path over the 
        whole genome, without having to do complicated things to handle multiple 
        chromosomes.
        '''
        c = df.loc[:, 'Chromosome'].copy().values
        translate_genomic_coords_to_abs = np.vectorize(lambda x, y: y + acc[x])
        s = translate_genomic_coords_to_abs(c, s)
        e = translate_genomic_coords_to_abs(c, e)
        
        '''
        Important! 
        ----------
        Intervals in our df must be sorted by their end coordinates, which we can safely
        assume here, as the input windows are built by stepping across the genome. 
        
        If we are working with other windows that are differently sized or of odd sizes, 
        sorting values by the end value will be required for the DP trace to work correctly.
        '''
        
        '''
        Next, we look for the nearest disjoint interval to the left of the current interval.
        '''
        p = []
        for j in range(n):
            i = bisect.bisect_right(e, s[j]) - 1
            p.append(i)

        '''
        Set up initial opt(imum) table values.
        '''
        opt = collections.defaultdict(int)
        opt[-1] = 0
        opt[0] = 0
        '''
        Forwards pass that puts the best-scoring path into opt.
        '''
        sys.stderr.write('[{}] Constructing forward pass\n'.format(APP_NAME))
        for j in range(1, n):
            score = df.loc[df.index[j], 'Score']
            opt[j] = max(score + opt[p[j]], opt[j - 1])

        '''
        Backwards trace to retrieve path.
        '''
        # given opt and p, find solution intervals in O(n)
        sys.stderr.write('[{}] Constructing qualifying bin list from optimum path\n'.format(APP_NAME))
        q = []
        j = n - 1
        while j >= 0:
            score = df.loc[df.index[j], 'Score']
            if score + opt[p[j]] > opt[j - 1]:
                q.append(j)
                j = p[j] # jump to the nearest disjoint interval to the left
            else:
                j -= 1 # try the "next" interval, one to the left

        '''
        Sort qualifying values so that we can read the dataframe by index.
        '''
        sys.stderr.write('[{}] Returning sorted bin list\n'.format(APP_NAME))
        q.sort()
        return df.iloc[q]        

    '''
    In this approach, we use a priority queue (min-heap) of scores and 
    indices.

    We read score values into the heap, along with an index key. This
    key refers back to an interval.
    
    We start by popping the current highest scoring element off 
    the heap.
    
    We look for overlaps of this candidate element with all other 
    elements in our "qualifying list", using a "rejection vector". 
    
    The rejection vector contains a boolean flag for each interval. 
    We can look upstream and downstream of some index into this vector 
    by N intervals, where N is defined by --window-span.

    In our test case, we have 25kb intervals that step by 1kb increments
    across the genome.
    
    This means that for a given interval, we must look at least 24
    intervals upstream and downstream for any elements that were already
    marked as "qualifying".

    In other words, any values that are "True" indicate that the 
    candidate interval will have an overlap with some element upstream 
    or downstream, which was previously marked as "qualifying". 
    
    In case no such overlap is found (such as the very first pop), we 
    add the candidate element to the qualifying list, then pop another 
    element and repeat the test.

    In case an overlap is found somewhere, we just skip this candidate 
    and pop another element off the heap, repeating the test until the
    heap is exhausted of elements.

    At the end, we return all qualifying elements.
    '''
    @classmethod
    def pq(self, inst, df):
        n = len(df.index)
        r = np.zeros(n, dtype=bool)
        w = df.loc[:, 'Score'].values
        h = []
        '''
        While we want to prioritize higher scores, the built-in Python 
        priority queue uses a min-heap structure, so we need to take the 
        inverse of the score. Popping then gives us the highest scoring 
        element.
        '''
        sys.stderr.write('[{}] Constructing heap\n'.format(APP_NAME))
        for i, v in enumerate(w):
            heapq.heappush(h, (-v, i))
        '''
        Build a qualifying list, until we have as many elements as we want,
        or until we have emptied the heap.
        '''
        sys.stderr.write('[{}] Constructing qualifying bin list from heap\n'.format(APP_NAME))
        q = []
        k = len(df)
        while k > 0:
            try:
                (v, i) = heapq.heappop(h)
                start_i = (i - inst._window_span) if (i - inst._window_span) > 0 else 0
                stop_i = (i + inst._window_span + 1) if (i + inst._window_span + 1) <= n else n
                # sys.stderr.write('k {} | testing key {} | bounds [{}:{}] -> {}'.format(k, i, start_i, stop_i, np.any(r[start_i:stop_i])))
                if not np.any(r[start_i:stop_i]):
                    r[i] = True
                    q.append(i)
                    k -= 1
            except IndexError:
                k = 0
        '''
        Sort indices and return subset of dataframe.
        '''
        sys.stderr.write('[{}] Returning sorted bin list\n'.format(APP_NAME))
        q.sort()
        return df.iloc[q]

    @property
    def window_span(self):
        return self._window_span

    @window_span.setter
    def window_span(self, ws):
        if not ws:
            raise ValueError("[{}] Must specify window span".format(APP_NAME))
        self._window_span = ws
    
    @property
    def exclusion_span(self):
        return self._exclusion_span

    @exclusion_span.setter
    def exclusion_span(self, es):
        if not es or not isinstance(es, int):
            raise ValueError("[{}] Must specify valid exclusion span size (nt): {}".format(APP_NAME, es))
        self._exclusion_span = es

    @property
    def bin_size(self):
        return self._bin_size

    @bin_size.setter
    def bin_size(self, bs):
        if not bs or not isinstance(bs, int):
            raise ValueError("[{}] Must specify valid bin size (nt): {}".format(APP_NAME, bs))
        self._bin_size = bs        

    @property
    def input_fn(self):
        return self._input_fn

    @input_fn.setter
    def input_fn(self, fn):
        if not fn or not os.path.exists(fn):
            raise ValueError("[{}] Must specify valid input filename: {}".format(APP_NAME, fn))
        self._input_fn = fn

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, m):
        if not m in SelectionMethod:
            raise ValueError("[{}] Must specify valid selection method: {}".format(APP_NAME, '|'.join([e.value for e in SelectionMethod])))
        self._method = m

@click.command()
@click.option('--method', type=str, help='selection method (pq|wis|maxmean)', default=None)
@click.option('--input-fn', type=str, help='input filename path', default=None)
@click.option('--bin-size', type=int, help='bin size (nt)', default=200)
@click.option('--exclusion-span', type=int, help='size of exclusion window, upstream and downstream of bin (nt)', default=24800)
def main(*args, **kwargs):
    if not kwargs['method'] or not kwargs['method'] in SelectionMethod:
        raise ValueError("[{}] Must specify valid selection method: --method=[{}]".format(APP_NAME, '|'.join([e.value for e in SelectionMethod])))
    if not kwargs['input_fn']:
        raise ValueError("[{}] Must specify valid input file: --input-fn=foo".format(APP_NAME))
    if not os.path.exists(kwargs['input_fn']):
        raise ValueError("[{}] Must specify path to valid input file: --input-fn=foo".format(APP_NAME))
    
    s = Selection()
    s.method = kwargs['method']
    s.input_fn = kwargs['input_fn']
    s.bin_size = kwargs['bin_size']
    s.exclusion_span = kwargs['exclusion_span']

    in_df = s.read(s, s.method, s.input_fn)
    out_df = s.run(s, s.method, in_df)
    print(out_df.head())
    # s.write(out_df)

if __name__ == '__main__':
    main()
