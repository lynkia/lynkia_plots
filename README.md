# Lynkia plots

## Getting started

To use the scripts, you will have to retrieve the log files of the GRiSP board. These files will be stored on the micro SD card of the board.

Here, the boards will use [Logger](https://erlang.org/doc/man/logger.html) to print logs. The lines will have the following format:

```
1988-01-01T01:36:41.943690+00:00 info: <text>
```

The scripts will parse the lines as follow:

```Python
{
  'time': datetime.datetime(1988, 1, 1, 1, 36, 41, 943690, tzinfo=datetime.timezone.utc),
  'level':  'info',
  'text': '<text>'
}
```

To add additional information, we decided to add the data in the `text` field. To be correctly parsed, the data will have to be encoded that way:

```
[<label>]: <key>=<value>;<key>=<value>
```

The scripts will add to the dictionary a new entry for each `<key>=<value>`. The field `<label>` will be able to distinguish the logs.

Example:

Input:

```
1988-01-01T01:36:41.943690+00:00 info: [MAPREDUCE]: node=lynkia@my_grisp_board_1;type="leader";round=0
```

Output:

```Python
{
  'time': datetime.datetime(1988, 1, 1, 1, 36, 41, 943690, tzinfo=datetime.timezone.utc),
  'level':  'info',
  'text': '[MAPREDUCE]: node=lynkia@my_grisp_board_1;type="leader";round=0',  
  'label': 'MAPREDUCE',
  'node': 'lynkia@my_grisp_board_1',
  'type': 'leader',
  'round': '0'
}
```

## Source

### Python

- [Matplotlib - Broken barh](https://matplotlib.org/3.2.1/gallery/lines_bars_and_markers/broken_barh.html#sphx-glr-gallery-lines-bars-and-markers-broken-barh-py)
