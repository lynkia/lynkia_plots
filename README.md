# Lynkia plots

This repository contains the scripts that we used to plot graphs. The script will parse the log files of the GRiSP boards and plot graphs with [matplotlib](https://matplotlib.org/).

## Getting started

**Step 1**: Add logs.

Here, the GRiSP boards will use [Logger](https://erlang.org/doc/man/logger.html) to print logs. To print a new line in the log file, you can call the function `info/2` of the module `logger`.

**Example**:

```erlang
logger:info("Hello ~p", ["Joe"]).
```

**Step 2**: Deploy your application on the GRiSP boards.

**Step 3**: Start the experiment.

**Step 4**: Shutdown the GRiSP boards.

**Step 5**: Copy the log files of each GRiSP board to your computer.

**Step 6.a**: Parse the logs.

**Example**:

```Python
from helpers import get_logs_per_node

if __name__ == "__main__":
  directory = "<path of your directory>"
  for (name, logs) in get_logs_per_node(directory):
    print(name)
    print(list(logs))
```

The function `get_logs_per_node` will parse the logs of all files present in the given directory. The `logs` variable will be a generator of tuples. Each tuple will correspond to a line of the log file.

The line:

```
1988-01-01T01:36:41.943690+00:00 info: <text>
```

will be parse in this tuple:

```Python
{
  'time': datetime.datetime(1988, 1, 1, 1, 36, 41, 943690, tzinfo=datetime.timezone.utc),
  'level':  'info',
  'text': '<text>'
}
```

**Step 6.b** (optional): Parse additional data

To add additional data, we decided to encode them in the `text` field. To be correctly parsed, the data will have to be encoded as follow:

```
[<label>]: <key>=<value>;<key>=<value>
```

**Example**:

```Python
from helpers import get_logs_per_node, parse_log

if __name__ == "__main__":
  directory = "<path of your directory>"
  labels = ["MAPREDUCE"]
  for (name, logs) in get_logs_per_node(directory):
    logs = parse_logs(labels, logs)
    print(name)
    print(list(logs))
```

The scripts will add to the dictionary a new entry for each `<key>=<value>` of the field `text`. `<label>` will allow you to differentiate each entry. We could for instance retrieve all logs having the label `MAPREDUCE`.

The line:

```
1988-01-01T01:36:41.943690+00:00 info: [MAPREDUCE]: node=lynkia@my_grisp_board_1;type="leader";round=0
```

will be parsed to:

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

**Step 7**: Load the logs in a dataframe

```Python
df = pandas.DataFrame(logs)
```

## Source

### Python

- [Matplotlib - Broken barh](https://matplotlib.org/3.2.1/gallery/lines_bars_and_markers/broken_barh.html#sphx-glr-gallery-lines-bars-and-markers-broken-barh-py)
