import norgatedata
import requests
import talib
import time
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from functools import wraps
from matplotlib.ticker import MaxNLocator, AutoMinorLocator
from matplotlib.dates import MO, AutoDateLocator, WeekdayLocator, MonthLocator
from yahoofinancials import YahooFinancials


# lists of parameters for each of the trend flags calculated in create_fields function
df_ma_list = [10, 20, 30, 50, 200]
df_macd_params = [12, 26, 9]
df_adx_list = [14, 20, 50, 200]
df_ma_cross_list = [[10, 30], [20, 50], [50, 200]]
df_price_cross_list = [20, 50, 200]
df_rsi_list = [14]
df_atr_list = [14]

# list of the individual trend flag lists
trend_flag_list = [df_ma_list, df_macd_params, df_adx_list, df_ma_cross_list, df_price_cross_list, df_rsi_list, df_atr_list]

# list of default trend flags to be used if no alternatives are supplied
default_trend_flags = ['MA_10_30',
                       'MACD_flag',               
                       'PX_MA_20',
                       'MA_20_50',
                       'ADX_20_flag',
                       'PX_MA_50',
                       'MA_50_200',
                       'ADX_50_flag',
                       'PX_MA_200',
                       'ADX_200_flag']


def timethis(func):
    """
    Timing decorator to provide running time of functions in milliseconds

    Parameters
    ----------
    func : Function
        Function to be evaluated

    Returns
    -------
    Time
        Prints the time the function took to run, in milliseconds

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {} milliseconds'.format(func.__module__, func.__name__, (end - start)*1e3))
        return r
    return wrapper


class DataProcess():
    """
    Container for various data processing operations
    """
    def __init__(self, *args, **kwargs):
        pass

    
    @timethis
    def create_fields(self, ticker_dict, ma_list, macd_params, adx_list, ma_cross_list, price_cross_list, rsi_list, atr_list):
        """
        Create and add various trend indicators to each DataFrame in the dictionary of tickers 
        
        Parameters
        ----------
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each ticker.

        Returns
        -------
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each ticker.

        """
        if ticker_dict is None:
            ticker_dict = self.ticker_dict
        
        # Loop through each ticker in ticker_dict
        for ticker, df in ticker_dict.items():
            # Create moving averages of 10, 20, 30, 50 and 200 day timeframes
            for tenor in ma_list:
                df['MA_'+str(tenor)] = df['Close'].rolling(window=str(tenor)+'D').mean()
            
            
            # Create MACD, Signal and Hist using default parameters of 12, 26, 9
            df['MACD'], df['MACD_SIGNAL'], df['MACD_HIST'] = talib.MACD(df['Close'], fastperiod=macd_params[0], slowperiod=macd_params[1], signalperiod=macd_params[2])
            # Create flag for MACD histogram increasing 
            df['MACD_flag'] = np.where(df['MACD_HIST'].diff() > 0, 1, 0)
            
            
            # Create ADX of 14, 20, 50 and 200 day timeframes 
            # Create flags for ADX over 25 for 20, 50 and 200 day timeframes
            for tenor in adx_list:
                df['ADX_'+str(tenor)] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=tenor)
                df['ADX_'+str(tenor)+'_flag'] = np.where(df['ADX_'+str(tenor)] > 25, 1, 0)

             
            # Create flag for fast moving average crossing slow moving average
            for tenor_pair in ma_cross_list:
                df['MA_'+str(tenor_pair[0])+'_'+str(tenor_pair[1])] = np.where(df['MA_'+str(tenor_pair[0])] > df['MA_'+str(tenor_pair[1])], 1, 0)
            
            
            # Create flag for price crossing moving average
            for tenor in price_cross_list:
                df['PX_MA_'+str(tenor)] = np.where(df['Close'] > df['MA_'+str(tenor)], 1, 0)


            # Create RSI with 14 day timeframe 
            for tenor in rsi_list:
                df['RSI_'+str(tenor)] = talib.RSI(df['Close'], timeperiod=tenor)
            
            # Create Average True Range with 14 day timeframe
            for tenor in atr_list:
                df['ATR_'+str(tenor)] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=tenor)
            
        
        return ticker_dict


    @timethis
    def create_barometer(self, ticker_dict=None, ticker_name_dict=None, trend_flags=default_trend_flags):
        """
        Create a DataFrame showing the strength of trend for selected markets.

        Parameters
        ----------
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each ticker.
        ticker_name_dict : Dict
            Dictionary mapping ticker to long name for each ticker.
        trend_flags : List
            List of the trend indicators to be used to calculate strength of trend. The default is default_trend_flags.

        Returns
        -------
        frame : DataFrame
            DataFrame of trend strength for each ticker.

        """
        if ticker_dict is None:
            ticker_dict = self.ticker_dict
        if ticker_name_dict is None:
            ticker_name_dict = self.ticker_name_dict
        
        # Create list of tickers from ticker_dict
        ticker_list = [ticker for ticker, df in ticker_dict.items()]
        
        # Convert ticker_name_dict to DataFrame 
        ticker_name_df = pd.DataFrame.from_dict(ticker_name_dict, orient='index', columns=['Long_name']) 
        
        # Create empty DataFrame with Trend Flags as columns and tickers as rows
        frame = pd.DataFrame(columns = trend_flags, index = ticker_list)
        
        # Merge the two DataFrames
        frame = pd.merge(frame, ticker_name_df, left_index=True, right_index=True)
        
        # Reorder columns with list of column names moving the Long Name to the start 
        cols = [frame.columns[-1]] + [col for col in frame if col != frame.columns[-1]]
        frame = frame[cols]
        
        # Loop through each ticker in ticker_dict to populate trend flags in frame
        for ticker, df in ticker_dict.items():
            for flag in trend_flags:
               frame.loc[ticker, flag] = df[flag].iloc[-1]
        
        # Create trend strength column that sums the trend flags and sort by this column       
        frame['Trend Strength'] = frame.iloc[:,1:].sum(axis=1)
        frame = frame.sort_values(by=['Trend Strength'], ascending=False)
        
        # Create short name column, stripping text from longname 
        frame['Short_name'] = frame.loc[:,'Long_name'].str.replace('Continuous Futures Backadjusted','')
        
        self.barometer = frame
        
        return self


    @timethis
    def prepare_chart_data(self, barometer=None, ticker_dict=None, ticker_short_name_dict=None, mkts=5, up='Both'):
        """
        Create a time series of closing prices for selected markets.

        Parameters
        ----------
        barometer : DataFrame
            DataFrame of trend strength for each ticker.
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each ticker.
        ticker_short_name_dict : Dict
            Dictionary mapping ticker to short name for each ticker.
        mkts : Int
            Number of markets to chart. The default is 10.
        up : Str
            True or False flag to select most or least trending markets. The default 
            is 'Both' which displays most and least trending markets.

        Returns
        -------
        chart_data : DataFrame
            DataFrame of closing prices of tickers selected by trend strength.
        data_list : List
            List of markets to be charted.

        """
        if barometer is None:
            barometer = self.barometer   
        if ticker_dict is None:
            ticker_dict = self.ticker_dict
        if ticker_short_name_dict is None:
            ticker_short_name_dict = self.ticker_short_name_dict
        
        # if trend flag is True, select tickers of most trending markets (twice 
        # as many as if selecting both)
        if up == True:
            data_list = list(barometer.index[:(mkts*2)])
        
        # if trend flag is False, select tickers of least trending markets        
        elif up == False:
            data_list = list(barometer.index[-(mkts*2):])
        
        # Otherwise select both
        else:    
            top = list(barometer.index[:mkts])
            bottom = list(barometer.index[-mkts:])
            data_list = top + bottom
        
        # Create a new DataFrame
        chart_data = pd.DataFrame()
        
        # For each ticker in the list of selected tickers, add the column of closing 
        # prices to new DataFrame
        for ticker in data_list:
            chart_data[ticker] = ticker_dict[ticker]['Close']
        
        # Rename columns from tickers to short names and forward fill any NaN cells
        chart_data = chart_data.rename(columns=ticker_short_name_dict)
        chart_data = chart_data.fillna(method='ffill')
                     
        self.chart_data = chart_data 
        self.data_list = data_list
        
        return self


    @timethis
    def norm_hist(self, chart_data=None, days=60):
        """
        Create a subset of chart_prep dataset normalized to start from 100 for the specified history window

        Parameters
        ----------
        chart_data : DataFrame
            DataFrame of closing prices of tickers selected by trend strength.
        days : Int
            Number of days of history. The default is 60.

        Returns
        -------
        tenor : DataFrame
            DataFrame of closing prices, normalized for a given historic window

        """
        if chart_data is None:
            chart_data = self.chart_data
        
        # Copy the selected number of days history from the input DataFrame
        tenor = chart_data[-days:].copy()
        
        # Normalize the closing price of each ticker to start from 100 at the beginning of the history window
        for ticker in tenor.columns:
            tenor[ticker] = tenor[ticker].div(tenor[ticker].iloc[0]).mul(100) 
                
        return tenor    


    @timethis
    def trend_barchart(self, barometer=None, mkts=20, top=True):
        """
        Create a barchart of the most or least trending markets.

        Parameters
        ----------
        barometer : DataFrame
            DataFrame of trend strength for each ticker.
        mkts : Int
            Number of markets to chart. The default is 20.
        top : Bool, optional
            Flag to select markets with highest or lowest trend indication. The default is True.

        Returns
        -------
        fig : Chart
            Returns barchart of most or least trending markets.

        """
        if barometer is None:
            barometer = self.barometer
        
        # Initialize the figure
        fig, ax = plt.subplots()
        
        # Set the xticks to be integer values
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Set the yticks to be horizontal
        plt.yticks(rotation=0)
        
        # If the markets flag is set to False, show the markets with lowest trend indication
        if top == False:
            plt.barh(barometer['Short_name'][-mkts:], barometer['Trend Strength'][-mkts:])
        
        # Otherwise show the markets with greatest trend indication 
        else:
            plt.barh(barometer['Short_name'][:mkts], barometer['Trend Strength'][:mkts])
        
        # Label xaxis
        plt.xlabel("Trend Strength") 
        
        plt.tight_layout()
        plt.show()
        
        
    @timethis
    def return_graph(self, tenor):
        """
        Create a line graph of price history produced by the norm_hist function

        Parameters
        ----------
        tenor : DataFrame
            DataFrame of closing prices, normalized for a given historic window by norm_hist

        Returns
        -------
        fig : Chart
            Line graph of closing prices for each ticker in tenor.

        """
        # Initialize the figure
        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots(figsize=(16,8))
        
        # Plot the lineplot
        ax.plot(tenor)
        
        # axis formatting
        # create a variable to choose interval between xticks based on length of history
        week_scaler = int(round(len(tenor) / 30))
        month_scaler = int(round(len(tenor) / 120))
     
        # Set major xticks as every 4th Monday or monthly at a specified interval
        #major_tick = WeekdayLocator(byweekday=MO, interval = 4)
        scale_week_tick = WeekdayLocator(byweekday=MO, interval=week_scaler)
        scale_month_tick = MonthLocator(interval=month_scaler)
        #auto_date = AutoDateLocator(maxticks=6)
        
        # Set axis format as DD-MMM-YYYY or MMM-YYYY
        daysFmt = mdates.DateFormatter('%d-%b-%Y')
        monthsFmt = mdates.DateFormatter('%b-%Y')
        
        # If less than 90 days history use day format and locate major xticks on 4th Monday
        if len(tenor) < 90:
            ax.xaxis.set_major_formatter(daysFmt)
            ax.xaxis.set_major_locator(scale_week_tick)
            #ax.xaxis.set_major_locator(auto_date)
            #ax.xaxis.set_major_locator(major_tick)
        
        # Otherwise use month format and locate major xticks at monthly (or greater) intervals
        else:
            ax.xaxis.set_major_formatter(monthsFmt)
            ax.xaxis.set_major_locator(scale_month_tick)
        
        # Set minor xticks to be 4 within each major xtick
        minor_tick = AutoMinorLocator(4)
        ax.xaxis.set_minor_locator(minor_tick)
        
        # Set size of ticks
        ax.tick_params(which='both', width=1)
        ax.tick_params(which='major', length=8)
        ax.tick_params(which='minor', length=4)
        
        # Set prices to the right as we are concerned with the current level
        ax.yaxis.set_label_position('right')
        ax.yaxis.tick_right()
        
        # Set x and y labels and title
        xlabel = 'Date'
        ylabel = 'Return'
        title = 'Relative return in last '+str(tenor)+' days'
        ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
        
        # Set the legend 
        ax.legend()
        
        # Set xtick labels at 70 degrees
        plt.xticks(rotation=70)
        
        plt.tight_layout()
        plt.show()    
        
            
    @timethis
    def market_chart(self, ticker_dict=None, ticker_short_name_dict=None, data_list=None, days=60, norm=True):
        """
        Create a chart showing the top and bottom 20 trending markets.

        Parameters
        ----------
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each ticker.
        ticker_short_name_dict : Dict
            Dictionary mapping ticker to short name for each ticker.
        data_list : List
            List of markets to be charted.
        days : Int
            Number of days of history. The default is 60.

        Returns
        -------
        fig : Chart
            Returns chart of multiple markets.

        """
        if ticker_dict is None:
            ticker_dict = self.ticker_dict
        if ticker_short_name_dict is None:
            ticker_short_name_dict = self.ticker_short_name_dict
        if data_list is None:
            data_list = self.data_list    
        
        # Initialize the figure
        fig, ax = plt.subplots(figsize=(16,16))
        plt.tight_layout()
        plt.style.use('seaborn-darkgrid')
    
        # create a color palette
        palette = plt.get_cmap('tab20')
    
        # multiple line plot
        num=0
        for ticker in data_list:
            num += 1
            if num < 21:
                colr = num
            else:
                colr = num - 20
    
            label = ticker_short_name_dict[ticker]
    
            # Find the right spot on the plot
            ax = plt.subplot(8,5, num)
    
            # Plot the lineplot
            if norm == True:
                ax.plot(ticker_dict[ticker].index[-days:], 
                         ticker_dict[ticker]['Close'][-days:].div(ticker_dict[ticker]['Close'][-days:].iloc[0]).mul(100), 
                         marker='', 
                         color=palette(colr), 
                         linewidth=1.9, 
                         alpha=0.9, 
                         label=label)
            else:
                ax.plot(ticker_dict[ticker].index[-days:], 
                         ticker_dict[ticker]['Close'][-days:], 
                         marker='', 
                         color=palette(colr), 
                         linewidth=1.9, 
                         alpha=0.9, 
                         label=label)    
    
            # xticks only on bottom graphs
            if num in range(36) :
                plt.tick_params(labelbottom=False)
    
            # Add title
            plt.title(label, loc='left', fontsize=12, fontweight=0, color='black' )
    
            # axis formatting
            # create a variable to choose interval between xticks based on length of history
            week_scaler = int(round(days / 30))
            month_scaler = int(round(days / 120))
            
            # Set major xticks as every 4th Monday or monthly at a specified interval  
            #major_tick = WeekdayLocator(byweekday=MO, interval = 4)
            scale_week_tick = WeekdayLocator(byweekday=MO, interval=week_scaler)
            scale_month_tick = MonthLocator(interval=month_scaler)
            #auto_date = AutoDateLocator(maxticks=6)
            
            # Set axis format as DD-MMM-YYYY or MMM-YYYY
            daysFmt = mdates.DateFormatter('%d-%b-%Y')
            monthsFmt = mdates.DateFormatter('%b-%Y')

            # If less than 90 days history use day format and locate major xticks on 4th Monday
            if days < 90:
                ax.xaxis.set_major_formatter(daysFmt)
                #ax.xaxis.set_major_locator(auto_date)
                ax.xaxis.set_major_locator(scale_week_tick)
                #ax.xaxis.set_major_locator(major_tick)
                
            # Otherwise use month format and locate major xticks at monthly (or greater) intervals    
            else:
                ax.xaxis.set_major_formatter(monthsFmt)
                ax.xaxis.set_major_locator(scale_month_tick)

            # Set minor xticks to be 4 within each major xtick
            minor_tick = AutoMinorLocator(4)
            ax.xaxis.set_minor_locator(minor_tick)
            
            # Set size of ticks
            ax.tick_params(which='both', width=1)
            ax.tick_params(which='major', length=8)
            ax.tick_params(which='minor', length=4)
                        
            # Set prices to the right as we are concerned with the current level
            ax.yaxis.set_label_position('right')
            ax.yaxis.tick_right()
            
            # Set xtick labels at 70 degrees
            plt.xticks(rotation=70)
    
        # general title
        plt.suptitle("Top and Bottom Trending Markets", fontsize=13, fontweight=0, color='black', style='italic', y=1.02)
        
        
    @timethis    
    def ticker_extract(self):
        """
        Extract list of S&P 500 Companies from Wikipedia.

        Returns
        -------
        tickers : List 
            List of stock tickers in the form of Reuters RIC codes as strings.
        ticker_name_dict : Dict
            Dictionary mapping ticker to long name for each ticker.

        """
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        r = requests.get(url)
        html_doc = r.text
        spx_list = pd.read_html(html_doc)
        
        # the first table on the page contains the stock data
        spx_table = spx_list[0]
        
        # create a list of the tickers from the 'Symbol' column
        tickers = list(spx_table['Symbol'])
        
        # create a dictionary mapping ticker to Security Name
        ticker_name_dict = dict(zip(spx_table['Symbol'],spx_table['Security']))
        
        return tickers, ticker_name_dict    


    def return_data(self, ticker, start_date, end_date, freq='daily'):
        """
        Create DataFrame of historic prices for specified ticker.

        Parameters
        ----------
        ticker : Int
            Stock to be returned in the form of Reuters RIC code as a string. 
        start_date : Str
            Start Date represented as a string in the format 'YYYY-MM-DD'.
        end_date : Str
            End Date represented as a string in the format 'YYYY-MM-DD'.
        freq : Int
            Frequency of data - set to 'daily'.

        Returns
        -------
        df : DataFrame
            DataFrame of historic prices for given ticker.

        """
        yahoo_financials = YahooFinancials(ticker)
        
        # Extract historic prices
        df = yahoo_financials.get_historical_price_data(start_date, end_date, freq)
        
        # Reformat columns
        df = pd.DataFrame(df[ticker]['prices']).drop(['date'], axis=1) \
                .rename(columns={'formatted_date':'Date',
                                 'open': 'Open',
                                 'high': 'High',
                                 'low': 'Low',
                                 'close': 'Close',
                                 'volume': 'Volume'}) \
                .loc[:, ['Date','Open','High','Low','Close','Volume']] \
                .set_index('Date')
        
        # Set Index to Datetime
        df.index = pd.to_datetime(df.index)
        
        return df


    @timethis
    def import_data_norgate(self, tickers, lookback):
        """
        Return dictionary of price histories from Norgate Data.

        Parameters
        ----------
        tickers : List
            List of tickers, represented as strings.
        lookback : Int
            Number of days price history to return.

        Returns
        -------
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each ticker.
        ticker_name_dict : Dict
            Dictionary mapping ticker to long name for each ticker.
        ticker_short_name_dict : Dict
            Dictionary mapping ticker to short name for each ticker.

        """
        # Create empty dictionaries
        ticker_dict = {}
        ticker_name_dict = {}
        ticker_short_name_dict = {}
        
        # Loop through list of tickers
        for ticker in tickers:
            # Append 'c_' to each ticker to avoid labels starting with a number and create lowercase value
            tick = "c_"+ticker[1:]
            lowtick = tick.lower()
            
            # Set data format and extract each DataFrame, storing as a key-value pair in ticker_dict 
            timeseriesformat = 'pandas-dataframe'
            ticker_dict[lowtick] = norgatedata.price_timeseries(ticker, limit = lookback, format=timeseriesformat,)
            
            # Extract the security name and store in ticker_name_dict
            ticker_name = norgatedata.security_name(ticker)
            ticker_name_dict[lowtick] = ticker_name
            
            # Truncate the ticker name to improve charting legibility and store in ticker_short_name_dict 
            ticker_short_name_dict[lowtick] = ticker_name.replace('Continuous Futures Backadjusted','')
            
        return ticker_dict, ticker_name_dict, ticker_short_name_dict




class DataSetNorgate(DataProcess):
    def __init__(self, tickers, lookback=500, trend_flags=default_trend_flags, 
                 ma_list=df_ma_list, macd_params=df_macd_params, adx_list=df_adx_list,
                 ma_cross_list=df_ma_cross_list, price_cross_list=df_price_cross_list, 
                 rsi_list=df_rsi_list, atr_list=df_atr_list):
        # Inherit methods from DataProcess class
        super().__init__(self)
        
        # Instantiate input variables
        self.tickers = tickers
        self.lookback = lookback
        self.trend_flags = trend_flags
        self.ma_list = df_ma_list
        self.macd_params = df_macd_params
        self.adx_list = df_adx_list
        self.ma_cross_list = df_ma_cross_list
        self.price_cross_list = df_price_cross_list
        self.rsi_list = df_rsi_list
        self.atr_list = df_atr_list

        
    def prepare_data_norgate(self):
        # Create dictionaries of DataFrames of prices and ticker names
        self.ticker_dict, self.ticker_name_dict, self.ticker_short_name_dict = self.import_data_norgate(self.tickers, self.lookback)
        
        # Add trend fields to each of the DataFrames in ticker_dict
        self.ticker_dict = self.create_fields(self.ticker_dict, self.ma_list, self.macd_params, 
                                                 self.adx_list, self.ma_cross_list, self.price_cross_list, 
                                                 self.rsi_list, self.atr_list)
        
        return self
    
    

class DataSetYahoo(DataProcess):
    def __init__(self, start_date, end_date, trend_flags=default_trend_flags,
                 ma_list=df_ma_list, macd_params=df_macd_params, adx_list=df_adx_list,
                 ma_cross_list=df_ma_cross_list, price_cross_list=df_price_cross_list, 
                 rsi_list=df_rsi_list, atr_list=df_atr_list):
        # Inherit methods from DataProcess class
        super().__init__(self)
        
        # Create list of tickers, dictionary of ticker names from Wikipedia
        self.tickers, self.ticker_name_dict = self.ticker_extract()
        
        # Set short_name_dict = name_dict
        self.ticker_short_name_dict = self.ticker_name_dict
        
        # Instantiate input variables
        self.start_date = start_date
        self.end_date = end_date
        self.trend_flags = trend_flags
        self.ma_list = df_ma_list
        self.macd_params = df_macd_params
        self.adx_list = df_adx_list
        self.ma_cross_list = df_ma_cross_list
        self.price_cross_list = df_price_cross_list
        self.rsi_list = df_rsi_list
        self.atr_list = df_atr_list


    def prepare_data_yahoo(self):
        # Create dictionaries of DataFrames of prices and ticker names
        self.ticker_dict, self.exceptions = self.import_data_yahoo_financials(self.tickers, self.start_date, self.end_date, mkts=None)
        
        # Add trend fields to each of the DataFrames in ticker_dict
        self.ticker_dict = self.create_fields(self.ticker_dict, self.ma_list, self.macd_params, 
                                                 self.adx_list, self.ma_cross_list, self.price_cross_list, 
                                                 self.rsi_list, self.atr_list)
             
        return self


    @timethis                                                          
    def import_data_yahoo_financials(self, tickers, start, end, mkts=None):
        """
        Return dictionary of price histories from Yahoo Finance.

        Parameters
        ----------
        tickers : List
            List of tickers, represented as strings.
        start : Str
            Start Date represented as a string in the format 'YYYY-MM-DD'.
        end : Str
            End Date represented as a string in the format 'YYYY-MM-DD'.
        markets : Int, optional
            Flag to select only the first n markets. The default is None.

        Returns
        -------
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each ticker.
        exceptions : List
            List of tickers that could not be returned.

        """
        # Create empty dictionary and list
        ticker_dict = {}
        exceptions = []
        
        # Loop through the tickers
        for sym in tickers[:mkts]:
            
            # Attempt to return the data for given ticker
            try:
                ticker_dict[sym] = super().return_data(ticker=sym,
                                                       start_date=start,
                                                       end_date=end,
                                                       freq='daily')
            
            # If error, try replacing '.' with '-' in ticker 
            except:
                try:
                    sym = sym.replace('.','-')
                    ticker_dict[sym] = super().return_data(ticker=sym,
                                                       start_date=start,
                                                       end_date=end,
                                                       freq='daily')
                # If error, add to list of exceptions and move to next ticker
                except:                    
                    print("Error with "+sym)
                    exceptions.append(sym)
                    continue
        
        return ticker_dict, exceptions
    
    
    