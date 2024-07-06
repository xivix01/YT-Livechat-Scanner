import pytchat, reticker, requests, time, get_video 
import yfinance as yf
from get_video import vid

chat = pytchat.create(vid)
tickerdictionary = {}
dict_sorter = 0

def Scanner(d):
    while chat.is_alive():
        # print(chat.get())
        for c in chat.get().sync_items():
            print(f"{c.datetime} [{c.author.name}]- {c.message}") #print wanted chat data

            # configure Reticker and extractor
            ticker_match_config = reticker.TickerMatchConfig(prefixed_uppercase=True, unprefixed_uppercase=True, prefixed_lowercase=True, prefixed_titlecase=True)
            extractor = reticker.TickerExtractor(deduplicate=False, match_config=ticker_match_config)
            
            # add extracted tickers from messages to a dictionary
            values = extractor.extract(c.message)
            if len(values) > 0:
                for t in values:
                    if t in tickerdictionary:
                        tickerdictionary[t] += 1
                    else:
                        try:
                            # Attempt to fetch information from Yahoo Finance API
                            ticker_info = yf.Ticker(t).info
                            if 'regularMarketPrice' in ticker_info and ticker_info['regularMarketPrice'] is not None:
                                tickerdictionary[t] = 1
                        except requests.exceptions.RequestException as e:
                            print(f"Error fetching data for ticker {t}: {e}")
                
                # sort dictionary
                dict_sorter = sorted(tickerdictionary.items(), key = lambda t:t[1])
                print(dict_sorter)

# return dictionary results
Scanner(dict_sorter)
