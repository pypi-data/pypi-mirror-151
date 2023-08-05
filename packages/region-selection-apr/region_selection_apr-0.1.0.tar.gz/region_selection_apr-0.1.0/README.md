# region-selection
Methods for filtering for high-scoring genomic intervals

## Usage

### Importing the module and creating a Selection instance

```
>>> from region_selection import Selection
>>> s = Selection()
```

### Specify properties

```
>>> s.method = "pq"
>>> s.input_fn = "/Users/areynolds/Developer/Github/region_selection/tests/windows.fixed.25k.bed"
>>> s.bin_size = 200
>>> s.exclusion_span = 24800
```

The `method` can be one of `pq`, `wis`, or `maxmean`, for selecting from one of priority-queue, weighted interval scheduling, or max-mean window sweep methods, respectively.

The `input_fn` property points to a file on the file system. This is optional, unless using the `read()` method.

The `bin_size` and `exclusion_span` properties are integers. These represent the size of elements, and the distance required between them (exclusing the bin, itself).

The default values are 200 and 24800, respectively. This means bins are 200 nt wide, and we require at least 25000 nt of distance between any filtered bins. 

### Input data

You can read in data from a four-column, tab-delimited text file:

```
>>> in_df = s.read(s, s.method, s.input_fn)
[region_selection] Reading input file into dataframe...
[region_selection] Read dataframe
```

Otherwise, you must provide a Pandas dataframe containing four columns, each labeled: `Chromosome`, `Start`, `End`, and `Score`, respecively.

In the above snippet, the input dataframe is called `in_df`.

### Running the selection method

Use `run()` to run the specified method on the input dataframe `in_df` (or whatever its name is):

```
>>> out_df = s.run(s, s.method, in_df)
[region_selection] Bin size (nt): 200
[region_selection] Exclusion span (nt): 24800
[region_selection] Exclusion bins: 124
[region_selection] Method: Priority-Queue (PQ)
[region_selection] Constructing heap
[region_selection] Constructing qualifying bin list from heap
[region_selection] Returning sorted bin list
[region_selection] Method (runtime in sec): 140.50703937999998
```

The result is stored as a Pandas dataframe. Here it is called `out_df` and you can call all the usual Pandas properties on this:

```
>>> print(out_df.head())
    Chromosome   Start     End  Score
47        chr1    9400   34400   0.41
172       chr1   34400   59400   0.41
304       chr1   60800   85800   0.41
429       chr1   85800  110800   0.41
554       chr1  110800  135800   0.41
```

Or use the `write()` to write to standard output:

```
>>> s.write(out_df)
...
```

Or write with `to_csv()` etc.