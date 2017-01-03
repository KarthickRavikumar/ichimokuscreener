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
    if start < days - 1:
        raise IndexError("Highest high start is out of bounds")
    return max([float(x[0]) for x in d[ticker][start - days:start + 1]])

def lowest_low(d, ticker, start, days):
    if start < days - 1:
        raise IndexError("Lowest low start is out of bounds")
    return min([float(x[1]) for x in d[ticker][start - days:start + 1]])

def chikou(d, ticker, start, days=26):
    if start > len(d[ticker]) - days:
        raise IndexError("Chikou start is out of bounds")
    return d[ticker][start + days][2]

def avg(hh, ll):
    return (hh + ll) / 2


def is_valid(d, ticker, days=26):

    if len(d[ticker]) != 84:
        return False
    
    mainday = len(d[ticker]) - days - 1
    
    hh9 = highest_high(d, ticker, mainday, 9)
    ll9 = lowest_low(d, ticker, mainday, 9)
    hh26 = highest_high(d, ticker, mainday, 26)
    ll26 = lowest_low(d, ticker, mainday, 26)
    hh52 = highest_high(d, ticker, mainday, 52)
    ll52 = lowest_low(d, ticker, mainday, 52)
    tenkansen = avg(hh9, ll9)
    kijunsen = avg(hh26, ll26)
    chikouspan = chikou(d, ticker, mainday)
    prev_chikouspan = chikou(d, ticker, mainday - 1)
    senkoua = avg(tenkansen, kijunsen)
    senkoub = avg(hh52, ll52)


    '''
    print hh9
    print ll9
    print hh26
    print ll26
    print hh52
    print ll52
    print tenkansen
    print kijunsen
    print chikouspan
    print senkoua
    print senkoub
    '''

    close = d[ticker][mainday][2]
    prev_close = d[ticker][mainday - 1][2]
    
    
    if (close > senkoua and
        close > senkoub and
        chikouspan >= close and
        prev_chikouspan < prev_close):
        return True

    if (close < senkoua and
        close < senkoub and
        chikouspan <= close and
        prev_chikouspan > prev_close):
        return True

    return False
        
    
        

def get_valid_tickers(d):
    valid_tickers = []
    for ticker in d:
        if is_valid(d, ticker):
            valid_tickers.append(ticker)
    return valid_tickers
            
    



d = readfile("sampledata/WIKI_PRICES_010158fe7c92b40ebea4a642c5d0b158.csv")
print(get_valid_tickers(d))




        
        
    
    
