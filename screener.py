import csv

def readfile(filename):
    f = open(filename, 'r')
    reader = csv.reader(f)
    data = list(reader)[1:]

    ticker_dictionary = {}
    for d in data:
        if d[0] not in ticker_dictionary:
            ticker_dictionary[d[0]] = []
        ticker_dictionary[d[0]].append([d[3], d[4], d[5]])
    return ticker_dictionary


def highest_high(d, ticker, start, days):
    if start < days - 1:
        raise IndexError("Highest high start is out of bounds")
    return max([float(x[0]) for x in d[ticker][start + 1 - days:start + 1]])

def lowest_low(d, ticker, start, days):
    if start < days - 1:
        raise IndexError("Lowest low start is out of bounds")
    return min([float(x[1]) for x in d[ticker][start + 1 - days:start + 1]])

def chikou(d, ticker, start, days=25):
    if start > len(d[ticker]) - days:
        raise IndexError("Chikou start is out of bounds")
    return float(d[ticker][start + days][2])

def avg(hh, ll):
    return float((hh + ll) / 2)

def is_signal_one(d, ticker, days=26):
    if len(d[ticker]) != 111:
        return False
    
    mainday = len(d[ticker]) - days - 1

    hh9 = highest_high(d, ticker, mainday, 9)
    ll9 = lowest_low(d, ticker, mainday, 9)
    hh9shift = highest_high(d, ticker, mainday-25, 9)
    ll9shift = lowest_low(d, ticker, mainday-25, 9)

    hh26 = highest_high(d, ticker, mainday, 26)
    ll26 = lowest_low(d, ticker, mainday, 26)
    hh26shift = highest_high(d, ticker, mainday-25, 26)
    ll26shift = lowest_low(d, ticker, mainday-25, 26)

    hh52shift = highest_high(d, ticker, mainday-25, 52)
    ll52shift = lowest_low(d, ticker, mainday-25, 52)

    tenkansen = avg(hh9, ll9)
    tenkansenshift = avg(hh9shift, ll9shift)

    kijunsen = avg(hh26, ll26)
    kijunsenshift = avg(hh26shift, ll26shift)

    chikouspan = chikou(d, ticker, mainday)
    prev_chikouspan = chikou(d, ticker, mainday - 1)

    senkoua = avg(tenkansenshift, kijunsenshift)
    senkoub = avg(hh52shift, ll52shift)

    close = float(d[ticker][mainday][2])
    prev_close = float(d[ticker][mainday - 1][2])
    
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

def is_signal_two(d, ticker, days=0):
    if len(d[ticker]) != 111:
        return False
    
    mainday = len(d[ticker]) - days - 1

    hh9 = highest_high(d, ticker, mainday, 9)
    ll9 = lowest_low(d, ticker, mainday, 9)
    hh9shift = highest_high(d, ticker, mainday-25, 9)
    ll9shift = lowest_low(d, ticker, mainday-25, 9)
    hh9prev = highest_high(d, ticker, mainday-1, 9)
    ll9prev = lowest_low(d, ticker, mainday-1, 9)

    hh26 = highest_high(d, ticker, mainday, 26)
    ll26 = lowest_low(d, ticker, mainday, 26)
    hh26shift = highest_high(d, ticker, mainday-25, 26)
    ll26shift = lowest_low(d, ticker, mainday-25, 26)
    hh26prev = highest_high(d, ticker, mainday-1, 26)
    ll26prev = lowest_low(d, ticker, mainday-1, 26)

    hh52shift = highest_high(d, ticker, mainday-25, 52)
    ll52shift = lowest_low(d, ticker, mainday-25, 52)

    tenkansen = avg(hh9, ll9)
    tenkansenshift = avg(hh9shift, ll9shift)
    prev_tenkansen = avg(hh9prev, ll9prev)

    kijunsen = avg(hh26, ll26)
    kijunsenshift = avg(hh26shift, ll26shift)
    prev_kijunsen = avg(hh26prev, ll26prev)

    senkoua = avg(tenkansenshift, kijunsenshift)
    senkoub = avg(hh52shift, ll52shift)
    
    close = float(d[ticker][mainday][2])
    prev_close = float(d[ticker][mainday - 1][2])
    
    if (kijunsen > senkoua and
        kijunsen > senkoub and
        tenkansen >= kijunsen and
        prev_tenkansen < prev_kijunsen):
        return True
    if (kijunsen < senkoua and
        kijunsen < senkoub and
        tenkansen <= kijunsen and
        prev_tenkansen > prev_kijunsen):
        return True
    return False
        
def get_signal_one(d):
    valid_tickers = []
    for ticker in d:
        if is_signal_one(d, ticker):
            valid_tickers.append(ticker)
    return valid_tickers

def get_signal_two(d):
    valid_tickers = []
    for ticker in d:
        if is_signal_two(d, ticker):
            valid_tickers.append(ticker)
    return valid_tickers

def get_combo(d):
    valid_tickers = []
    sig_one = get_signal_one(d)
    sig_two = get_signal_two(d)

    for ticker in sig_one:
        if (is_signal_two(d, ticker, 0) or 
            is_signal_two(d, ticker, 1) or 
            is_signal_two(d, ticker, 2) or 
            is_signal_two(d, ticker, 3) or 
            is_signal_two(d, ticker, 4)):
            valid_tickers.append(ticker)

    for ticker in sig_two:
        if (is_signal_one(d, ticker, 26) or 
            is_signal_one(d, ticker, 27) or 
            is_signal_one(d, ticker, 28) or 
            is_signal_one(d, ticker, 29) or 
            is_signal_one(d, ticker, 30)):
            valid_tickers.append(ticker)

    return valid_tickers

def filter_price(d, tickers, min):
    valid_tickers = []
    for ticker in tickers:
        price = float(d[ticker][len(d[ticker]) - 1][2])
        if price >= min:
            valid_tickers.append(ticker)
    return valid_tickers

def remove_duplicates(array):
    valid_tickers = []
    for ticker in array:
        if ticker not in valid_tickers:
            valid_tickers.append(ticker)
    return valid_tickers
    
d = readfile("datafortoday.csv")
print("Both signals: " + ', '.join(remove_duplicates(filter_price(d, get_combo(d), 10))) + '\n')
print("Signal One (Chikou): " + ', '.join(filter_price(d, get_signal_one(d), 10)) + '\n')
print("Signal Two (Tenkansen): " + ', '.join(filter_price(d, get_signal_two(d), 10)))