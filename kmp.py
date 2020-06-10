# Author: Ganesh Rajendran
# PSU ID: 901595183
# CS-584/684-003: Algorithm Design and Analysis - Spring 2020 - Final project
# Module using Knuth Morris pratt to perform string pattern searching for the given input file and produces time and memory stats.

import tracemalloc
import json
from plotter import plotter
from time import process_time

#
# Pre-processing step to compute longest prefix and suffix.
#
def compute_lps(pattern, p_len):
    len = 0
    l_pre_suf= [0]*p_len
    i = 1

    while i < p_len:
        if pattern[i]== pattern[len]:
            len += 1
            l_pre_suf[i] = len
            i += 1
        else:
            if len != 0:
                len = l_pre_suf[len-1]
            else:
                l_pre_suf[i] = 0
                i += 1
    return l_pre_suf

#
# KMP string algorithm to find string pattern matching and return the index of the match.
#

def kmp_string_search(pattern, act_txt):
    p_len = len(pattern)
    t_len = len(act_txt)
    b_pattern_found = False
    tot_index_match_count = 0;
    j = 0
    lp_suffix = compute_lps(pattern, p_len)
    i = 0
    while i < t_len:
        if pattern[j] == act_txt[i]:
            i += 1
            j += 1
        if j == p_len:
            b_pattern_found = True
            print("Pattern found at index " + str(i-j))
            tot_index_match_count = tot_index_match_count + 1;
            j = lp_suffix[j-1]
        elif i < t_len and pattern[j] != act_txt[i]:
            if j != 0:
                j = lp_suffix[j-1]
            else:
                i += 1

    if not b_pattern_found:
        print("The Pattern {} not found in the given text {}".format(pattern,act_txt))
    
    print("Total matched index --> "+ str(tot_index_match_count))

#
# readfile method reads the given file and return the data in json format which expects the filename contains json data.
#

def readfile(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

#
# Block take care of looping the given data and print out memory usage and time taken.
# Plotting the graph by time and size.
#

if __name__ == "__main__":
    # change input file as required.
    data_dict = readfile("string_pattern_match2.json")
    p = plotter();
    tracemalloc.start()
    for data in data_dict:
        t1_start = process_time()
        text = data["text"]
        pattern = data["pattern"]
        p.add_pattern(pattern)
        p.add_txt(text)
        print("Text size {}, Pattern size {}".format(len(text), len(pattern)))
        kmp_string_search(pattern, text)
        current, peak = tracemalloc.get_traced_memory()
        p.add_usage(current / 10**6)
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        t1_stop = process_time()
        time = t1_stop-t1_start
        print(f"Time taken to complete {time}ms")
        p.add_time(time)
    tracemalloc.stop()
    # - Comments above block to get pattern time and size graph
    # p.plot_txt_time()
    # p.plot_txt_size()
    # - Comments above block to get pattern time and size graph
    p.plot_pat_time()
    p.plot_pat_size()