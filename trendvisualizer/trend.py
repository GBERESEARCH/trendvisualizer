import copy
import datetime as dt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import math
import norgatedata
import numpy as np
import pandas as pd
import requests
from technicalmethods.methods import Indicators
import trend_params as tp
import seaborn as sns
import warnings
from matplotlib.ticker import MaxNLocator, AutoMinorLocator, PercentFormatter
from matplotlib.dates import MO, WeekdayLocator, MonthLocator
from operator import itemgetter
from pandas.tseries.offsets import BDay
from yahoofinancials import YahooFinancials


class DataProcess():
    """
    Container for various data processing operations
    """
    def __init__(self, *args, **kwargs):
                
        # Import dictionary of default parameters 
        self.df_dict = tp.trend_params_dict
        
        # Initialize fixed default parameters
        self._init_fixed_params()
        
        # Set empty time window
        self.window = self.df_dict['df_window']
       
    
    def _init_fixed_params(self):
        """
        Initialize fixed default parameters using values from parameters dict
        Returns
        -------
        Various parameters and dictionaries to the object.
        """
        # Parameters to overwrite mpl_style defaults
        self.mpl_line_params = self.df_dict['df_mpl_line_params']
        self.mpl_bar_params = self.df_dict['df_mpl_bar_params']
        self.mpl_chart_params = self.df_dict['df_mpl_chart_params']
        self.mpl_summary_params = self.df_dict['df_mpl_summary_params']
        
        # Default sector mapping info
        self.sector_mappings = self.df_dict['df_sector_mappings']
        self.equity_sectors = self.df_dict['df_equity_sectors']
        self.commodity_sector_levels = self.df_dict['df_commodity_sector_levels']
        self.equity_sector_levels = self.df_dict['df_equity_sector_levels']
        self.ticker_types = self.df_dict['df_ticker_types']
        
    
    def _refresh_params_default(self, **kwargs):
        """
        Set parameters in various functions to the default values.
        Parameters
        ----------
        **kwargs : Various
                   Takes any of the arguments of the various methods 
                   that use it to refresh data.
        Returns
        -------
        Various
            Runs methods to fix input parameters and reset defaults if 
            no data provided
        """
        
        # For all the supplied arguments
        for k, v in kwargs.items():
            
            # If a value for a parameter has not been provided
            if v is None:
                
                # Set it to the default value and assign to the object 
                # and to input dictionary
                v = self.df_dict['df_'+str(k)]
                self.__dict__[k] = v
                kwargs[k] = v 
            
            # If the value has been provided as an input, assign this 
            # to the object
            else:
                self.__dict__[k] = v
                      
        return kwargs    


    def _date_set(self, start_date=None, end_date=None, lookback=None):
        """
        Create start and end dates if not supplied

        Parameters
        ----------
        start_date : Str, optional
            Date to begin backtest. Format is YYYY-MM-DD. The default is 500 
            business days prior (circa 2 years).
        end_date : Str, optional
            Date to end backtest. Format is YYYY-MM-DD. The default is the 
            last business day.
        lookback : Int, optional
            Number of business days to use for the backtest. The default is 500 
            business days (circa 2 years).

        Returns
        -------
        Str
            Assigns start and end dates to the object.

        """
        
        # If end date is not supplied, set to previous working day
        if end_date is None:
            end_date_as_dt = (dt.datetime.today() - BDay(1)).date()
            end_date = str(end_date_as_dt)
        self.end_date = end_date    
        
        # If start date is not supplied, set to today minus lookback period
        if start_date is None:
            start_date_as_dt = (dt.datetime.today() - 
                                pd.Timedelta(days=lookback*(365/250))).date()
            start_date = str(start_date_as_dt)
        self.start_date = start_date

        return self


    def generate_fields(self, ma_list=None, macd_params=None, adx_list=None, 
                        ma_cross_list=None, price_cross_list=None, 
                        rsi_list=None, breakout_list=None, atr_list=None):
        """
        Generate the indicators used to calculate trend strength

        Parameters
        ----------
        ma_list : List, optional
            List of Moving Average periods. The default is 
            [10, 20, 30, 50, 100, 200].
        macd_params : List, optional
            List of MACD parameters. The default is [12, 26, 9].
        adx_list : List, optional
            List of ADX periods. The default is [10, 20, 30, 50, 100, 200].
        ma_cross_list : List, optional
            List of Moving Average Crossover periods. The default is 
            [(10, 30), (20, 50), (50, 200)].
        price_cross_list : List, optional
            List of Moving Average Price Crossover periods. The default is 
            [10, 20, 30, 50, 100, 200].
        rsi_list : List, optional
            List of RSI periods. The default is [10, 20, 30, 50, 100, 200].
        breakout_list : List, optional
            List of breakout periods. The default is 
            [10, 20, 30, 50, 100, 200].
        atr_list : List, optional
            List of ATR periods. The default is [14].

        Returns
        -------
        Dict
            DataFrames of each ticker updated with additional trend indicators.

        """
        # Set the lists of parameters used to calculate the trend indicators
        # either to those supplied or to the default values
        (ma_list, macd_params, adx_list, ma_cross_list, price_cross_list, 
         rsi_list, breakout_list, atr_list) = itemgetter(
             'ma_list', 'macd_params', 'adx_list', 'ma_cross_list', 
             'price_cross_list', 'rsi_list', 'breakout_list',
             'atr_list')(self._refresh_params_default(
                 ma_list=ma_list, macd_params=macd_params, adx_list=adx_list, 
                 ma_cross_list=ma_cross_list, 
                 price_cross_list=price_cross_list, rsi_list=rsi_list, 
                 breakout_list=breakout_list, atr_list=atr_list))
                 
        # Add trend fields to each of the DataFrames in ticker_dict
        self._fields(
            ma_list=ma_list, macd_params=macd_params, adx_list=adx_list, 
            ma_cross_list=ma_cross_list, price_cross_list=price_cross_list, 
            rsi_list=rsi_list, breakout_list=breakout_list, atr_list=atr_list)
    
        return self
           

    def _fields(self, ma_list, macd_params, adx_list, ma_cross_list, 
                price_cross_list, rsi_list, breakout_list, atr_list):
        """
        Create and add various trend indicators to each DataFrame in 
        the dictionary of tickers    

        Parameters
        ----------
        ma_list : List, optional
            List of Moving Average periods. The default is 
            [10, 20, 30, 50, 100, 200].
        macd_params : List, optional
            List of MACD parameters. The default is [12, 26, 9].
        adx_list : List, optional
            List of ADX periods. The default is [10, 20, 30, 50, 100, 200].
        ma_cross_list : List, optional
            List of Moving Average Crossover periods. The default is 
            [(10, 30), (20, 50), (50, 200)].
        price_cross_list : List, optional
            List of Moving Average Price Crossover periods. The default is 
            [10, 20, 30, 50, 100, 200].
        rsi_list : List, optional
            List of RSI periods. The default is [10, 20, 30, 50, 100, 200].
        breakout_list : List, optional
            List of breakout periods. The default is 
            [10, 20, 30, 50, 100, 200].    
        atr_list : List, optional
            List of ATR periods. The default is [14].

        Returns
        -------
        Dict
            DataFrames of each ticker updated with additional trend indicators.

        """
        
        # Initialize dictionary of DataFrames of tickers, taking a copy of the 
        # raw ticker dictionary
        self.ticker_dict = copy.deepcopy(self.raw_ticker_dict)
        
        # Loop through each ticker in ticker_dict
        for ticker, df in self.ticker_dict.items():
            
            # Create moving averages of 10, 20, 30, 50 and 200 day 
            # timeframes
            for tenor in ma_list:
                try:
                    df['MA_'+str(tenor)] = df['Close'].rolling(
                        window=str(tenor)+'D').mean()
                except:
                    print("Error with " + ticker + " MA_"+str(tenor))
            
            # Create flag for price crossing moving average
            for tenor in price_cross_list:
                try:
                    df['PX_MA_'+str(tenor)] = np.where(
                        df['Close'] > df['MA_'+str(tenor)], 1, -1)
                except:
                    print("Error with " + ticker + " PX_MA_"+str(tenor))
            
            # Create MACD, Signal and Hist using default parameters 
            # of 12, 26, 9
            df['MACD'], df['MACD_SIGNAL'], df['MACD_HIST'] = Indicators.MACD(
                close=df['Close'], 
                fast=macd_params[0], 
                slow=macd_params[1], 
                signal=macd_params[2])
            
            
            # Create flag for MACD histogram increasing 
            df['MACD_flag'] = np.where(df['MACD_HIST'].diff() > 0, 1, -1)
            
            
            # Create ADX of 14, 20, 50, 100 and 200 day timeframes 
            # Create flags for ADX over 25
            for tenor in adx_list:
                try:
                    df['ADX_'+str(tenor)] = Indicators.ADX(
                        high=df['High'], low=df['Low'], close=df['Close'], 
                        time_period=tenor)
                    df['ADX_'+str(tenor)+'_flag'] = np.where(
                        df['ADX_'+str(tenor)] > 25, np.where(
                            df['PX_MA_'+str(tenor)] == 1, 1, -1), 0)
                except:
                    print("Error with " + ticker + " ADX_"+str(tenor))
            
             
            # Create flag for fast moving average crossing slow moving 
            # average
            for tenor_pair in ma_cross_list:
                df['MA_'+str(tenor_pair[0])+'_'+str(tenor_pair[1])] = np.where(
                    df['MA_'+str(tenor_pair[0])] > df[
                        'MA_'+str(tenor_pair[1])], 1, -1)


            # Create RSI with 14, 20, 50, 100 and 200 day timeframes 
            # Create flag for RSI over 70 or under 30
            for tenor in rsi_list:
                try:
                    df['RSI_'+str(tenor)] = Indicators.RSI(
                        close=df['Close'], time_period=tenor)
                    df['RSI_'+str(tenor)+'_flag'] = np.where(
                        df['RSI_'+str(tenor)] > 70, 1, np.where(
                            df['RSI_'+str(tenor)] < 30, -1, 0))
                except:
                    print("Error with " + ticker + " RSI_"+str(tenor))
           
            # Create breakout flags with 14, 20, 50, 100 and 200 day timeframes
            for tenor in breakout_list:
                try:
                    df['low_'+str(tenor)], df['high_'+str(tenor)], \
                        df['breakout_'+str(tenor)] = Indicators.breakout(
                            df, time_period=tenor)
                except:
                    print("Error with " + ticker + " breakout_"+str(tenor))
            
            # Create Average True Range with 14 day timeframe
            for tenor in atr_list:
                try:
                    df['ATR_'+str(tenor)] = Indicators.ATR(
                        high=df['High'], low=df['Low'], close=df['Close'], 
                        time_period=tenor)
                except:
                    print("Error with " + ticker + " ATR_"+str(tenor))
        
        return self


    def generate_trend_strength(self, trend_flags=None):     
        """
        Generate data to show the strength of the trend

        Parameters
        ----------
        trend_flags : List, optional
            The list of indicators used to calculate the strength of the trend. 
            The default values are ['PX_MA_10',
                                    'ADX_10_flag',
                                    'RSI_10_flag',
                                    'MA_10_30',
                                    'MACD_flag',           
                                    'PX_MA_20',
                                    'MA_20_50',
                                    'ADX_20_flag',
                                    'RSI_20_flag',
                                    'PX_MA_30',
                                    'ADX_30_flag',
                                    'RSI_30_flag',
                                    'PX_MA_50',
                                    'MA_50_200',
                                    'ADX_50_flag',
                                    'RSI_50_flag',
                                    'PX_MA_100',
                                    'ADX_100_flag',
                                    'RSI_100_flag',
                                    'PX_MA_200',
                                    'ADX_200_flag',
                                    'RSI_200_flag'
                                    ].

        Returns
        -------
        DataFrame
            DataFrame of trend strength for each ticker.

        """
        # Set the list of trend indicators to be used in calculating trend 
        # strength either to that supplied or to the default values
        (trend_flags) = itemgetter(
            'trend_flags')(self._refresh_params_default(
                 trend_flags=trend_flags))
        
        # Create trend strength data
        self._trendstrength(trend_flags=trend_flags)
        
        return self


    def _trendstrength(self, trend_flags=None):
        """
        Create a DataFrame showing the strength of trend for selected 
        markets.

        Parameters
        ----------

        trend_flags : List
            The list of indicators used to calculate the strength of the trend. 
            The default values are ['PX_MA_10',
                                    'ADX_10_flag',
                                    'RSI_10_flag',
                                    'MA_10_30',
                                    'MACD_flag',           
                                    'PX_MA_20',
                                    'MA_20_50',
                                    'ADX_20_flag',
                                    'RSI_20_flag',
                                    'PX_MA_30',
                                    'ADX_30_flag',
                                    'RSI_30_flag',
                                    'PX_MA_50',
                                    'MA_50_200',
                                    'ADX_50_flag',
                                    'RSI_50_flag',
                                    'PX_MA_100',
                                    'ADX_100_flag',
                                    'RSI_100_flag',
                                    'PX_MA_200',
                                    'ADX_200_flag',
                                    'RSI_200_flag'
                                    ].

        Returns
        -------
        frame : DataFrame
            DataFrame of trend strength for each ticker.

        """
        
        # If data is not supplied as an input, take default values
        if trend_flags is None:
            trend_flags = self.trend_flags
        
        # Create list of tickers from ticker_dict
        ticker_list = [ticker for ticker, df in self.ticker_dict.items()]
        
        # Convert ticker_name_dict to DataFrame 
        ticker_name_df = pd.DataFrame.from_dict(
            self.ticker_name_dict, orient='index', columns=['Long_name']) 
        
        # Create empty DataFrame with Trend Flags as columns and 
        # tickers as rows
        frame = pd.DataFrame(columns = trend_flags, index = ticker_list)
        
        # Merge the two DataFrames
        frame = pd.merge(frame, ticker_name_df, left_index=True, 
                         right_index=True)
        
        # Reorder columns with list of column names moving the
        # Long Name to the start 
        cols = [frame.columns[-1]] + [col for col in frame 
                                      if col != frame.columns[-1]]
        frame = frame[cols]
        
        # Loop through each ticker in ticker_dict to populate trend 
        # flags in frame
        for ticker, df in self.ticker_dict.items():
            for flag in trend_flags:
                try:
                    frame.loc[ticker, flag] = df[flag].iloc[-1]
                
                except:
                    print("Error with " + ticker + " " + flag)
                    frame.loc[ticker, flag] = 0
                    
        # Create trend strength column that sums the trend flags and 
        # sort by this column       
        frame['Trend Strength'] = frame.iloc[:,1:].sum(axis=1)
        frame = frame.sort_values(by=['Trend Strength'], ascending=False)
        
        # Create short name column, stripping text from longname
        short_name = np.array(frame['Long_name'], dtype=str)
        long_name = np.array(frame['Long_name'], dtype=str)

        for row in range(0, len(frame['Long_name'])):
            short_name[row] = long_name[row].partition(" Continuous")[0]

        frame['Short_name'] = short_name
        
        # Create trend strength color column and absolute strength column
        def col_color(row):
            row['Absolute Trend Strength'] = np.abs(row['Trend Strength'])
            if np.abs(row['Trend Strength']) < 5:
                row['Trend Color'] = 'red'
            elif np.abs(row['Trend Strength']) < 10:
                row['Trend Color'] = 'orange'
            else:
                row['Trend Color'] = 'green'
            return row
       
        self.barometer = frame.apply(lambda x: col_color(x), axis=1)
        
        # Apply sector mappings
        self._barometer_sectors()
        
        return self
    

    def _barometer_sectors(self):    
        """
        Add sector mappings to the trend barometer table to use in summary 
        graph

        Returns
        -------
        DataFrame
            barometer updated with additional sector columns.

        """
        
        # Calculate the number of trend indicators
        num_flags = len(self.trend_flags)
        
        # Join the baometer table to the sector mappings table
        self.barometer = self.barometer.join(self.sector_mappings_df)
        
        # Calculate Trend Strength as a percentage by dividing by the number 
        # of trend indicators
        self.barometer['Trend Strength %'] = self.barometer[
            'Trend Strength'] / num_flags
        
        # Calculate the absolute value of trend strength as a percentage
        self.barometer['Absolute Trend Strength %'] = abs(
            self.barometer['Trend Strength %'])
        
        # Reset the index and rename column as 'Ticker
        self.barometer = self.barometer.reset_index()
        self.barometer = self.barometer.rename(columns={'index':'Ticker'})
        
        # Add a column as the string 'Trend' to use in swarm plot
        self.barometer['Trend'] = 'Trend'

        return self


    def trendbarchart(self, mkts=None, trend=None):
        """
        Create a barchart of the most or least trending markets.

        Parameters
        ----------
        mkts : Int
            Number of markets to chart. The default is 20.
        trend : Str
            Flag to select most or least trending markets. 
            Select from: 'up' - strongly trending upwards, 
                         'down - strongly trending downwards, 
                         'neutral' - weak trend, 
                         'strong' - up and down trends, 
            The default is 'strong' which displays both up-trending 
            and down-trending markets.

        Returns
        -------
        fig : Chart
            Returns barchart of most or least trending markets.

        """
        
        # If data is not supplied as an input, take default values
        mkts, trend = itemgetter(
            'mkts', 'trend')(self._refresh_params_default(
                 mkts=mkts, trend=trend))

        # Take a copy of the barometer table        
        barometer = copy.deepcopy(self.barometer)

        # Initialize the figure
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(self.mpl_bar_params)
        num_markets = min(mkts, 20)
        fig, ax = plt.subplots(figsize=(8,int(num_markets/2)))
        plt.tight_layout()
       
        # Set the xticks to be integer values
        ax.xaxis.set_major_locator(MaxNLocator(6))#integer=True))
                
        # Set the x axis to be in percentages
        ax.xaxis.set_major_formatter(PercentFormatter(1))
        
        # Set the spacing between y axis and labels
        ax.yaxis.set_tick_params(pad=15)

        # Set axis tick label size
        font_scaler = min(int(0.6*(50-mkts)), 18)
        ax.tick_params(axis='both', which='both', labelsize=font_scaler)
                
        # Set the yticks to be horizontal
        plt.yticks(rotation=0)
        
        # If the trend flag is set to 'up', show the markets with 
        # greatest up trend indication
        if trend == 'up':
            
            # Set the x-axis range
            ax.set_xlim([0,1])
            
            # Sort by Trend Strength
            barometer = barometer.sort_values(
                by=['Trend Strength %'], ascending=True)
            
            plt.barh(barometer['Short_name'][-mkts:], 
                     barometer['Trend Strength %'][-mkts:], 
                     color=list(barometer['Trend Color'][-mkts:]))
            titlestr = 'Up'
            
        # If the trend flag is set to 'down', show the markets with 
        # greatest down trend indication    
        elif trend == 'down':
            
            # Set the x-axis range
            ax.set_xlim([-1,0])
           
            # Sort by Trend Strength
            barometer = barometer.sort_values(
                by=['Trend Strength %'], ascending=False)     
                        
            plt.barh(barometer['Short_name'][-mkts:], 
                     barometer['Trend Strength %'][-mkts:], 
                     color=list(barometer['Trend Color'][-mkts:]))
            titlestr = 'Down'
        
        # If the trend flag is set to 'down', show the markets with 
        # lowest trend indication    
        elif trend == 'neutral':
            
            # Set the x-axis range
            ax.set_xlim([-1,1])
            
            # Sort by Absolute Trend Strength
            barometer = barometer.sort_values(
                by=['Absolute Trend Strength %'], ascending=True)
            
            plt.barh(barometer['Short_name'][:mkts], 
                     barometer['Trend Strength %'][:mkts], 
                     color=list(barometer['Trend Color'][:mkts]),
                     #height=0.5,
                     )
            titlestr = 'Neutral'
        
        # If the trend flag is set to 'strong', show the markets with 
        # greatest trend indication both up and down
        elif trend == 'strong':
            
            # Set the x-axis range
            ax.set_xlim([-1,1])
            
            # Sort by Absolute Trend Strength
            barometer = barometer.sort_values(
                by=['Absolute Trend Strength %'], ascending=True)
            
            plt.barh(barometer['Short_name'][-mkts:], 
                     barometer['Trend Strength %'][-mkts:], 
                     color=list(barometer['Trend Color'][-mkts:]))
            titlestr = 'Strongly'
        
        
        # Label xaxis
        plt.xlabel("Trend Strength", fontsize=font_scaler*1.2, labelpad=10) 
        
        # Set title
        plt.suptitle(titlestr+' Trending Markets', 
                     fontsize=24, 
                     fontweight=0, 
                     color='black', 
                     style='italic', 
                     y=1.04)        
                
        plt.show()
        
        
    def returnsgraph(self, mkts=None, trend=None, days=None):
        """
        Create a line graph of normalised price history

        Parameters
        ----------
        mkts : Int
            Number of markets to chart. The default is 5.
        trend : Str
            Flag to select most or least trending markets. 
            Select from: 'up' - strongly trending upwards, 
                         'down - strongly trending downwards, 
                         'neutral' - weak trend, 
                         'strong' - up and down trends, 
                         'all' - up down and weak trends
            The default is 'strong' which displays both up-trending 
            and down-trending markets.
        days : Int
            Number of days of history. The default is 60.

        Returns
        -------
        fig : Chart
            Line graph of closing prices for each ticker in tenor.

        """
        
        # If data is not supplied as an input, take default values
        mkts, trend, days = itemgetter(
             'mkts', 'trend', 'days')(self._refresh_params_default(
                 mkts=mkts, trend=trend, days=days))
                
        self._normdata(mkts=mkts, trend=trend, days=days)
        
        tenor = self.tenor
        
        # Initialize the figure
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(self.mpl_line_params)
        plt.tight_layout()
        fig, ax = plt.subplots(figsize=(16,8))
        
        # Plot the lineplot
        ax.plot(tenor)
        
        # axis formatting
        # create a variable to choose interval between xticks based on 
        # length of history
        week_scaler = int(round(len(tenor) / 30))
        month_scaler = int(round(len(tenor) / 120))
     
        # Set major xticks as every 4th Monday or monthly at a specified 
        # interval
        scale_week_tick = WeekdayLocator(byweekday=MO, interval=week_scaler)
        scale_month_tick = MonthLocator(interval=month_scaler)
               
        # Set axis format as DD-MMM-YYYY or MMM-YYYY
        daysFmt = mdates.DateFormatter('%d-%b-%Y')
        monthsFmt = mdates.DateFormatter('%b-%Y')
        
        # If less than 90 days history use day format and locate major 
        # xticks on 4th Monday
        if len(tenor) < 90:
            ax.xaxis.set_major_formatter(daysFmt)
            ax.xaxis.set_major_locator(scale_week_tick)
                   
        # Otherwise use month format and locate major xticks at monthly 
        # (or greater) intervals
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
        
        # Set prices to the right as we are concerned with the current 
        # level
        ax.yaxis.set_major_locator(plt.MaxNLocator(11))
        ax.yaxis.set_label_position('right')
        ax.yaxis.tick_right()
        
        # Set ytick labels 
        yticklabels = (
            int(round(tenor.min().min(), -1)),
            100 - int((abs(100 - round(tenor.min().min(), -1))) / 2),
            100, 
            100 + int((abs(100 - round(tenor.max().max(), -1))) / 2),
            int(round(tenor.max().max(), -1)))
        ax.set_yticks(yticklabels)
        
        # Set x axis range
        ax.set_xlim(min(tenor.index), max(tenor.index))
       
        # Shift label to avoid overlapping tick marks
        ax.yaxis.labelpad = 40
        ax.xaxis.labelpad = 20
        
        # Set a horizontal line at 100 
        ax.axhline(y=100, linewidth=1, color='k')
        
        # Set x and y labels and title
        ax.set_xlabel('Date', fontsize=18)
        ax.set_ylabel('Return %', fontsize=18, rotation=0)
        
        # Set the legend
        upper_anchor = 1.15 + mkts/250
        #plt.legend(loc='upper left', labels=tenor.columns)
        plt.legend(bbox_to_anchor=(0.5, upper_anchor), #1.21), #-0.4,1), #1.05, 1), 
                  #title_fontsize=15,
                  #fontsize=10,
                  #title='Asset',
                  #shadow=True,
                  labels=tenor.columns,
                  loc='upper center',
                  #edgecolor='black',
                  #facecolor='white', #(0.8, 0.8, 0.9, 0.5),
                  ncol=4,
                  #frameon=True,
                  #framealpha=1
                  )
        
        
        # Set xtick labels at 0 degrees and fontsize of x and y ticks 
        # to 15
        plt.xticks(rotation=0, fontsize=15)
        plt.yticks(fontsize=15)
        
        # Set title
        dynamic_y = 1.05 + mkts/500
        plt.suptitle('Relative Return Over Last '
                     +str(len(tenor))+' Trading Days', 
                     fontsize=25, 
                     fontweight=0, 
                     color='black', 
                     style='italic', 
                     y=dynamic_y) #1.08) #0.98)        
        
        plt.show()    
        
   
    def marketchart(self, days=None, trend=None, norm=None, 
                    chart_dimensions=None, mkts=None):
        """
        Create a chart showing the top and bottom 20 trending markets.

        Parameters
        ----------
        days : Int
            Number of days of history. The default is 60.
        trend : Str
            Flag to select most or least trending markets. 
            Select from: 'up' - strongly trending upwards, 
                         'down - strongly trending downwards, 
                         'neutral' - weak trend, 
                         'strong' - up and down trends, 
                         'all' - up down and weak trends
            The default is 'strong' which displays both up-trending 
            and down-trending markets.    
        norm : Bool
            Whether to normalize values to start from 100
        chart_dimensions : Tuple
            Number of tickers to chart expressed as a Tuple, n * m. 
            The default is (8, 5).  

        Returns
        -------
        fig : Chart
            Returns chart of multiple markets.

        """
        
        # If data is not supplied as an input, take default values
        days, trend, norm, chart_dimensions = itemgetter(
             'days', 'trend', 'norm', 
             'chart_dimensions')(self._refresh_params_default(
                 days=days, trend=trend, norm=norm, 
                 chart_dimensions=chart_dimensions))

        # If a mkts parameter has been specified then create a tuple of chart 
        # dimensions         
        if mkts is not None:
            chart_dimensions = self._mkt_dims(mkts)
                 
        self.num_charts = int(chart_dimensions[0] * chart_dimensions[1])         
                 
        self._datalist(mkts=None, trend=trend, market_chart=True, 
                       num_charts=self.num_charts)
        ticker_dict = self.ticker_dict
        
        # Set style
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(self.mpl_chart_params)
                
        # create a color palette
        palette = plt.get_cmap('tab20')
        
        # Initialize the figure
        fig, ax = plt.subplots(figsize=(int(chart_dimensions[1]*3),int(chart_dimensions[0]*2)))
        fig.subplots_adjust(top=0.85)
        fig.tight_layout()
               
        # multiple line plot
        num=0
        for ticker in self.data_list:
            num += 1
            if num < 21:
                colr = num
            else:
                colr = num - 20
    
            label = self.ticker_short_name_dict[ticker]
    
            # Find the right spot on the plot
            ax = plt.subplot(chart_dimensions[0], chart_dimensions[1], num)
    
            # Plot the lineplot
            # Pandas error regarding multi indexing requires converting axes to 
            # numpy arrays
            axis_dates = np.array(ticker_dict[ticker].index[-days:])
            if norm: 
                axis_prices = np.array(
                    ticker_dict[ticker]['Close'][-days:]
                    .div(ticker_dict[ticker]['Close'][-days:].iloc[0])
                    .mul(100))
            
            else:
                axis_prices = np.array(ticker_dict[ticker]['Close'][-days:])
                
            ax.plot(axis_dates, 
                    axis_prices, 
                    marker='', 
                    color=palette(colr), 
                    linewidth=1.9, 
                    alpha=0.9, 
                    label=label)
    
            # xticks only on bottom graphs
            if num in range(self.num_charts - chart_dimensions[1] + 1) :
                plt.tick_params(labelbottom=False)
                   
            # Add title
            plt.title(label, 
                      loc='left', 
                      fontsize=10, 
                      fontweight=0, 
                      color='black' )
    
            # axis formatting
            # create a variable to choose interval between xticks based 
            # on length of history
            week_scaler = int(round(days / 30))
            month_scaler = int(round(days / 120))
            
            # Set major xticks as every 4th Monday or monthly at a 
            # specified interval  
            scale_week_tick = WeekdayLocator(byweekday=MO, 
                                             interval=week_scaler)
            scale_month_tick = MonthLocator(interval=month_scaler)
                        
            # Set axis format as DD-MMM-YYYY or MMM-YYYY
            daysFmt = mdates.DateFormatter('%d-%b-%Y')
            monthsFmt = mdates.DateFormatter('%b-%Y')

            # If less than 90 days history use day format and locate 
            # major xticks on 4th Monday
            if days < 90:
                ax.xaxis.set_major_formatter(daysFmt)
                ax.xaxis.set_major_locator(scale_week_tick)
                                
            # Otherwise use month format and locate major xticks at 
            # monthly (or greater) intervals    
            else:
                ax.xaxis.set_major_formatter(monthsFmt)
                ax.xaxis.set_major_locator(scale_month_tick)

            # Set minor xticks to be 4 within each major xtick
            minor_tick = AutoMinorLocator(4)
            ax.xaxis.set_minor_locator(minor_tick)
            
            # Set size of ticks
            ax.tick_params(which='both', width=0.5, labelsize=8)
            ax.tick_params(which='major', length=2)
            ax.tick_params(which='minor', length=1)
                        
            # Set prices to the right as we are concerned with the 
            # current level
            ax.yaxis.set_label_position('right')
            ax.yaxis.tick_right()
            
            # Set xtick labels at 70 degrees
            plt.xticks(rotation=70)
        
        # Update chart title based on whether the data is normalized 
        # and the chosen trend type to display
        if norm:
            if trend == 'up':
                charttitle = ("Up Trending Markets" 
                              +" - Relative Return Over Last "
                              +str(days)+' Trading Days')
            
            if trend == 'down':
                charttitle = ("Down Trending Markets" 
                              +" - Relative Return Over Last "
                              +str(days)+' Trading Days')

            if trend == 'strong':
                charttitle = ("Most Strongly Trending Markets" 
                              +" - Relative Return Over Last "
                              +str(days)+' Trading Days')

            if trend == 'neutral':
                charttitle = ("Neutral Trending Markets" 
                              +" - Relative Return Over Last "
                              +str(days)+' Trading Days')

            if trend == 'all':
                charttitle = ("Most Strongly and Neutral Trending" 
                              +" Markets - Price Over Last "
                              +str(days)+' Trading Days')
                
        else:
            if trend == 'up':
                charttitle = ("Up Trending Markets" 
                              +" - Price Over Last "
                              +str(days)+' Trading Days')
            
            if trend == 'down':
                charttitle = ("Down Trending Markets" 
                              +" - Price Over Last "
                              +str(days)+' Trading Days')

            if trend == 'strong':
                charttitle = ("Most Strongly Trending Markets" 
                              +" - Price Over Last "
                              +str(days)+' Trading Days')

            if trend == 'neutral':
                charttitle = ("Neutral Trending Markets" 
                              +" - Price Over Last "
                              +str(days)+' Trading Days')

            if trend == 'all':
                charttitle = ("Most Strongly and Neutral Trending" 
                              +" Markets - Price Over Last "
                              +str(days)+' Trading Days')            
       
        # general title
        fig.suptitle(charttitle, 
                     fontsize=20, 
                     fontweight=0, 
                     color='black', 
                     style='italic', 
                     y=1.05)
       
    
    @staticmethod
    def _mkt_dims(mkts):
        """
        Create a tuple giving the height and width of the market chart

        Parameters
        ----------
        mkts : Int
            Number of markets to chart.

        Returns
        -------
        chart_dimensions : Tuple
            Tuple of height, width for market chart.

        """
        if mkts < 20:
            if mkts % 5 == 0:
                width = 5
            elif mkts % 4 == 0:
                width = 4
            elif mkts % 3 == 0:
                width = 3
            elif (mkts+1) % 5 == 0:
                width = 5
            elif (mkts+1) % 4 == 0:
                width = 4    
            elif (mkts+1) % 3 == 0:
                width = 3        
            else:
                width = 5
        elif mkts < 40:
            if mkts % 5 == 0:
                width = 5
            elif mkts % 4 == 0:
                width = 4
            elif (mkts+1) % 5 == 0:
                width = 5
            elif (mkts+1) % 4 == 0:
                width = 4    
            else:
                width = 5
        else:
            width = 5
    
        height = math.ceil(mkts/width)                
        chart_dimensions = (height, width)
        
        return chart_dimensions


    def _normdata(self, mkts, trend, days):
        """
        Create a subset of chart_prep dataset normalized to start from 
        100 for the specified history window

        Parameters
        ----------
        mkts : Int
            Number of markets to chart. The default is 5.
        trend : Str
            Flag to select most or least trending markets. 
            Select from: 'up' - strongly trending upwards, 
                         'down - strongly trending downwards, 
                         'neutral' - weak trend, 
                         'strong' - up and down trends, 
                         'all' - up down and weak trends
            The default is 'strong' which displays both up-trending 
            and down-trending markets.
        days : Int
            Number of days of history. The default is 60.

        Returns
        -------
        tenor : DataFrame
            DataFrame of closing prices, normalized for a given historic 
            window

        """
        
        self._chartdata(mkts=mkts, trend=trend)
        
        # Copy the selected number of days history from the input 
        # DataFrame
        tenor = copy.deepcopy(self.chart_data[-days:])
        
        # Normalize the closing price of each ticker to start from 100 
        # at the beginning of the history window
        for ticker in tenor.columns:
            tenor[ticker] = tenor[ticker].div(tenor[ticker].iloc[0]).mul(100) 
        
        self.tenor = tenor
        
        return self    


    def _chartdata(self, mkts, trend):
        """
        Create a time series of closing prices for selected markets.

        Parameters
        ----------
        mkts : Int
            Number of markets to chart. The default is 5.
        trend : Str
            Flag to select most or least trending markets. 
            Select from: 'up' - strongly trending upwards, 
                         'down - strongly trending downwards, 
                         'neutral' - weak trend, 
                         'strong' - up and down trends, 
                         'all' - up down and weak trends
            The default is 'strong' which displays both up-trending 
            and down-trending markets.

        Returns
        -------
        chart_data : DataFrame
            DataFrame of closing prices of tickers selected by trend 
            strength.
        
        """

        self._datalist(mkts=mkts, trend=trend, market_chart=False, 
                       num_charts=None)
        
        # Create a new DataFrame
        chart_data = pd.DataFrame()
        
        # For each ticker in the list of selected tickers, add the 
        # column of closing prices to new DataFrame
        for ticker in self.data_list:
            chart_data[ticker] = self.ticker_dict[ticker]['Close']
        
        # Rename columns from tickers to short names and forward fill 
        # any NaN cells
        chart_data = chart_data.rename(columns=self.ticker_short_name_dict)
        chart_data = chart_data.fillna(method='ffill')
                     
        self.chart_data = chart_data 
                
        return self
    

    def _datalist(self, mkts, trend, market_chart, num_charts):
        """
        Create a list of the most / least trending markets.

        Parameters
        ----------
        mkts : Int
            Number of markets to chart. The default is 5.
        trend : Str
            Flag to select most or least trending markets. 
            Select from: 'up' - strongly trending upwards, 
                         'down - strongly trending downwards, 
                         'neutral' - weak trend, 
                         'strong' - up and down trends, 
                         'all' - up down and weak trends
            The default is 'strong' which displays both up-trending 
            and down-trending markets.
        market_chart : Bool 
            Whether the data is used for the marketchart graph. The 
            default is False    
        num_charts : Int
            The number of sub plots in the market chart. The default is 40. 

        Returns
        -------
        data_list : List
            List of markets to be charted.

        """
        
        # Take data from the trend strength table         
        barometer = self.barometer   
                        
        # if trend flag is 'up', select tickers of most up trending 
        # markets 
        if trend == 'up':
            
            # Sort by Trend Strength
            barometer = barometer.sort_values(
                by=['Trend Strength'], ascending=False)
            
            if market_chart:
                # Select the specified number of highest values
                data_list = list(barometer['Ticker'][:num_charts])
                
            else:                
                # Select the highest values
                data_list = list(barometer['Ticker'][:mkts])
            
        
        # if trend flag is 'down', select tickers of most down trending 
        # markets
        elif trend == 'down':
            
            # Sort by Trend Strength
            barometer = barometer.sort_values(
                by=['Trend Strength'], ascending=False)
            
            if market_chart:
                # Select the specified number of lowest values
                data_list = list(barometer['Ticker'][-num_charts:])
                
            else:    
                # Select the lowest values
                data_list = list(barometer['Ticker'][-mkts:])
        
        
        # if trend flag is 'neutral', select tickers of least trending 
        # markets        
        elif trend == 'neutral':
            
            # Sort by Absolute Trend Strength
            barometer = barometer.sort_values(
                by=['Absolute Trend Strength'], ascending=False)
            
            if market_chart:
                # Select the specified number of lowest values
                data_list = list(barometer['Ticker'][-num_charts:])
            
            else:
                # Select the lowest values
                data_list = list(barometer['Ticker'][-mkts:])
        
        
        # if trend flag is 'strong', select tickers of most down trending 
        # markets
        elif trend == 'strong':
            
            # Sort by Trend Strength
            barometer = barometer.sort_values(
                by=['Trend Strength'], ascending=False)
            
            if market_chart:
                # Select the specified number of highest values
                top = list(barometer['Ticker'][:int(num_charts/2)])
            
                # Select the lowest values
                bottom = list(barometer['Ticker'][
                    -(num_charts-int(num_charts/2)):])
            
            else:
                # Select the highest values
                top = list(barometer['Ticker'][:int(mkts/2)])
            
                # Select the lowest values
                bottom = list(barometer['Ticker'][
                    -(mkts-int(mkts/2)):])
            
            # Combine this data
            data_list = top + bottom
       
        
        # Otherwise select all 3
        else: 
            
            # Sort by Trend Strength
            barometer = barometer.sort_values(
                by=['Trend Strength'], ascending=False)
            
            if market_chart:
                # Select 1/3 of the specified number of highest values
                top = list(barometer['Ticker'][:int(num_charts/3)])
                
                # Select 1/3 of the specified number of lowest values
                bottom = list(barometer['Ticker'][-int(num_charts/3):])
                
                # Sort by Absolute Trend Strength
                barometer = barometer.sort_values(
                    by=['Absolute Trend Strength'], ascending=False)
                
                # Select 1/3 of the specified number of lowest values
                neutral = list(barometer['Ticker'][
                    -(num_charts-2*int(num_charts/3)):])
            
            else:
                # Select the highest values
                top = list(barometer['Ticker'][:int(mkts/3)])
                
                # Select the lowest values
                bottom = list(barometer['Ticker'][-int(mkts/3):])
                
                # Sort by Absolute Trend Strength
                barometer = barometer.sort_values(
                    by=['Absolute Trend Strength'], ascending=False)
                
                # Select the lowest values
                neutral = list(barometer['Ticker'][
                    -(mkts-2*int(mkts/3)):])
            
            # Combine this data
            data_list = top + bottom + neutral
      
        self.data_list = data_list
      
        return self
                    
        
    def summaryplot(self, sector_level=2, absolute=True, chart_type='swarm', 
                    ticker_types=['c', 's'], dodge=False, compact=False, 
                    marker='^', violin=False):
        """
        Plot a summary of the strength of trend across markets        

        Parameters
        ----------
        sector_level : Int, optional
            The level of granularity of the assets. 
            For Commodities the choices are: 
                1:'Asset Class', 
                2:'Broad Sector', 
                3:'Mid Sector', 
                4:'Narrow Sector',
                5:'Underlying'. The default is 2:'Broad Sector'.
            For Equities the choices are:
                1:'Sector', 
                2:'Industry Group', 
                3:'Industry', 
                4:'Sub-Industry', 
                5:'Security'

        absolute : Bool, optional
            Whether to show absolute trend strength (from 0 - 100%) or show 
            positive and negative trends seperately
            
        chart_type : Str, optional
            The type of chart to display. The default is Swarmplot.

        ticker_types : Str or List
            Ticker types to use. Choose from 'c': continuous futures, 
            'r':ratios, 's':spot cash commodities, 'i':indices, 'y':yields.
            The default is ['c', 's']

        Returns
        -------
        Seaborn Swarmplot of the data.

        """
        # Suppress userwarning warnings caused by overlapping data
        warnings.filterwarnings("ignore", category=UserWarning)
        
        # Configure sector name, marker size, trend type and drop rows from
        # barometer DataFrame as appropriate
        sector_name, marker_size, trend_type, \
            chart_barometer, axis_range, plot_height, \
            sector_list = self._summary_config(
                sector_level, absolute, ticker_types, chart_type, dodge)

        # sns.set_style("darkgrid", {"axes.edgecolor": "black"})        
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(self.mpl_summary_params)
                
        if compact:
            plot_height = plot_height / 4
        
        # Create Seaborn swarm plot
        if chart_type == 'swarm':
            fig, ax = plt.subplots(figsize=(8, plot_height))
            ax = sns.swarmplot(data=chart_barometer, 
                               x=trend_type, 
                               y="Trend", 
                               hue=sector_name,
                               hue_order=sector_list,
                               dodge=dodge,
                               palette='cubehelix',
                               marker=marker,
                               s=marker_size
                               )         
            
            ax.set(ylabel="")
            ax.set_xlabel(trend_type, fontsize=12)
            ax.xaxis.set_major_formatter(PercentFormatter(1))
            ax.set_xlim(axis_range)
            ax.tick_params(axis='both', which='major', labelsize=12)
            ax.set_title('Trend Strength by Sector', fontsize=18, y=1)
            ax.legend(bbox_to_anchor= (1.1, 1), 
                      title_fontsize=10,
                      fontsize=8,
                      title='Sector',
                      shadow=True,
                      frameon=True,
                      facecolor='white')

        # Create Seaborn strip plot 
        if chart_type == 'strip':
            fig, ax = plt.subplots(figsize=(8,plot_height))
            if violin:
                ax = sns.violinplot(x=trend_type, 
                                    y=sector_name,
                                    data=self.barometer,
                                    inner='quartile', 
                                    #color=".8",
                                    linewidth=1, 
                                    palette="coolwarm",
                                    scale='count')
            ax = sns.stripplot(x=trend_type, 
                               y=sector_name,
                               data=self.barometer, 
                               dodge=True, 
                               alpha=1, 
                               order=sector_list,
                               marker=marker,
                               palette='viridis',
                               s=marker_size)
            
            ax.set_title('Trend Strength by Sector', fontsize=18, y=1)
            ax.xaxis.set_major_formatter(PercentFormatter(1))
            ax.set_xlim(axis_range)
            ax.tick_params(axis='both', which='major', labelsize=12)
            ax.tick_params(axis='both', which='minor', labelsize=12)
            ax.set(ylabel="")
            ax.set_xlabel(trend_type, fontsize=12)
    
        # Return warnings to default setting
        warnings.filterwarnings("default", category=UserWarning)    
    
            
    def _summary_config(self, sector_level, absolute, data_types, chart_type, 
                        dodge):
        """
        Configure inputs for Trend Summary plots

        Parameters
        ----------
        sector_level : Int, optional
            The level of granularity of the assets. 
            For Commodities the choices are: 
                1:'Asset Class', 
                2:'Broad Sector', 
                3:'Mid Sector', 
                4:'Narrow Sector',
                5:'Underlying'. The default is 2:'Broad Sector'.
            For Equities the choices are:
                1:'Sector', 
                2:'Industry Group', 
                3:'Industry', 
                4:'Sub-Industry', 
                5:'Security'

        absolute : Bool, optional
            Whether to show absolute trend strength (from 0 - 100%) or show 
            positive and negative trends seperately

        data_types : Str or List
            Data types to use. Choose from 'c': continuous futures, 
            'r':ratios, 's':spot cash commodities, 'i':indices, 'y':yields.
            The default is ['c', 's']

        Returns
        -------
        sector_name : Str
            The sector level used to summarize the data.
        marker_size : Int
            The size of the markers in the strip plot.
        trend_type : Str
            Absolute or relavive trend strength.
        chart_barometer : DataFrame
            Data source used to produce charts.

        """
        # Set sector names and marker size when using Norgate futures data
        if self.asset_type == 'CTA':            
            sector_name = self.commodity_sector_levels[sector_level-1]
            marker_size = 10
           
            # 'all' is used to select all of the Norgate data types
            if data_types == 'all':
                chart_barometer = self.barometer
                
            # If the type is a string, remove all the other types    
            elif type(data_types) == str:
                chart_barometer = copy.deepcopy(self.barometer)
                for tick in list(self.ticker_types.values()):
                    if tick[0] != data_types:
                        chart_barometer.drop(
                            index=chart_barometer[
                                chart_barometer['Ticker'].str.contains(
                                    tick)].index, inplace=True)

            # If the result is a list, remove all the types not in the list
            elif type(data_types) == list:
                chart_barometer = copy.deepcopy(self.barometer)
                for tick in list(self.ticker_types.values()):
                    if tick[0] not in data_types:
                        chart_barometer.drop(
                            index=chart_barometer[
                                chart_barometer['Ticker'].str.contains(
                                    tick)].index, inplace=True)
            
            # Print an error message if an incorrect type is supplied            
            else:
                print('Enter a valid ticker type')

            # Set the maximum height of the chart
            #plot_height = max(min(
            #    len(chart_barometer[sector_name].unique())/2, 40), 
            #    len(chart_barometer[sector_name].unique()))
                       
        # Otherwise for Yahoo SPX data    
        else:
            sector_name = self.equity_sector_levels[sector_level-1]        
            marker_size = 10
            chart_barometer = self.barometer
            
            # Set the maximum height of the chart
            #plot_height = max(min(
            #    len(chart_barometer[sector_name].unique())/2, 100), 
            #    len(chart_barometer[sector_name].unique())) 
                            
        # Set label for Absolute trend strength ranging from 0% to 100%
        if absolute:
            trend_type = 'Absolute Trend Strength %'
            axis_range = [-0.1,1]
        
        # Or splitting uptrends and downtrends ranging from -100% to 100%    
        else:
            trend_type = 'Trend Strength %'
            axis_range = [-1,1]
            
        max_bucket = chart_barometer[trend_type].value_counts().max()
        
        trend_sector_group = chart_barometer[[trend_type, sector_name]]
        
        max_bucket_per_sector = trend_sector_group.groupby(
            trend_sector_group.columns.tolist()).size().max()
        
        num_sectors = len(chart_barometer[sector_name].unique())
        
        # Set the maximum height of the chart
        if chart_type == 'strip':    
            plot_height = max_bucket_per_sector * num_sectors / 6     
        else:
            if dodge:
                #plot_height = max((max_bucket / 2), 
                #                  len(chart_barometer[sector_name].unique())/3)
                plot_height = max_bucket_per_sector * num_sectors / 8
            else:
                plot_height = max_bucket / 4
            
        # Rank the sector split by average  of the trend_type        
        sect_data = trend_sector_group.groupby([sector_name]).mean()
        sector_list = list(sect_data.sort_values(
            trend_type, ascending=False).index)
        
        # Sort chart barometer by trend type
        chart_barometer = chart_barometer.sort_values(
            by=[trend_type], ascending=True)    
        
        return sector_name, marker_size, trend_type, chart_barometer, \
            axis_range, plot_height, sector_list
        
        
    def _ticker_clean(self):
        """
        Remove tickers with incomplete history

        Returns
        -------
        Dict
            Deletes DataFrames from raw ticker dict.

        """
        # Create empty list of tickers to be removed
        drop_list = []
        
        # Loop through each DataFrame in raw ticker dict
        for ticker, df in self.raw_ticker_dict.items():
            
            # If the DataFrame has less than 90% full history 
            if len(df) < (self.window * 0.9):
                
                # Add ticker to the drop list
                drop_list.append(ticker) 
        
        # For each ticker in the drop list
        for ticker in drop_list:
            
            # Delete the ticker from the dictionary
            del self.raw_ticker_dict[ticker]
        
        return self        


    def _window_set(self, df, start_date):
        """
        Set the correct length of the selected data

        Parameters
        ----------
        df : DataFrame
            The historical prices.
        start_date : Str
            The chosen start date.

        Returns
        -------
        The window length as an object variable.

        """
        # If the history window has not yet been set 
        if self.window is None:
            
            # If the difference in start dates between the chosen start date
            # and the first value in the index is less than 5 days
            if (pd.to_datetime(start_date) - df.index[0]).days < 5:
                
                # Set the window length to the length of the DataFrame
                self.window = len(df)



class DataSetNorgate(DataProcess):
    
    
    def __init__(self):
        
        # Inherit methods from DataProcess class
        DataProcess.__init__(self)
        
        
    def prepnorgate(self, tickers=None, start_date=None, end_date=None, 
                    ticker_limit=None, lookback=None):
        """
        Create dataframes of prices, extracting data from Norgatedata. 

        Returns
        -------
        Dict, DataFrames
            Dictionary of DataFrames.

        """
        
        # Set the asset type to 'CTA'
        self.asset_type = 'CTA'
        
        # If a list of tickers are not supplied, run the function to collect 
        # available tickers 
        if tickers is None:
            tickers = self._get_norgate_tickers()
        
        # Set values for the number of tickers to return and the number of days 
        # to look back over, either to those supplied or to the default values    
        (ticker_limit, lookback) = itemgetter(
            'ticker_limit', 'lookback')(
                self._refresh_params_default(
                    ticker_limit=ticker_limit, lookback=lookback))  
        
        # Set the start and end dates        
        self._date_set(start_date=start_date, end_date=end_date, 
                       lookback=lookback)        
                
        # Create dictionaries of DataFrames of prices and ticker names
        self._importnorgate(tickers=tickers, start_date=self.start_date,
                            end_date=self.end_date, ticker_limit=ticker_limit)
    
        # Remove tickers with short history    
        self._ticker_clean()
    
        return self
    
    
    def _get_norgate_tickers(self):
        """
        Create list of all available Norgate Commodity tickers

        Returns
        -------
        tickers : List
            Returns a list of ticker codes.

        """
        
        # Specify Norgate Cash Commodities database and extract data
        databasename = 'Cash Commodities'
        databasecontents = norgatedata.database(databasename)
        
        # Create empty dictionary to store tickers
        init_ticker_dict = {}
        
        # For each dictionary in the data extract
        for dicto in databasecontents:
            
            # Add the symbol and security name to the ticker dict as a 
            # key-value pair
            key = dicto['symbol']
            value = dicto['securityname']
            if 'Stocks' not in value:
                init_ticker_dict[key] = value
        
        # Specify Norgate Continuous Futures database and extract data            
        databasename = 'Continuous Futures'
        databasecontents = norgatedata.database(databasename)

        # For each dictionary in the data extract
        for dicto in databasecontents:
            
            # Add the symbol and security name to the ticker dict as a 
            # key-value pair
            key = dicto['symbol']
            value = dicto['securityname']
            
            # Only take the back-adjusted tickers
            if '_CCB' in key:
                init_ticker_dict[key] = value
        
        self.init_ticker_dict = init_ticker_dict
        
        # Convert the ticker dict keys into a list
        tickers = list(init_ticker_dict.keys())
    
        return tickers
    
    
    def _importnorgate(self, tickers, start_date, end_date, ticker_limit):
        """
        Return dictionary of price histories from Norgate Data.

        Parameters
        ----------
        tickers : List
            List of tickers, represented as strings.

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
        self.raw_ticker_dict = {}
        self.ticker_name_dict = {}
        self.ticker_short_name_dict = {}
        
        # Loop through list of tickers
        for ticker in tickers[:ticker_limit]:
            
            # Append character to each ticker to represent its type and create 
            # lowercase value
            tick = self.ticker_types[ticker[0]]+ticker[1:]
            lowtick = tick.lower()
            
            # Set data format and extract each DataFrame, storing as 
            # a key-value pair in ticker_dict 
            timeseriesformat = 'pandas-dataframe'
            try:
                data = norgatedata.price_timeseries(
                    ticker, start_date=start_date, end_date=end_date, 
                    format=timeseriesformat,)
                
                data = data[['Open', 'High', 'Low', 'Close']]
                               
                self.raw_ticker_dict[lowtick] = data
                
                # Extract the security name and store in ticker_name_dict
                ticker_name = norgatedata.security_name(ticker)
                self.ticker_name_dict[lowtick] = ticker_name

                # Set the proper length of DataFrame to help filter out missing 
                # data        
                self._window_set(df=data, start_date=start_date)

            except:
                print('Error importing : ', ticker)
                
            try:    
                # Truncate the ticker name to improve charting legibility 
                # and store in ticker_short_name_dict 
                self.ticker_short_name_dict[lowtick] = ticker_name.partition(
                    " Continuous")[0]

            except:
                self.ticker_short_name_dict[lowtick] = ticker_name

        # Create sector mappings DataFrame
        self._commodity_sector_mappings()
            
        return self


    def _commodity_sector_mappings(self):
        """
        Create sector mappings DataFrame

        Returns
        -------
        DataFrame
            Sector mappings DataFrame stored in the object.

        """
        # Create empty dictionary
        sectors = {}
        
        # For each key-value pair in the default sector mappings dictionary
        for key, value in self.sector_mappings.items():
            
            # If the first character in the key is in the list of keys from the 
            # ticker types dictionary
            if key[0] in list(self.ticker_types.keys()):
                
                # Create a new key equal to the lower case original key with 
                # the first character replaced by the value in the ticker types 
                # dictionary 
                new_key = key.lower().replace(key[0], 
                                              self.ticker_types[key[0]])
                
                # create an entry in the sectors dictionary
                sectors[new_key] = value
        
        # Create a sector mappings DataFrame from the sectors dictionary using 
        # the default commodity sector levels list as the column headers
        self.sector_mappings_df = pd.DataFrame.from_dict(
            sectors, 
            orient='index', 
            columns=self.commodity_sector_levels)
        
        return self
    
    

class DataSetYahoo(DataProcess):
    
    def __init__(self):
        
        # Inherit methods from DataProcess class
        DataProcess.__init__(self)
        
        # Create list of tickers, dictionary of ticker names from 
        # Wikipedia
        self._tickerextract()
        
        # Set short_name_dict = name_dict
        self.ticker_short_name_dict = self.ticker_name_dict
       

    def _tickerextract(self):
        """
        Extract list of S&P 500 Companies from Wikipedia.

        Returns
        -------
        tickers : List 
            List of stock tickers in the form of Reuters RIC codes 
            as strings.
        ticker_name_dict : Dict
            Dictionary mapping ticker to long name for each ticker.

        """
        
        # Extract data from the Wikipedia SPX page
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        r = requests.get(url)
        html_doc = r.text
        spx_list = pd.read_html(html_doc)
        
        # the first table on the page contains the stock data
        spx_table = spx_list[0]
        
        # create a list of the tickers from the 'Symbol' column
        self.tickers = list(spx_table['Symbol'])
        
        # create a dictionary mapping ticker to Security Name
        self.ticker_name_dict = dict(zip(spx_table['Symbol'], 
                                    spx_table['Security']))
        
        # Create a DataFrame from the default equity sectors dictionary 
        equity_sectors_df = pd.DataFrame.from_dict(
            self.equity_sectors, 
            orient='index', 
            columns=['Sector', 
                     'Industry Group',
                     'Industry'])
        
        # Reset the index and rename as Sub-Industry column
        equity_sectors_df = equity_sectors_df.reset_index()
        equity_sectors_df = equity_sectors_df.rename(
            columns={'index':'Sub-Industry'})        
       
        # Create a sector mappings DataFrame by joining the SPX table from 
        # Wikipedia to the Equity Sectors DataFrame 
        self.sector_mappings_df = spx_table.merge(equity_sectors_df, 
                                                  how='left', 
                                                  left_on='GICS Sub-Industry', 
                                                  right_on='Sub-Industry')
        
        # Set the Index to the Ticker symbol
        self.sector_mappings_df = self.sector_mappings_df.set_index('Symbol')
        
        # Keep only the columns related to the sector levels 
        self.sector_mappings_df = self.sector_mappings_df[
            ['Sector', 'Industry Group', 'Industry', 'Sub-Industry', 
             'Security']]
        
        return self    


    def prepyahoo(self, tickers=None, start_date=None, end_date=None, 
                  ticker_limit=None, lookback=None):
        """
        Create dataframes of prices, extracting data from Yahoo Finance. 

        tickers : List
            List of tickers, represented as strings.
        start : Str
            Start Date represented as a string in the 
            format 'YYYY-MM-DD'.
        end : Str
            End Date represented as a string in the 
            format 'YYYY-MM-DD'.
        ticker_limit : Int, optional
            Flag to select only the first n markets. The default 
            is None.
        lookback : Int, optional
            Number of days history if dates are not specified

        Returns
        -------
        Dict, DataFrames
            Dictionary of DataFrames.

        """
        
        # Set the asset type to 'Equity'
        self.asset_type = 'Equity'
        
        # If a list of tickers are not supplied, take those created in the 
        # initialization process
        if tickers is None:
            tickers = self.tickers
        
        # Set values for the number of tickers to return and the number of days 
        # to look back over, either to those supplied or to the default values  
        (ticker_limit, lookback) = itemgetter(
            'ticker_limit', 'lookback')(self._refresh_params_default(
                 ticker_limit=ticker_limit, lookback=lookback))

        # Set the start and end dates            
        self._date_set(start_date, end_date, lookback)        
                
        # Create dictionaries of DataFrames of prices and ticker names
        self._importyahoo(tickers=tickers, start_date=self.start_date, 
                          end_date=self.end_date, ticker_limit=ticker_limit)
    
        # Remove tickers with short history    
        self._ticker_clean()
    
        return self
   

    def _importyahoo(self, tickers, start_date, end_date, ticker_limit):
        """
        Return dictionary of price histories from Yahoo Finance.

        Parameters
        ----------
        tickers : List
            List of tickers, represented as strings.
        start : Str
            Start Date represented as a string in the 
            format 'YYYY-MM-DD'.
        end : Str
            End Date represented as a string in the 
            format 'YYYY-MM-DD'.
        ticker_limit : Int, optional
            Flag to select only the first n markets. The default 
            is None.

        Returns
        -------
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each 
            ticker.
        exceptions : List
            List of tickers that could not be returned.

        """
        
        # Create empty dictionary and list
        self.raw_ticker_dict = {}
        self.exceptions = []
        
        # Loop through the tickers
        for sym in tickers[:ticker_limit]:
            
            # Attempt to return the data for given ticker
            try:
                self.raw_ticker_dict[sym] = self._returndata(
                    ticker=sym, start_date=start_date, end_date=end_date)
            
            # If error, try replacing '.' with '-' in ticker 
            except:
                try:
                    sym_alt = sym.replace('.','-')
                    self.raw_ticker_dict[sym] = self._returndata(
                        ticker=sym_alt, start_date=start_date, 
                        end_date=end_date)
                
                # If error, add to list of exceptions and move to next 
                # ticker
                except:                    
                    print("Error with "+sym)
                    self.exceptions.append(sym)
                    continue
        
        return self
    

    def _returndata(self, ticker, start_date, end_date):
        """
        Create DataFrame of historic prices for specified ticker.

        Parameters
        ----------
        ticker : Int
            Stock to be returned in the form of Reuters RIC code as a 
            string. 
        start_date : Str
            Start Date represented as a string in the 
            format 'YYYY-MM-DD'.
        end_date : Str
            End Date represented as a string in the 
            format 'YYYY-MM-DD'.
        freq : Int
            Frequency of data - set to 'daily'.

        Returns
        -------
        df : DataFrame
            DataFrame of historic prices for given ticker.

        """
        
        # Initialize a YahooFinancials object with the supplied ticker 
        yahoo_financials = YahooFinancials(ticker)
        
        # Set frequency to daily
        freq='daily'
        
        # Extract historic prices
        df = yahoo_financials.get_historical_price_data(
            start_date, end_date, freq)
        
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

        # Set the proper length of DataFrame to help filter out missing data        
        self._window_set(df=df, start_date=start_date)
        
        return df

    
