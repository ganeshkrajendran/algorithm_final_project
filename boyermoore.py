# Author: Ganesh Rajendran
# PSU ID: 901595183
# CS-584/684-003: Algorithm Design and Analysis - Spring 2020 - Final project
# Module using BoyerMoore to perform string pattern searching for the given input file and produces time and memory stats.

import tracemalloc
import json
from plotter import plotter
from time import process_time

#
# Pre-processing step to generate bad table char list.
#

def generateBadtable(pat):
    badTable = {}
    for i in range(0, len(pat)-1):
        badTable[pat[i]] = len(pat)-i-1
    return badTable

#
# Pre-processing step: Genearting the good suffix skip list.
#

def findSuffixPos(badchar, suffix, suffix_key):
    for offset in range(1, len(suffix_key)+1)[::-1]:
        flag = True
        for suffix_index in range(0, len(suffix)):
            pos_index = offset-len(suffix)-1+suffix_index
            if pos_index < 0 or suffix[suffix_index] == suffix_key[pos_index]:
                pass
            else:
                flag = False
        pos_index = offset-len(suffix)-1
        if flag and (pos_index <= 0 or suffix_key[pos_index-1] != badchar):
            return len(suffix_key)-offset+1

#
# Generate Good suffix table for comparision
#

def generateSuffixTable(pat):
    goodSkipList = {}
    buffer = ""
    for i in range(0, len(pat)):
        goodSkipList[len(buffer)] = findSuffixPos(pat[len(pat)-1-i], buffer, pat)
        buffer = pat[len(pat)-1-i] + buffer
    return goodSkipList

#
# Boyermoore Algorithm where the input is pattern and txt and return the index of the pattern match.
#
def BMSearch(pattern,txt):
    # Pre-processing step to get the good and bad chars list table.
    goodSuffix = generateSuffixTable(pattern)
    badChar = generateBadtable(pattern)
    tot_index_match_count = 0;
    index = 0
    while index < len(txt)-len(pattern)+1:
        p_len = len(pattern)
        while p_len > 0 and pattern[p_len-1] == txt[index+p_len-1]:
            p_len -= 1
        if p_len > 0:
            badCharShift = badChar.get(txt[index+p_len-1], len(pattern))
            goodSuffixShift = goodSuffix[len(pattern)-p_len]
            if badCharShift > goodSuffixShift:
                index += badCharShift
            else:
                index += goodSuffixShift
            print("Pattern found at index " + str(index))
            tot_index_match_count = tot_index_match_count + 1; 
        else:
            return index
    return -1

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
        BMSearch(pattern, text)
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