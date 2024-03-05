"""
Prepare data for charts and graphs

"""

import copy
import math
import pandas as pd

class Formatting():
    """
    Various data formatting methods for graphing

    """
    @staticmethod
    def get_chart_title(params: dict) -> str:
        """
        Create title label for market chart

        Parameters
        ----------
        norm : Bool
            Whether the prices have been normalised.
        trend : Str
            The type / direction of the trend.
        days : Int
            The number of days price history.

        Returns
        -------
        charttitle : Str
            The chart title label.

        """
        norm = params['norm']
        trend = params['trend']
        days = params['days']

        # Update chart title based on whether the data is normalized
        # and the chosen trend type to display
        if norm:
            if trend == 'up':
                chart_title = ("Up Trending Markets"
                              +" - Relative Return Over Last "
                              +str(days)+' Trading Days')

            if trend == 'down':
                chart_title = ("Down Trending Markets"
                              +" - Relative Return Over Last "
                              +str(days)+' Trading Days')

            if trend == 'strong':
                chart_title = ("Most Strongly Trending Markets"
                              +" - Relative Return Over Last "
                              +str(days)+' Trading Days')

            if trend == 'neutral':
                chart_title = ("Neutral Trending Markets"
                              +" - Relative Return Over Last "
                              +str(days)+' Trading Days')

            if trend == 'all':
                chart_title = ("Most Strongly and Neutral Trending"
                              +" Markets - Price Over Last "
                              +str(days)+' Trading Days')

        else:
            if trend == 'up':
                chart_title = ("Up Trending Markets"
                              +" - Price Over Last "
                              +str(days)+' Trading Days')

            if trend == 'down':
                chart_title = ("Down Trending Markets"
                              +" - Price Over Last "
                              +str(days)+' Trading Days')

            if trend == 'strong':
                chart_title = ("Most Strongly Trending Markets"
                              +" - Price Over Last "
                              +str(days)+' Trading Days')

            if trend == 'neutral':
                chart_title = ("Neutral Trending Markets"
                              +" - Price Over Last "
                              +str(days)+' Trading Days')

            if trend == 'all':
                chart_title = ("Most Strongly and Neutral Trending"
                              +" Markets - Price Over Last "
                              +str(days)+' Trading Days')
        
        chart_title = str(chart_title)

        chart_title = chart_title+' - '+params['end_date']

        return chart_title


    @staticmethod
    def create_mkt_dims(params: dict) -> dict:
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
        mkts = params['chart_mkts']

        if mkts % 5 == 0:
            width = 5

        elif mkts % 4 == 0:
            width = 4

        elif mkts < 20 and mkts % 3 == 0:
            width = 3

        elif (mkts+1) % 5 == 0:
            width = 5

        elif (mkts+1) % 4 == 0:
            width = 4

        elif mkts < 20 and (mkts+1) % 3 == 0:
            width = 3

        else:
            width = 5

        height = math.ceil(mkts/width)
        params['chart_dimensions'] = (height, width)

        return params


    @classmethod
    def create_normalized_data(
        cls,
        params: dict,
        tables: dict) -> pd.DataFrame:
        """
        Create a subset of chart_prep dataset normalized to start from
        100 for the specified history window

        Parameters
        ----------
        params : Dict
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
        tables : Dict
            Dictionary of key tables.

        Returns
        -------
        tenor : DataFrame
            DataFrame of closing prices, normalized for a given historic
            window

        """

        chart_data = cls._create_chart_data(params=params, tables=tables)

        # Copy the selected number of days history from the input
        # DataFrame
        tenor = copy.deepcopy(chart_data[-params['days']:])

        # Normalize the closing price of each ticker to start from 100
        # at the beginning of the history window
        for ticker in tenor.columns:
            tenor[ticker] = tenor[ticker].div(tenor[ticker].iloc[0]).mul(100)

        return tenor


    @classmethod
    def _create_chart_data(
        cls,
        params: dict,
        tables: dict) -> pd.DataFrame:
        """
        Create a time series of closing prices for selected markets.

        Parameters
        ----------
        params : Dict
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
        tables : Dict
            Dictionary of key tables.

        Returns
        -------
        chart_data : DataFrame
            DataFrame of closing prices of tickers selected by trend
            strength.

        """

        data_list = cls.create_data_list(
            params, 
            tables['barometer'], 
            market_chart=False, 
            num_charts=None
            )

        # Create a new DataFrame
        chart_data = pd.DataFrame()

        # For each ticker in the list of selected tickers, add the
        # column of closing prices to new DataFrame
        for ticker in data_list:
            chart_data[ticker] = tables['ticker_dict'][ticker]['Close']

        # Rename columns from tickers to short names and forward fill
        # any NaN cells
        chart_data = chart_data.rename(
            columns=params['ticker_short_name_dict'])
        chart_data = chart_data.fillna(method='ffill')

        return chart_data


    @classmethod
    def create_data_list(
        cls,
        params: dict,
        barometer: pd.DataFrame,
        market_chart: bool,
        num_charts: int | None) -> list:
        """
        Create a list of the most / least trending markets.

        Parameters
        ----------
        params : Dict
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
        barometer : DataFrame
            DataFrame showing trend strength for each ticker.
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
        trend = params['trend']
        mkts = params['mkts']

        # if trend flag is 'up', select tickers of most up trending
        # markets
        if trend == 'up':
            data_list = cls._up_trend(
                barometer=barometer, market_chart=market_chart,
                num_charts=num_charts, mkts=mkts)

        # if trend flag is 'down', select tickers of most down trending
        # markets
        elif trend == 'down':
            data_list = cls._down_trend(
                barometer=barometer, market_chart=market_chart,
                num_charts=num_charts, mkts=mkts)

        # if trend flag is 'neutral', select tickers of least trending
        # markets
        elif trend == 'neutral':
            data_list = cls._neutral_trend(
                barometer=barometer, market_chart=market_chart,
                num_charts=num_charts, mkts=mkts)

        # if trend flag is 'strong', select tickers of most down trending
        # markets
        elif trend == 'strong':
            data_list = cls._strong_trend(
                barometer=barometer, market_chart=market_chart,
                num_charts=num_charts, mkts=mkts)

        # Otherwise select all 3
        else:
            data_list = cls._mixed_trend(
                barometer=barometer, market_chart=market_chart,
                num_charts=num_charts, mkts=mkts)

        return data_list


    @staticmethod
    def _up_trend(
        barometer: pd.DataFrame,
        market_chart: bool,
        num_charts: int | None,
        mkts: int) -> list:

        # Sort by Trend Strength
        barometer = barometer.sort_values(
            by=['Trend Strength'], ascending=False)

        if market_chart:
            # Select the specified number of highest values
            data_list = list(barometer['Ticker'].iloc[:num_charts])

        else:
            # Select the highest values
            data_list = list(barometer['Ticker'].iloc[:mkts])

        return data_list


    @staticmethod
    def _down_trend(
        barometer: pd.DataFrame,
        market_chart: bool,
        num_charts: int | None,
        mkts: int) -> list:

        # Sort by Trend Strength
        barometer = barometer.sort_values(
            by=['Trend Strength'], ascending=False)

        if (market_chart and num_charts !=None) :
            # Select the specified number of lowest values
            data_list = list(barometer['Ticker'].iloc[-num_charts:])

        else:
            # Select the lowest values
            data_list = list(barometer['Ticker'].iloc[-mkts:])

        return data_list


    @staticmethod
    def _neutral_trend(
        barometer: pd.DataFrame,
        market_chart: bool,
        num_charts: int | None,
        mkts: int) -> list:

        # Sort by Absolute Trend Strength
        barometer = barometer.sort_values(
            by=['Absolute Trend Strength'], ascending=False)

        if (market_chart and num_charts !=None):
            # Select the specified number of lowest values
            data_list = list(barometer['Ticker'].iloc[-num_charts:])

        else:
            # Select the lowest values
            data_list = list(barometer['Ticker'].iloc[-mkts:])

        return data_list


    @staticmethod
    def _strong_trend(
        barometer: pd.DataFrame,
        market_chart: bool,
        num_charts: int | None,
        mkts: int) -> list:

        # Sort by Trend Strength
        barometer = barometer.sort_values(
            by=['Trend Strength'], ascending=False)

        if (market_chart and num_charts !=None):
            # Select the specified number of highest values
            top = list(barometer['Ticker'].iloc[:int(num_charts/2)])

            # Select the lowest values
            bottom = list(barometer['Ticker'].iloc[
                -(num_charts-int(num_charts/2)):])

        else:
            # Select the highest values
            top = list(barometer['Ticker'].iloc[:int(mkts/2)])

            # Select the lowest values
            bottom = list(barometer['Ticker'].iloc[
                -(mkts-int(mkts/2)):])

        # Combine this data
        data_list = top + bottom

        return data_list


    @staticmethod
    def _mixed_trend(
        barometer: pd.DataFrame,
        market_chart: bool,
        num_charts: int | None,
        mkts: int) -> list:

        # Sort by Trend Strength
        barometer = barometer.sort_values(
            by=['Trend Strength'], ascending=False)

        if (market_chart and num_charts !=None):
            # Select 1/3 of the specified number of highest values
            top = list(barometer['Ticker'].iloc[:int(num_charts/3)])

            # Select 1/3 of the specified number of lowest values
            bottom = list(barometer['Ticker'].iloc[-int(num_charts/3):])

            # Sort by Absolute Trend Strength
            barometer = barometer.sort_values(
                by=['Absolute Trend Strength'], ascending=False)

            # Select 1/3 of the specified number of lowest values
            neutral = list(barometer['Ticker'].iloc[
                -(num_charts-2*int(num_charts/3)):])

        else:
            # Select the highest values
            top = list(barometer['Ticker'].iloc[:int(mkts/3)])

            # Select the lowest values
            bottom = list(barometer['Ticker'].iloc[-int(mkts/3):])

            # Sort by Absolute Trend Strength
            barometer = barometer.sort_values(
                by=['Absolute Trend Strength'], ascending=False)

            # Select the lowest values
            neutral = list(barometer['Ticker'].iloc[
                -(mkts-2*int(mkts/3)):])

        # Combine this data
        data_list = top + bottom + neutral

        return data_list


    @classmethod
    def summary_config(
        cls,
        params: dict,
        barometer: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
        """
        Configure inputs for Trend Summary plots

        Parameters
        ----------
        params : Dict
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
        barometer : DataFrame
            DataFrame showing trend strength for each ticker.

        Returns
        -------
        params : Dict
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
        if params['asset_type'] == 'CTA':
            params['sector_name'] = params[
                'commodity_sector_levels'][params['sector_level']-1]
            params['marker_size'] = 10

            # 'all' is used to select all of the Norgate data types
            if params['data_types'] == 'all':
                chart_barometer = barometer

            # If the type is a string, remove all the other types
            elif isinstance(params['data_types'], str):
                chart_barometer = barometer
                for tick in list(params['graph_ticker_types'].values()):
                    if tick[0] != params['data_types']:
                        chart_barometer.drop(
                            index=chart_barometer[
                                chart_barometer['Ticker'].str.contains(
                                    tick)].index, inplace=True)

            # If the result is a list, remove all the types not in the list
            elif isinstance(params['data_types'], list):
                chart_barometer = barometer
                for tick in list(params['graph_ticker_types'].values()):
                    if tick[0] not in params['data_types']:
                        chart_barometer.drop(
                            index=chart_barometer[
                                chart_barometer['Ticker'].str.contains(
                                    tick)].index, inplace=True)

            # Print an error message if an incorrect type is supplied
            else:
                print('Enter a valid ticker type')

        # Otherwise for Yahoo SPX data
        else:
            params['sector_name'] = params[
                'equity_sector_levels'][params['sector_level']-1]
            params['marker_size'] = 10
            chart_barometer = barometer

        # Set label for Absolute trend strength ranging from 0% to 100%
        if params['absolute']:
            params['trend_type'] = 'Absolute Trend Strength %'
            params['axis_range'] = [-0.1,1]

        # Or splitting uptrends and downtrends ranging from -100% to 100%
        else:
            params['trend_type'] = 'Trend Strength %'
            params['axis_range'] = [-1,1]

        trend_sector_group = chart_barometer[
            [params['trend_type'], params['sector_name']]]

        # Set the maximum height of the chart
        params['plot_height'] = cls._set_height(
            params=params, chart_barometer=chart_barometer,
            trend_sector_group=trend_sector_group)

        # Rank the sector split by average  of the trend_type
        sect_data = trend_sector_group.groupby([params['sector_name']]).mean()
        params['sector_list'] = list(sect_data.sort_values(
            params['trend_type'], ascending=False).index)

        # Sort chart barometer by trend type
        chart_barometer = chart_barometer.sort_values(
            by=[params['trend_type']], ascending=True)

        return params, chart_barometer


    @staticmethod
    def _set_height(
        params: dict,
        chart_barometer: pd.DataFrame,
        trend_sector_group: pd.DataFrame) -> float:

        max_bucket = chart_barometer[params['trend_type']].value_counts().max()

        max_bucket_per_sector = trend_sector_group.groupby(
            trend_sector_group.columns.tolist()).size().max()

        num_sectors = len(chart_barometer[params['sector_name']].unique())

        if params['summary_type'] == 'strip':
            if num_sectors > 200:
                plot_height = max_bucket_per_sector * num_sectors / 5
            else:
                plot_height = max_bucket_per_sector * num_sectors / 20
        else:
            if params['dodge']:
                plot_height = max_bucket_per_sector * num_sectors / 8
            else:
                plot_height = max_bucket / 4

        return plot_height
