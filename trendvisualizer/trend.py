"""
Calculate Trend Strength across various markets / asset classes and graph
results

"""
import copy
from trendvisualizer.chart_display import Graphs
from trendvisualizer.pie_charts import PieCharts
from trendvisualizer.sector_mappings import sectmap
from trendvisualizer.trend_params import trend_params_dict
from trendvisualizer.trenddata import Fields, TickerList
from trendvisualizer.marketdata import NorgateExtract, YahooExtract, MktUtils


class TrendStrength():
    """
    Create Trend Strength data and display results

    Parameters
    ----------
    chart_dimensions : Tuple
        Tuple of height, width for market chart.
    chart_mkts : Int
        Number of markets for market chart.
    days : Int
        The number of days price history.
    end_date : Str
        End Date represented as a string in the
        format 'YYYY-MM-DD'.
    indicator_type : Str
        The indicator to plot. Choose from 'adx', 'ma_cross',
        'price_cross', 'rsi', 'breakout'.
    lookback : Int
        Number of days history if dates are not specified
    mkts : Int
        Number of markets for barchart or linegraph.
    norm : Bool
        Whether the prices have been normalised.
    pie_tenor : Int / Tuple
        The time period of the indicator. For the Moving Average
        crossover this is a tuple from the following pairs: (5, 200),
        (10, 30), (10, 50), (20, 50), (30, 100), (50, 200). For the
        other indicators this is an integer from the list: 10, 20, 30,
        50, 100, 200.
    sector_level : Int
        The level of granularity of the assets.
        For Commodities the choices are:
            1:'Asset Class',
            2:'Broad Sector',
            3:'Mid Sector',
            4:'Narrow Sector',
            5:'Underlying'.
        For Equities the choices are:
            1:'Sector',
            2:'Industry Group',
            3:'Industry',
            4:'Sub-Industry',
            5:'Security'
    source : Str
        The source of the market data. 'norgate' or 'yahoo'. The default is
        'norgate'.
    start_date : Str
        Start Date represented as a string in the
        format 'YYYY-MM-DD'.
    tickers : List
        List of tickers, represented as strings.
    ticker_limit : Int
        Flag to select only the first n markets. The default
        is None.
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
    None.

    """
    def __init__(self, **kwargs):

        # Import dictionary of default parameters
        self.default_dict = copy.deepcopy(trend_params_dict)

        # Import dictionary of sector mappings
        mappings = copy.deepcopy(sectmap)

        # Store initial inputs
        inputs = {}
        for key, value in kwargs.items():
            inputs[key] = value

        # Initialise system parameters
        params = self._init_params(inputs)

        # Dictionary to store data tables
        tables = {}

        # Import the data from Norgate Data
        if params['source'] == 'norgate':
            params, tables, mappings = self.prepnorgate(
                 params=params, tables=tables, mappings=mappings)

        # Or from Yahoo Finance
        elif params['source'] == 'yahoo':
            params, tables, mappings = self.prepyahoo(
                params=params, tables=tables, mappings=mappings)

        # Calculate the technical indicator fields and Trend Strength table
        tables = self.trendcalc(
            params=params, tables=tables, mappings=mappings)

        # Generate list of top trending securities
        self.trend_ticker_list, self.tables = self.top_trend_tickers(
            params=params, tables=tables)

        self.params = params
        self.mappings = mappings


    @staticmethod
    def _init_params(inputs):
        """
        Initialise parameter dictionary
        Parameters
        ----------
        inputs : Dict
            Dictionary of parameters supplied to the function.

        Returns
        -------
        params : Dict
            Dictionary of parameters.
        """
        # Copy the default parameters
        params = copy.deepcopy(trend_params_dict['df_params'])

        # For all the supplied arguments
        for key, value in inputs.items():

            # Replace the default parameter with that provided
            params[key] = value

        return params


    @staticmethod
    def prepnorgate(params, tables, mappings):
        """
        Create dataframes of prices, extracting data from Norgate Data.

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
        params : Dict
            Dictionary of key parameters.
        tables : Dict
            Dictionary of key tables.
        mappings : Dict
            Dictionary of sector mappings.

        """

        # Set the asset type to 'CTA'
        params['asset_type'] = 'CTA'

        # If a list of tickers are not supplied, run the function to collect
        # available tickers
        if params['tickers'] is None:
            params['tickers'], params[
                'init_ticker_dict'] = NorgateExtract.get_norgate_tickers()

        # Set the start and end dates
        params = MktUtils.date_set(params)

        # Create dictionaries of DataFrames of prices and ticker names
        params, tables, mappings = NorgateExtract.importnorgate(
            params=params, tables=tables, mappings=mappings)

        # Remove tickers with short history
        tables = MktUtils.ticker_clean(params=params, tables=tables)

        return params, tables, mappings


    @staticmethod
    def prepyahoo(params, tables, mappings):
        """
        Create dataframes of prices, extracting data from Yahoo Finance.

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
        params : Dict
            Dictionary of key parameters.
        tables : Dict
            Dictionary of key tables.
        mappings : Dict
            Dictionary of sector mappings.

        """

        # Create list of tickers, dictionary of ticker names from
        # Wikipedia
        params, mappings = YahooExtract.tickerextract(
            params=params, mappings=mappings)

        # Set short_name_dict = name_dict
        params['ticker_short_name_dict'] = params['ticker_name_dict']

        # Set the asset type to 'Equity'
        params['asset_type'] = 'Equity'

        # Set the start and end dates
        params = MktUtils.date_set(params)

        # Create dictionaries of DataFrames of prices and ticker names
        params, tables = YahooExtract.importyahoo(params, tables)

        # Remove tickers with short history
        tables = MktUtils.ticker_clean(params=params, tables=tables)

        return params, tables, mappings


    @staticmethod
    def trendcalc(params, tables, mappings):
        """
        Calculate the technical indicator fields and Trend Strength table

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
            Dictionary of key tables.

        """
        # Calculate the technical indicator fields
        tables['ticker_dict'] = Fields.generate_fields(
            params, tables['raw_ticker_dict'])

        # Calculate the Trend Strength table
        tables['barometer'] = Fields.generate_trend_strength(
            params=params, ticker_dict=tables['ticker_dict'],
            sector_mappings_df=mappings['sector_mappings_df'])

        return tables


    @staticmethod
    def top_trend_tickers(params, tables):
        """
        Prepare list of top trending securities.

        Parameters
        ----------
        params : Dict
            Dictionary of key parameters.
        tables : Dict
            Dictionary of key tables.

        Returns
        -------
        ticker_list : List
                List of top trending securities.
        tables : Dict
            Dictionary of key tables.

        """
        # Generate list of top trending securities
        if params['source'] == 'norgate':
            norgate_source=True
        else:
            norgate_source=False

        ticker_list, tables = TickerList.top_trend_list(
            tables, params, norgate_source=norgate_source)


        return ticker_list, tables


    def chart(self, chart_type, **kwargs):
        """
        Display the selcted chart of Trend Strength

        Parameters
        ----------
        chart_type : Str
            The typr of chart to display.
        **kwargs : Dict
            Parameters supplied to override the defaults.

        Returns
        -------
        Displays the selected chart.

        """
        # Update params with the specified parameters
        for key, value in kwargs.items():

            # Replace the default parameter with that provided
            self.params[key] = value

        if chart_type == 'bar':
            Graphs.trendbarchart(
                params=self.params, barometer=self.tables['barometer'])

        elif chart_type == 'returns':
            Graphs.returnsgraph(params=self.params, tables=self.tables)

        elif chart_type == 'market':
            self.params = Graphs.marketchart(
                params=self.params, tables=self.tables)

        elif chart_type == 'summary':
            self.params, self.tables = Graphs.summaryplot(
                params=self.params, tables=self.tables)

        elif chart_type == 'pie_summary':
            self.params = PieCharts.pie_summary(
                params=self.params, barometer=self.tables['barometer'])

        elif chart_type == 'pie_breakdown':
            self.params, self.tables = PieCharts.pie_breakdown(
                params=self.params, tables=self.tables)

        else:
            print("Please select a valid graph from 'bar', 'returns', \
                  'market', 'pie_summary', 'pie_breakdown' and 'summary'")
