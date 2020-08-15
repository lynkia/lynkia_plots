#!/usr/bin/env python3

import pandas
import matplotlib.pyplot as plt

from datetime import timedelta
from helpers import get_logs_per_node, get_logs, parse_logs

def open_block(blocks, time):
  if blocks and len(blocks[-1]) == 1:
    blocks[-1] = blocks[-1] + (time,)
  blocks.append((time,))

def close_block(blocks, time):
  if blocks and len(blocks[-1]) == 1:
    blocks[-1] = blocks[-1] + (time,)

def transform_block(blocks, offset):
  for k in range(len(blocks)):
    if len(blocks[k]) == 1:
      continue
    (start, end) = blocks[k]
    start = start - offset
    end = end - offset
    yield ((
      (start).total_seconds(),
      (end - start).total_seconds()
    ))

def plot_blocks(ax, index, blocks, color):
  xrange = blocks
  yrange = (((index + 1) * 6) - 2, 4)
  ax.broken_barh(xrange, yrange, facecolors=color)

def plot(df, ax, myself, names, time_offsets):
  """
  df - Dataframe
  ax - Axis
  """

  df = df.sort_values(by="time", ascending=True)
  blocks = {
    "leader": [],
    "observer": []
  }

  for (_id, row) in df.iterrows():
    time = row["time"]
    if row["label"] == "MAPREDUCE":
      if row["type"] == '"leader"':
        close_block(blocks["observer"], time)
        open_block(blocks["leader"], time)
      if row["type"] == '"observer"':
        close_block(blocks["leader"], time)
        open_block(blocks["observer"], time)
    if row["label"] == "STOP-MAPREDUCE":
      close_block(blocks["leader"], time)
      close_block(blocks["observer"], time)

  offset = df.iloc[0]["time"] + time_offsets[myself]
  blocks["leader"] = list(transform_block(blocks["leader"], offset))
  blocks["observer"] = list(transform_block(blocks["observer"], offset))

  index = names.index(myself)
  plot_blocks(ax, index, blocks["leader"], "tab:orange")
  plot_blocks(ax, index, blocks["observer"], "tab:blue")

  x_ticks = range(0, 95, 5)
  y_ticks = range(6, 6 * (len(names) + 1), 6)

  ax.set_xticks(x_ticks)
  ax.set_yticks(y_ticks)
  ax.set_xlabel("seconds since start")
  ax.set_yticklabels(names)
  ax.grid(True)

  # Add annotations:

  # 1. Add round annotations

  for (_id, row) in df.iterrows():
    time = row["time"]
    x = (row["time"] - offset).total_seconds()
    y = y_ticks[index]
    if row["label"] == "MAPREDUCE":
      plot_blocks(ax, index, [(x - 0.25, 0.5)], "black")
      ax.annotate(row["round"], (x + 0.25, y + 2.5))

  # 2. Display kill message

  for (_id, row) in df.iterrows():
    if row["label"] != "STOP-MAPREDUCE":
      continue
    time = row["time"]
    x = (time - offset).total_seconds()
    y = y_ticks[index]
    ax.annotate("kill", (x, y))

def get_labels():
  return ["MAPREDUCE", "STOP-MAPREDUCE"]

def get_dataframe_per_node(directory):
  dfs = {}
  labels = get_labels()
  for (name, logs) in get_logs_per_node(directory):
    logs = parse_logs(labels, logs)
    df = pandas.DataFrame(logs)
    dfs[name] = df
  return dfs

def get_dataframes(path):

  labels = get_labels()
  logs = get_logs(path)
  logs = parse_logs(labels, logs)

  nodes = {}
  for log in logs:
    name = log["node"]
    if name not in nodes:
      nodes[name] = []
    nodes[name].append(log)

  return {k: pandas.DataFrame(v) for k, v in nodes.items()}

if __name__ == "__main__":

  directory = ""
  dfs = get_dataframe_per_node(directory)

  time_offsets = {
    # "node1": timedelta(seconds=-10),
    # "node2": timedelta(seconds=-10),
    # "node3": timedelta(seconds=-10),
    # "node4": timedelta(seconds=-10),
    # "node5": timedelta(seconds=-10)
  }

  for key in dfs.keys():
    if not key in time_offsets:
      time_offsets[key] = timedelta()

  fig = plt.figure(figsize=(10, 6), dpi=80)
  fig.tight_layout()

  grid = (1, 1)
  ax = plt.subplot2grid(grid, (0, 0))

  for (name, df) in dfs.items():
    plot(df, ax, name, list(dfs.keys()), time_offsets)

  plt.show()