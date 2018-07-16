# gomap

Some utilities for working with gopro data



## `prune.py`

Remove image files that were taken within some threshold distance of each other.

### Usage

Just pass it the directory to be scanned:

```{python}
python prune.py /path/to/image/dir1
```

Default threshold is 2 meters. You can include multiple directories (comma-delimited) and optionally change the threshold.

```{python}
python prune.py /path/to/image/dir1,/path/to/image/dir/2 --thresh 5
```