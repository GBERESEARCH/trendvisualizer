"""
Generate trend strength fields

"""
import warnings
import numpy as np
import pandas as pd
from technicalmethods.methods import Indicators

class Fields():
    """
    Create trend strength fields across range of tickers

    """

    @classmethod
    def generate_fields(cls, params, ticker_dict):
        """
        Create and add various trend indicators to each DataFrame in
        the dictionary of tickers

        Parameters
        ----------
        params : Dict
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
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each ticker.

        Returns
        -------
        ticker_dict : Dict
            Dictionary of DataFrames of each ticker updated with additional
            trend indicators.

        """

        with warnings.catch_warnings():
            warnings.filterwarnings("error")

            # Loop through each ticker in ticker_dict
            for ticker, frame in ticker_dict.items():

                # Create moving averages of 10, 20, 30, 50 and 200 day
                # timeframes
                frame = cls._field_ma(
                    params=params, frame=frame, ticker=ticker)

                # Create flag for price crossing moving average
                frame = cls._field_px_ma(
                    params=params, frame=frame, ticker=ticker)

                # Create MACD, Signal and Hist using default parameters
                # of 12, 26, 9
                frame = cls._field_macd(
                    params=params, frame=frame, ticker=ticker)

                # Create ADX of 14, 20, 50, 100 and 200 day timeframes
                # Create flags for ADX over 25
                frame = cls._field_adx(
                    params=params, frame=frame, ticker=ticker)

                # Create flag for fast moving average crossing slow moving
                # average
                frame = cls._field_ma_cross(
                    params=params, frame=frame, ticker=ticker)

                # Create RSI with 14, 20, 50, 100 and 200 day timeframes
                # Create flag for RSI over 70 or under 30
                frame = cls._field_rsi(
                    params=params, frame=frame, ticker=ticker)

                # Create breakout flags with 14, 20, 50, 100 and 200 day
                # timeframes
                frame = cls._field_breakout(
                    params=params, frame=frame, ticker=ticker)

                # Create Average True Range with 14 day timeframe
                frame = cls._field_atr(
                    params=params, frame=frame, ticker=ticker)

        return ticker_dict


    @staticmethod
    def _field_ma(params, frame, ticker):
        for tenor in params['ma_list']:
            try:
                frame['MA_'+str(tenor)] = frame['Close'].rolling(
                    window=str(tenor)+'D').mean()

            except RuntimeWarning:
                print("Error with "
                      + ticker
                      + " MA_"
                      + str(tenor)
                      + " : More than "
                      + str(tenor)
                      + " consecutive days unchanged price")

        return frame


    @staticmethod
    def _field_px_ma(params, frame, ticker):
        for tenor in params['price_cross_list']:
            try:
                frame['PX_MA_'+str(tenor)+'_flag'] = np.where(
                    frame['Close'] > frame['MA_'+str(tenor)], 1, -1)

            except RuntimeWarning:
                print("Error with "
                      + ticker
                      + " PX_MA_"
                      + str(tenor)
                      + " : More than "
                      + str(tenor)
                      + " consecutive days unchanged price")

        return frame


    @staticmethod
    def _field_macd(params, frame, ticker):
        try:
            frame['MACD'], frame['MACD_SIGNAL'], \
                frame['MACD_HIST'] = Indicators.MACD(
                    close=frame['Close'],
                    fast=params['macd_params'][0],
                    slow=params['macd_params'][1],
                    signal=params['macd_params'][2])

            # Create flag for MACD histogram increasing
            frame['MACD_flag'] = np.where(
                frame['MACD_HIST'].diff() > 0, 1, -1)

        except RuntimeWarning:
            print("Error with " + ticker + " MACD")

        return frame


    @staticmethod
    def _field_adx(params, frame, ticker):
        for tenor in params['adx_list']:
            try:
                frame['ADX_'+str(tenor)] = Indicators.ADX(
                    high=frame['High'],
                    low=frame['Low'],
                    close=frame['Close'],
                    time_period=tenor)
                frame['ADX_'+str(tenor)+'_flag'] = np.where(
                    frame['ADX_'+str(tenor)] > 25, np.where(
                        frame['PX_MA_'+str(tenor)+'_flag'] == 1, 1, -1), 0)

            except RuntimeWarning:
                print("Error with "
                      + ticker
                      + " ADX_"+str(tenor)
                      + " : More than "
                      + str(tenor)
                      + " consecutive days unchanged price")

        return frame


    @staticmethod
    def _field_ma_cross(params, frame, ticker):
        for tenor_pair in params['ma_cross_list']:
            try:
                frame['MA_'+str(tenor_pair[0])+'_'+str(
                    tenor_pair[1])+'_flag'] = np.where(
                        frame['MA_'+str(tenor_pair[0])] > frame[
                            'MA_'+str(tenor_pair[1])], 1, -1)

            except RuntimeWarning:
                print("Error with " + ticker + " MA_"+str(tenor_pair))

        return frame


    @staticmethod
    def _field_rsi(params, frame, ticker):
        for tenor in params['rsi_list']:
            try:
                frame['RSI_'+str(tenor)] = Indicators.RSI(
                    close=frame['Close'], time_period=tenor)
                frame['RSI_'+str(tenor)+'_flag'] = np.where(
                    frame['RSI_'+str(tenor)] > 70, 1, np.where(
                        frame['RSI_'+str(tenor)] < 30, -1, 0))

            except RuntimeWarning:
                print("Error with "
                      + ticker
                      + " RSI_"+str(tenor)
                      + " : More than "
                      + str(tenor)
                      + " consecutive days unchanged price")

        return frame


    @staticmethod
    def _field_breakout(params, frame, ticker):
        for tenor in params['breakout_list']:
            try:
                frame['low_'+str(tenor)], frame['high_'+str(tenor)], \
                    frame['breakout_'+str(
                        tenor)+'_flag'] = Indicators.breakout(
                            high=frame['High'], low=frame['Low'],
                            time_period=tenor)

            except RuntimeWarning:
                print("Error with "
                      + ticker
                      + " breakout_"
                      + str(tenor)
                      + " : More than "
                      + str(tenor)
                      + " consecutive days unchanged price")

        return frame


    @staticmethod
    def _field_atr(params, frame, ticker):
        for tenor in params['atr_list']:
            try:
                frame['ATR_'+str(tenor)] = Indicators.ATR(
                    high=frame['High'],
                    low=frame['Low'],
                    close=frame['Close'],
                    time_period=tenor)

            except RuntimeWarning:
                print("Error with "
                      + ticker
                      + " ATR_"
                      + str(tenor)
                      + " : More than "
                      + str(tenor)
                      + " consecutive days unchanged price")

        return frame



    @classmethod
    def generate_trend_strength(cls, params, ticker_dict, sector_mappings_df):
        """
        Create a DataFrame showing the strength of trend for selected
        markets.

        Parameters
        ----------

        params : Dict
            trend_flags : List
                The list of indicators used to calculate the strength of the
                trend.
                The default values are ['PX_MA_10',
                                        'ADX_10_flag',
                                        'RSI_10_flag',
                                        'breakout_10_flag',
                                        'MA_10_30',
                                        'MACD_flag',
                                        'PX_MA_20',
                                        'MA_20_50',
                                        'ADX_20_flag',
                                        'RSI_20_flag',
                                        'breakout_20_flag',
                                        'PX_MA_30',
                                        'ADX_30_flag',
                                        'RSI_30_flag',
                                        'breakout_30_flag',
                                        'PX_MA_50',
                                        'MA_50_200',
                                        'ADX_50_flag',
                                        'RSI_50_flag',
                                        'breakout_50_flag',
                                        'PX_MA_100',
                                        'ADX_100_flag',
                                        'RSI_100_flag',
                                        'breakout_100_flag',
                                        'PX_MA_200',
                                        'ADX_200_flag',
                                        'RSI_200_flag',
                                        'breakout_200_flag'
                                        ].
        ticker_dict : Dict
            Dictionary of price history DataFrames, one for each ticker.
        sector_mappings_df : DataFrame
            Sector mappings DataFrame.

        Returns
        -------
        barometer : DataFrame
            DataFrame showing trend strength for each ticker.

        """

        # Prepare dataframe from ticker_dict
        frame = cls._prepframe(params, ticker_dict)

        # Loop through each ticker in ticker_dict to populate trend
        # flags in frame
        for ticker, dataframe in ticker_dict.items():
            for flag in params['trend_flags']:
                try:
                    frame.loc[ticker, flag] = dataframe[flag].iloc[-1]

                except KeyError:
                    print("Missing ticker: "
                          + ticker
                          + " , trend flag: "
                          + flag
                          + " from ticker dict")
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

        # Add column showing trend strength as Red, Amber, Green
        barometer = frame.apply(cls._col_color, axis=1)

        # Apply sector mappings
        barometer = cls._barometer_sectors(
            params, barometer, sector_mappings_df)

        return barometer


    @staticmethod
    def _prepframe(params, ticker_dict):

        # Create list of tickers from ticker_dict
        ticker_list = [ticker for ticker, df in ticker_dict.items()]

        # Convert ticker_name_dict to DataFrame
        ticker_name_df = pd.DataFrame.from_dict(
            params['ticker_name_dict'], orient='index', columns=['Long_name'])

        # Create empty DataFrame with Trend Flags as columns and
        # tickers as rows
        frame = pd.DataFrame(columns=params['trend_flags'], index=ticker_list)

        # Merge the two DataFrames
        frame = pd.merge(frame, ticker_name_df, left_index=True,
                         right_index=True)

        # Reorder columns with list of column names moving the
        # Long Name to the start
        cols = [frame.columns[-1]] + [col for col in frame
                                      if col != frame.columns[-1]]
        frame = frame[cols]

        return frame


    @staticmethod
    def _col_color(row):

        # Create trend strength color column and absolute strength column
        row['Absolute Trend Strength'] = np.abs(row['Trend Strength'])

        if np.abs(row['Trend Strength']) < 5:
            row['Trend Color'] = 'red'

        elif np.abs(row['Trend Strength']) < 10:
            row['Trend Color'] = 'orange'

        else:
            row['Trend Color'] = 'green'

        return row


    @staticmethod
    def _barometer_sectors(params, barometer, sector_mappings_df):
        """
        Add sector mappings to the trend barometer table to use in summary
        graph

        Parameters
        ----------
        params : Dict
            Dictionary of key parameters.
        sector_mappings_df : DataFrame
            Sector mappings DataFrame.
        barometer : DataFrame
            DataFrame showing trend strength for each ticker.

        Returns
        -------
        barometer : DataFrame
            barometer updated with additional sector columns.

        """

        # Calculate the number of trend indicators
        num_flags = len(params['trend_flags'])

        # Join the baometer table to the sector mappings table
        barometer = barometer.join(sector_mappings_df)

        # Calculate Trend Strength as a percentage by dividing by the number
        # of trend indicators
        barometer['Trend Strength %'] = barometer[
            'Trend Strength'] / num_flags

        # Calculate the absolute value of trend strength as a percentage
        barometer['Absolute Trend Strength %'] = abs(
            barometer['Trend Strength %'])

        # Reset the index and rename column as 'Ticker
        barometer = barometer.reset_index()
        barometer = barometer.rename(columns={'index':'Ticker'})

        # Add a column as the string 'Trend' to use in swarm plot
        barometer['Trend'] = 'Trend'

        return barometer


class TickerList():
    """
    Generate list of strongly trending securities

    """

    @staticmethod
    def futures_split(tables):
        """
        Split the continuous futures from the rest of the norgate data

        Parameters
        ----------
        tables : Dict
            Dictionary of key tables.

        Returns
        -------
        tables : Dict
            Dictionary of key tables updated for futures_ticker_dict and
            futures_barometer.

        """
        tables['futures_ticker_dict'] = {
            k:v for k,v in tables['raw_ticker_dict'].items()
            if '_ccb' in k}
        tables['futures_barometer'] = tables['barometer'][
            tables['barometer']['Ticker'].str.lower().str.contains('_ccb')]

        return tables


    @classmethod
    def _filter_barometer(cls, tables, params, norgate_source):
        """
        Sort and filter the top trending securities

        Parameters
        ----------
        barometer : DataFrame
            DataFrame showing trend strength for each ticker.
        norgate_source : Bool
            Whether the market data source is norgate or yahoo.

        Returns
        -------
        filtered_barometer : DataFrame
            DataFrame showing the top trending securities.

        """
        if norgate_source:
            # Split the continuous futures data
            tables = cls.futures_split(tables)
            barometer = tables['futures_barometer']
        else:
            barometer = tables['barometer']

        data = barometer.sort_values(
            by=['Absolute Trend Strength'],
            ascending=False)[:params['top_trend_params']['initial_size']]

        filtered_barometer = pd.DataFrame()

        if norgate_source:
            sectors = set(barometer['Mid Sector'])
            data = data.sort_values(
                by=['Mid Sector', 'Absolute Trend Strength'],
                ascending=False)
        else:
            sectors = set(barometer['Sector'])
            data = data.sort_values(
                by=['Sector', 'Absolute Trend Strength'], ascending=False)

        for sector in sectors:
            if norgate_source:
                frame = data[data['Mid Sector']==sector]
            else:
                frame = data[data['Sector']==sector]

            if len(frame) > 0:
                if norgate_source:
                    frame = frame.drop_duplicates(subset='Underlying')
                else:
                    frame = frame.drop_duplicates(subset='Security')

                if len(frame) > params['top_trend_params']['max_per_sector']:
                    frame = frame[:params['top_trend_params'][
                        'max_per_sector']]
                filtered_barometer = pd.concat([filtered_barometer, frame])

        filtered_barometer = filtered_barometer.sort_values(
            by=['Absolute Trend Strength'],
            ascending=False)[:params['top_trend_params']['final_size']]

        return filtered_barometer


    @classmethod
    def top_trend_list(cls, tables, params, norgate_source):
        """
        Prepare list of top trending securities.

        Parameters
        ----------
        barometer : DataFrame
            DataFrame showing trend strength for each ticker.
        norgate_source : Bool
            Whether the market data source is norgate or yahoo.

        Returns
        -------
        ticker_list : List
            List of top trending securities.
        tables : Dict
            Dictionary of key tables updated for the filtered barometer.

        """
        tables['filtered_barometer'] = cls._filter_barometer(
            tables, params, norgate_source)
        ticker_list = []
        for ticker in tables['filtered_barometer']['Ticker']:
            if norgate_source:
                ticker = '&'+ticker.upper()
                ticker = ticker.replace('&C_','&')
            ticker_list.append(ticker)

        return ticker_list, tables
