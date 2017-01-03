#!/usr/bin/env python

import csv

def readfile(filename):
    f = open(filename, 'r')
    reader = csv.reader(f)
    data = list(reader)[1:]

    ticker_dictionary = {}
    for d in data:
        if d[0] not in ticker_dictionary:
            ticker_dictionary[d[0]] = []

        #high : d[3]
        #low : d[4]
        #close : d[5]
        #ascending dates
        ticker_dictionary[d[0]].append([d[3], d[4], d[5]])

    return ticker_dictionary


def highest_high(d, ticker, start, days):
    return max([x[0] for x in d[ticker][start:start+days]])

def lowest_low(d, ticker, start, days):
    return min([x[1] for x in d[ticker][start:start+days]])

def chikou(d, ticker, start, days=26):
    if start < days:
        raise IndexError("Chikou needs start > days")
    return d[ticker][start - days][2]

def avg(hh, ll):
    return (hh + ll) / 2

def is_valid(d, ticker):
    hh9 = highest_high(d, ticker, )
    ll9 =
    hh26 =
    ll26 =
    hh52 =
    ll52 = 
    tenkansen = 





    




d = readfile("sampledata/WIKI_PRICES_010158fe7c92b40ebea4a642c5d0b158.csv")
print(chikou(d, "A", 27, 26))




        
        
    
    
