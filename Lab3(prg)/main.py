import math
from tkinter import N

import PySimpleGUI as sg
import sys
import re

INFINITY = float('inf')

def copy_to_final(curr_path, final_path):
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]

def first_min(adj, i):
    min_val = INFINITY
    for k in range(N):
        if adj[i][k] < min_val and i != k:
            min_val = adj[i][k]
    return min_val

def second_min(adj, i):
    first, second = INFINITY, INFINITY
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]
        elif adj[i][j] <= second and adj[i][j] != first:
            second = adj[i][j]
    return second

def tsp_rec(adj, curr_bound, curr_weight, level, curr_path, visited, final_res, final_path):
    if level == N:
        if adj[curr_path[level - 1]][curr_path[0]] != 0:
            curr_res = curr_weight + adj[curr_path[level - 1]][curr_path[0]]
            if curr_res < final_res[0]:
                copy_to_final(curr_path, final_path)
                final_res[0] = curr_res
        return

    for i in range(N):
        if adj[curr_path[level - 1]][i] != 0 and not visited[i]:
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]
            if level == 1:
                curr_bound -= ((first_min(adj, curr_path[level - 1]) + first_min(adj, i)) / 2)
            else:
                curr_bound -= ((second_min(adj, curr_path[level - 1]) + first_min(adj, i)) / 2)
            if curr_bound + curr_weight < final_res[0]:
                curr_path[level] = i
                visited[i] = True
                tsp_rec(adj, curr_bound, curr_weight, level + 1, curr_path, visited, final_res, final_path)
            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True

def tsp(adj):
    curr_bound = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N
    final_res = [INFINITY]
    final_path = [None] * (N + 1)

    for i in range(N):
        curr_bound += (first_min(adj, i) + second_min(adj, i))
    curr_bound = math.ceil(curr_bound / 2)

    visited[0] = True
    curr_path[0] = 0

    tsp_rec(adj, curr_bound, 0, 1, curr_path, visited, final_res, final_path)
    return final_res[0], final_path

if len(sys.argv) == 1:
    event1, values1 = sg.Window('Branch and Bound', [[sg.Text('Choose a file')], [sg.In(), sg.FileBrowse()], [sg.Open(), sg.Cancel()]]).read(close=True)
    fname = values1[0]
else:
    fname = sys.argv[1]

if not fname:
    raise SystemExit("Cancelling: no filename supplied...")