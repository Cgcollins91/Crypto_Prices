# %%
import pandas as pd
from   datetime import datetime
from   sklearn.model_selection import train_test_split
from   sklearn.linear_model import LinearRegression
from   sklearn.metrics import mean_squared_error
import category_encoders as ce
import matplotlib.pyplot as plt
import seaborn as sns
import sweetviz as sv
import matplotlib.pyplot as plt
from   coinapi import indicators_def, indicators
from   config import api_key
from   coinapi import get_data


# %%
def get_coin_data(symbol = 'ETH/USDT', interval= '5m'):
    base_url            = "https://api.taapi.io/"
    secret              =  api_key
    exchange            = 'binance'
    results             = '1800'
    addResultTimeStamp  =  True

    indicator = indicators[0]
    df_ind    = get_data(indicator, indicators_def, exchange, symbol, interval, results, addResultTimeStamp)

    for indicator in indicators[1:]:
        df_ind = get_data(indicator, indicators_def, exchange, symbol, interval, results, addResultTimeStamp, df_ind)

    return df_ind


def plot_price_vs_indicators(df):
    # Assuming 'df' is your DataFrame containing price and indicator columns
    # Define the indicators you want to plot
    indicators = df.columns

    # Create a new figure with multiple subplots
    fig, axs = plt.subplots(len(indicators), 1, figsize=(10, 6 * len(indicators)))

    # Plot each indicator against the price with a separate y-axis
    for i, indicator in enumerate(indicators):
        axs[i].plot(df.index, df['Average Price'], label='Price', color='blue')
        axs[i].set_ylabel('Price')
        axs[i].tick_params(axis='y', labelcolor='blue')

        ax2 = axs[i].twinx()
        ax2.plot(df.index, df[indicator], label=indicator, color='red')
        ax2.set_ylabel(indicator)
        ax2.tick_params(axis='y', labelcolor='red')

        axs[i].set_title(f'Price vs. {indicator}')
        axs[i].set_xlabel('Timestamp')

        # Combine legends
        lines, labels = axs[i].get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        axs[i].legend(lines + lines2, labels + labels2, loc='best')

    plt.tight_layout()
    plt.show()
    report = sv.analyze(df)

    # Generate the report
    report.show_html('sweetviz_report.html')

def pre_process(df, shift=12):
    df['datetime']  = pd.to_datetime(df['timestamp'], unit='s') 
    df.set_index('datetime', inplace=True)
    drop_cols = [ 'base', 'conversion', 'Typical Price']
    df.drop(columns = drop_cols, inplace=True)

    ohe_cols = ['countdownIndexIsEqualToPreviousElement', 'sellSetup', 'buySetup',
                'sellSetupPerfection', 'buySetupPerfection', 'bearishFlip', 'bullishFlip', 
                'countdownResetForTDST', 'valueAdvice' ]
    encoder      = ce.OneHotEncoder(cols=ohe_cols)
    df           = encoder.fit_transform(df)
    df_shift     = df.shift(12)

    df_shift.dropna(inplace=True)
    y = df_shift['Average Price']
    X = df_shift.drop(columns=['timestamp', 'Average Price'])
    return X, y

def train_and_predict(X, y, symbol):
    X_curr, y_curr   = X.iloc[-1:], y.iloc[-1:]  # Last row only


    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)  # Don't shuffle

    # Initialize and train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)


    # Predict future prices on the test set
    y_pred = model.predict(X_test)

    # Evaluate model performance
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Optionally, you can also print the coefficients to see the impact of each metric/indicator
    print("Coefficients:", model.coef_)


    y_pred_curr         = model.predict(X_curr)
    y_pred_curr, y_curr = str(y_pred_curr), str(y_curr.iloc[0])
    print(f"{symbol} Price predicted in 1 hour: {y_pred_curr}, current price: {y_curr}")


# %%
symbol          = 'BTC/USDT'
df              = get_coin_data(symbol)
X, y            = pre_process(df)

train_and_predict(X, y, symbol)




# %%
