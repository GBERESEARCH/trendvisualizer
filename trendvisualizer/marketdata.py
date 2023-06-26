"""
Data extraction functions

"""
import datetime as dt
import norgatedata
import pandas as pd
import requests
from pandas.tseries.offsets import BDay
from yahoofinancials import YahooFinancials


class NorgateExtract():
    """
    Functions to extract data from Norgate Data

    """
    @staticmethod
    def get_norgate_tickers(params: dict) -> dict:
        """
        Create list of all available Norgate Commodity tickers

        Returns
        -------
        tickers : List
            Returns a list of ticker codes.
        init_ticker_dict : Dict
            Dictionary of ticker-security name pairs

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

            if params['tickers_adjusted']:
                # Only take the back-adjusted tickers
                if '_CCB' in key:
                    init_ticker_dict[key] = value

            else:
                if key.startswith('&') and '_CCB' not in key:
                    init_ticker_dict[key] = value

        # Convert the ticker dict keys into a list
        tickers = list(init_ticker_dict.keys())

        params['tickers'] = tickers
        params['init_ticker_dict'] = init_ticker_dict

        return params


    @classmethod
    def importnorgate(
        cls,
        params: dict,
        tables: dict,
        mappings: dict) -> tuple[dict, dict, dict]:
        """
        Return dictionary of price histories from Norgate Data.

        Parameters
        ----------
        params : Dict
            Dictionary of key parameters.
        tables : Dict
            Dictionary of key tables.
        mappings : Dict
            Dictionary of sector mappings.

        Returns
        -------
        tables : Dict
            raw_ticker_dict : Dict
                Dictionary of price history DataFrames, one for each ticker.
        params : Dict
            ticker_name_dict : Dict
                Dictionary mapping ticker to long name for each ticker.
            ticker_short_name_dict : Dict
                Dictionary mapping ticker to short name for each ticker.
        mappings : Dict
            Dictionary of sector mappings

        """
        # Create empty dictionaries
        tables['raw_ticker_dict'] = {}
        params['ticker_name_dict'] = {}
        params['ticker_short_name_dict'] = {}

        # Loop through list of tickers
        for ticker in params['tickers'][:params['ticker_limit']]:

            # Append character to each ticker to represent its type and create
            # lowercase value
            tick = params['ticker_types'][ticker[0]]+ticker[1:]
            lowtick = tick.lower()

            # Set data format and extract each DataFrame, storing as
            # a key-value pair in ticker_dict
            timeseriesformat = 'pandas-dataframe'
            try:
                data = norgatedata.price_timeseries(
                    ticker, start_date=params['start_date'],
                    end_date=params['end_date'],
                    format=timeseriesformat,)

                data = data[['Open', 'High', 'Low', 'Close']]

                tables['raw_ticker_dict'][lowtick] = data

                # Extract the security name and store in ticker_name_dict
                ticker_name = norgatedata.security_name(ticker)
                params['ticker_name_dict'][lowtick] = ticker_name

                # Set the proper length of DataFrame to help filter out
                # missing data
                params = MktUtils.window_set(frame=data, params=params)

            except IndexError:
                print('Error importing : ', ticker)

            #try:
                # Truncate the ticker name to improve charting legibility
                # and store in ticker_short_name_dict
            params['ticker_short_name_dict'][
                lowtick] = ticker_name.partition(" Continuous")[0]

            #except:
            #    params['ticker_short_name_dict'][lowtick] = ticker_name

        # Create sector mappings DataFrame
        mappings['sector_mappings_df'] = cls._commodity_sector_mappings(
            params, mappings)

        return params, tables, mappings


    @staticmethod
    def _commodity_sector_mappings(
        params: dict,
        mappings: dict) -> pd.DataFrame:
        """
        Create sector mappings DataFrame

        Parameters
        ----------
        params : Dict
            Dictionary of key parameters.
        mappings : Dict
            Dictionary of sector mappings.

        Returns
        -------
        sector_mappings_df : DataFrame
            Sector mappings DataFrame.

        """
        # Create empty dictionary
        sectors = {}

        # For each key-value pair in the default sector mappings dictionary
        for key, value in mappings['commodity_sector_mappings'].items():

            # If the first character in the key is in the list of keys from the
            # ticker types dictionary
            if key[0] in list(params['ticker_types'].keys()):

                # Create a new key equal to the lower case original key with
                # the first character replaced by the value in the ticker types
                # dictionary
                new_key = key.lower().replace(
                    key[0], params['ticker_types'][key[0]])

                # create an entry in the sectors dictionary
                sectors[new_key] = value

        # Create a sector mappings DataFrame from the sectors dictionary using
        # the default commodity sector levels list as the column headers
        sector_mappings_df = pd.DataFrame.from_dict(
            sectors,
            orient='index',
            columns=params['commodity_sector_levels'])

        return sector_mappings_df


class YahooExtract():
    """
    Functions to extract data from Yahoo Finance

    """
    @staticmethod
    def tickerextract(
        params: dict,
        mappings: dict) -> tuple[dict, dict]:
        """
        Extract list of S&P 500 Companies from Wikipedia.

        Parameters
        ----------
        params : Dict
            Dictionary of key parameters.
        mappings : Dict
            Dictionary of sector mappings.

        Returns
        -------
        params : Dict
            tickers : List
                List of stock tickers in the form of Reuters RIC codes
                as strings.
            ticker_name_dict : Dict
                Dictionary mapping ticker to long name for each ticker.
        mappings : Dict
            Dictionary of sector mappings.

        """

        # Extract data from the Wikipedia SPX page
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        req = requests.get(url, timeout=10)
        html_doc = req.text
        spx_list = pd.read_html(html_doc)

        # the first table on the page contains the stock data
        spx_table = spx_list[0]

        # create a list of the tickers from the 'Symbol' column
        params['tickers'] = list(spx_table['Symbol'])

        # create a dictionary mapping ticker to Security Name
        params['ticker_name_dict'] = dict(
            zip(spx_table['Symbol'], spx_table['Security']))

        # Create a DataFrame from the default equity sectors dictionary
        equity_sectors_df = pd.DataFrame.from_dict(
            mappings['equity_sector_mappings'],
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
        mappings['sector_mappings_df'] = spx_table.merge(
            equity_sectors_df,
            how='left',
            left_on='GICS Sub-Industry',
            right_on='Sub-Industry')

        # Set the Index to the Ticker symbol
        mappings['sector_mappings_df'] = mappings[
            'sector_mappings_df'].set_index('Symbol')

        # Keep only the columns related to the sector levels
        mappings['sector_mappings_df'] = mappings['sector_mappings_df'][
            ['Sector', 'Industry Group', 'Industry', 'Sub-Industry',
             'Security']]

        return params, mappings


    @classmethod
    def importyahoo(
        cls,
        params: dict,
        tables: dict) -> tuple[dict, dict]:
        """
        Return dictionary of price histories from Yahoo Finance.

        Parameters
        ----------
        params : Dict
            Dictionary of key parameters.
        tables : Dict
            Dictionary of key tables.

        Returns
        -------
        tables : Dict
            raw_ticker_dict : Dict
                Dictionary of price history DataFrames, one for each
                ticker.
        params : Dict
            exceptions : List
                List of tickers that could not be returned.

        """

        # Create empty dictionary and list
        tables['raw_ticker_dict'] = {}
        params['exceptions'] = []

        # Loop through the tickers
        for sym in params['tickers'][:params['ticker_limit']]:

            # Attempt to return the data for given ticker
            try:
                tables['raw_ticker_dict'][sym], params = cls._returndata(
                    ticker=sym, params=params)

            # If error, try replacing '.' with '-' in ticker
            except KeyError:
                try:
                    sym_alt = sym.replace('.','-')
                    tables['raw_ticker_dict'][sym], params = cls._returndata(
                        ticker=sym_alt, params=params)

                # If error, add to list of exceptions and move to next
                # ticker
                except KeyError:
                    print("Error with "+sym)
                    params['exceptions'].append(sym)
                    continue

        return params, tables


    @staticmethod
    def _returndata(
        ticker: str,
        params: dict) -> tuple[pd.DataFrame, dict]:
        """
        Create DataFrame of historic prices for specified ticker.

        Parameters
        ----------
        ticker : Str
            Stock to be returned in the form of Reuters RIC code as a
            string.
        params : Dict
            start_date : Str
                Start Date represented as a string in the
                format 'YYYY-MM-DD'.
            end_date : Str
                End Date represented as a string in the
                format 'YYYY-MM-DD'.

        Returns
        -------
        frame : DataFrame
            DataFrame of historic prices for given ticker.
        params : Dict
            Dictionary of key parameters.

        """

        # Initialize a YahooFinancials object with the supplied ticker
        yahoo_financials = YahooFinancials(ticker)

        # Set frequency to daily
        freq='daily'

        # Extract historic prices
        frame = yahoo_financials.get_historical_price_data(
            params['start_date'], params['end_date'], freq)

        # Reformat columns
        frame = pd.DataFrame(frame[ticker]['prices']).drop(['date'], axis=1) \
                .rename(columns={'formatted_date':'Date',
                                 'open': 'Open',
                                 'high': 'High',
                                 'low': 'Low',
                                 'close': 'Close',
                                 'volume': 'Volume'}) \
                .loc[:, ['Date','Open','High','Low','Close','Volume']] \
                .set_index('Date')

        # Set Index to Datetime
        frame.index = pd.to_datetime(frame.index)

        # Set the proper length of DataFrame to help filter out missing data
        params = MktUtils.window_set(frame=frame, params=params)

        return frame, params


class MktUtils():
    """
    Various market data cleaning utilities

    """
    @staticmethod
    def ticker_clean(
        params: dict,
        tables: dict) -> dict:
        """
        Remove tickers with incomplete history

        Parameters
        ----------
        params : Dict
            Dictionary of key parameters.
        tables : Dict
            Dictionary of key tables.

        Returns
        -------
        tables : Dict
            Dictionary of key tables.

        """
        # Create empty list of tickers to be removed
        params['drop_list'] = []

        # Loop through each DataFrame in raw ticker dict
        for ticker, frame in tables['raw_ticker_dict'].items():

            # If the DataFrame has less than 90% full history or has too many
            # repeated values
            if (len(frame) < (params['window'] * 0.9)
                or frame['Close'].nunique() < (params['lookback'] / 15)):

                # Add ticker to the drop list
                params['drop_list'].append(ticker)

        # For each ticker in the drop list
        for ticker in params['drop_list']:

            # Delete the ticker from the dictionary
            del tables['raw_ticker_dict'][ticker]

        return tables


    @staticmethod
    def window_set(
        frame: pd.DataFrame,
        params: dict) -> dict:
        """
        Set the correct length of the selected data

        Parameters
        ----------
        frame : DataFrame
            The historical prices.
        params : Dict
            start_date : Str
                The chosen start date.

        Returns
        -------
        params : Dict
            Dictionary of key parameters.

        """
        # If the history window has not yet been set
        if params['window'] is None:

            # If the difference in start dates between the chosen start date
            # and the first value in the index is less than 5 days
            if ((pd.to_datetime(params['start_date'])
                 - frame.index[0]).days < 5):

                # Set the window length to the length of the DataFrame
                params['window'] = len(frame)

        return params


    @staticmethod
    def date_set(params: dict) -> dict:
        """
        Create start and end dates if not supplied

        Parameters
        ----------
        params : Dict
            start_date : Str, optional
                Date to begin backtest. Format is YYYY-MM-DD. The default is
                500 business days prior (circa 2 years).
            end_date : Str, optional
                Date to end backtest. Format is YYYY-MM-DD. The default is the
                last business day.
            lookback : Int, optional
                Number of business days to use for the backtest. The default
                is 500 business days (circa 2 years).

        Returns
        -------
        params : Dict
            Dictionary of key parameters.

        """

        # If end date is not supplied, set to previous working day
        if params['end_date'] is None:
            end_date_as_dt = (dt.datetime.today() - BDay(1)).date()
            params['end_date'] = str(end_date_as_dt)

        # If start date is not supplied, set to today minus lookback period
        if params['start_date'] is None:
            start_date_as_dt = (
                dt.datetime.today()
                - pd.Timedelta(days=params['lookback']*(365/250))).date()
            params['start_date'] = str(start_date_as_dt)

        return params
