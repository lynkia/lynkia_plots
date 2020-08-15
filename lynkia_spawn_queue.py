#!/usr/bin/env python3

import math
import pandas
import matplotlib.pyplot as plt

from helpers import get_logs_per_node, get_logs, parse_logs

def cast_log(logs):
  offset = next(logs)["time"]
  for log in logs:
    if log["time"]:
      try:
        delta = log["time"] - offset
        log["delta_time"] = delta.total_seconds()
        log["running_tasks"] = int(log["running_tasks"])
        log["forwarded_tasks"] = int(log["forwarded_tasks"])
        log["queue"] = int(log["queue"])
        yield log
      except:
        pass

def get_labels():
  return ["SPAWN-QUEUE"]

def get_dataframe_per_node(directory):
  dfs = {}
  labels = get_labels()
  for (name, logs) in get_logs_per_node(directory):
    logs = parse_logs(labels, logs)
    logs = cast_log(logs)
    df = pandas.DataFrame(logs)
    dfs[name] = df
  return dfs

def plot(df, ax, myself):
  df.sort_values(by="time", ascending=True)
  df.plot.line(
    ax=ax,
    x="delta_time",
    y="running_tasks",
    marker="o",
    markersize=2
  )
  df.plot.line(
    ax=ax,
    x="delta_time",
    y="forwarded_tasks",
    marker="o",
    markersize=2
  )
  df.plot.line(
    ax=ax,
    x="delta_time",
    y="queue",
    marker="o",
    markersize=2
  )
  ax.set_xlabel("seconds since start")
  ax.set_ylabel("number of tasks")

if __name__ == '__main__':

  path = ""
  dfs = get_dataframe_per_node(path)

  ncol = 2
  nrow = math.ceil(len(dfs) / ncol)
  grid = (nrow, ncol)

  fig = plt.figure(figsize=(12, 8), dpi=80, facecolor="w", edgecolor="k")
  fig.tight_layout()

  index = 0
  for (name, df) in dfs.items():
    i = index // ncol
    j = index % ncol
    ax = plt.subplot2grid(grid, (i, j))
    ax.title.set_text(name)
    plot(df, ax, name)
    index = index + 1

  plt.show()
