# %%
import requests
import pandas as pd
from config import api_key
from datetime import datetime



indicators_def ={
    'avgprice'                  : 'Average Price',
    'beta'                      : 'Beta',
    'cci'                       : 'Commodity Channel Index',
    'cmf'                       : 'Chaikin Money Flow',
    'ichimoku'                  : 'Ichimoku Cloud',
    'macd'                      : 'Moving Average Convergence Divergence',
    'mfi'                       : 'Money Flow Index',
    'rsi'                       : 'Relative Strength Index',
    'mom'                       : 'Momentum',
    'stoch'                     : 'Stochastic',
    'stochrsi'                  : 'Stochastic RSI',
    'dmi'                       : 'Directional Movement Index',
    'adx'                       : 'Average Directional Movement Index',
    'supertrend'                : 'Super Trend',
    'ma'                        : 'Moving Average',
    'sma'                       : 'Simple Moving Average',
    'ema'                       : 'Exponential Moving Average',
    'wma'                       : 'Weighted Moving Average',
    'dema'                      : 'Double Exponential Moving Average',
    'tema'                      : 'Triple Exponential Moving Average',
    'vwap'                      : 'Volume Weighted Average Price',
    'fibonacciretracement'      : 'Fibonacci Retracement',
    'stalledpattern'            : 'Stalled Pattern',
    'tdsequential'              : 'TD Sequential',
    'ultosc'                    : 'Ultimate Oscillator',
    'typprice'                  : 'Typical Price',
    'pivotpoints'               : 'Pivot Points',
    'bbands'                    : 'Bollinger Bands',
    'doji'                      : 'Doji',
    'stddev'                    : 'Standard Deviation',
    'tsf'                       : 'Time Series Forecast',
    'vosc'                      : 'Volume Oscillator',
    'pvi'                       : 'Positive Volume Index',
    'obv'                       : 'On Balance Volume',
    'nvi'                       : 'Negative Volume Index',
    'cmo'                       : 'Chande Momentum Oscillator',
    'roc'                       : 'Rate of Change',
    'pd'                        : 'Price Difference',

}

indicators = ['avgprice', 'beta', 'cci', 'cmf', 'ichimoku', 'macd', 'mfi',
              'rsi', 'mom', 'stoch', 'stochrsi', 'dmi', 'adx', 'supertrend',
              'ma', 'sma', 'ema', 'wma', 'dema', 'tema', 'vwap', 
              'fibonacciretracement', 'stalledpattern', 'tdsequential',
              'ultosc', 'typprice', 'pivotpoints', 'bbands', 'doji',
              'stddev', 'tsf', 'vosc', 'pvi', 'obv', 'nvi', 'cmo', 'roc', 'pd'
]
              
def get_data(indicator, indicators_def, exchange, symbol, interval, results,
              addResultTimeStamp, df_in = None):
    ind_name = indicators_def[indicator]
    base_url            = "https://api.taapi.io/"
    secret              =  api_key
    exchange            = 'binance'
    try:
        url = base_url + indicator 
        
        parameters = {
        'secret'  :           secret,
        'exchange':           exchange,
        'symbol'  :           symbol,
        'interval':           interval,
        'results' :           results,
        'addResultTimestamp': addResultTimeStamp
        }

        response = requests.request("GET", url = url, params = parameters)

        if response.status_code == 200: # Check if the request was successful (status code 200)
            json_data = response.json()
            df = pd.DataFrame(json_data)  # Convert the JSON data to a pandas DataFrame
            df = df.rename(columns = {'value': ind_name}) # Rename value column to indicator name

            if df_in is not None:
                if (df['timestamp'] == df_in['timestamp']).all(): # If all timestaps equal, drop one of them
                    df.drop(columns=['timestamp'], inplace=True)
                    df = pd.concat([df_in, df], axis=1)

            return df

        else:  # If the request was not successful, print an error message
            print("Error:", response.status_code)
            print(response.text)
            return df_in

        
    except:
        print(f'Error: {indicator} {exchange} {symbol} {interval} {results} {addResultTimeStamp}')
        if df_in is not None:
            return df_in
        

# %%
def get_coin_data():
    symbols              = ['BTC/USDT', 'ETH/USDT']
    intervals           = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '12h', '1d', '1w']
    base_url            = "https://api.taapi.io/"
    secret              =  api_key
    exchange            = 'binance'
    results             = '1800'
    addResultTimeStamp  =  True
    for symbol in symbols:
        for interval in intervals:
            indicator = indicators[0]
            df_ind    = get_data(indicator, indicators_def, exchange, symbol, interval, results, addResultTimeStamp)

            for indicator in indicators[1:]:
                df_ind = get_data(indicator, indicators_def, exchange, symbol, interval, results, addResultTimeStamp, df_ind)

            curr_time = datetime.now().strftime("%Y-%m-%d %H-%M")
            f_name    = f'{symbol}_{curr_time}_{interval}.xlsx'
            f_name    = 'data/' + f_name.replace("/", "")
            df_ind.to_excel(f_name)


# %%
get_coin_data()
# %%
