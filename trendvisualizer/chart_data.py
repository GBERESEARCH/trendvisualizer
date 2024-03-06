import numpy as np
import pandas as pd
import collections
from trendvisualizer.chart_prep import Formatting

class Data():
    """
    Create data dictionaries to display various charts of Trend Strength

    """
    @staticmethod
    def bar_data(barometer: pd.DataFrame, mkts: int=20) -> dict:
        """
        Create data dictionary for plotting barchart trends

        Parameters
        ----------
        barometer : DataFrame
            DataFrame showing trend strength for each ticker.
        mkts : Int
            Number of markets to chart. The default is 20.

        Returns
        -------
        bar_dict : TYPE
            DESCRIPTION.

        """
        bar_dict = collections.defaultdict(dict)

        # Create entries for up trend
        barometer_up = barometer.sort_values(
            by=['Trend Strength %'], ascending=True)
        bar_dict['up']['short_name'] = list(
            barometer_up['Short_name'].iloc[-mkts:])
        bar_dict['up']['trend_strength'] = np.array(
            barometer_up['Trend Strength %'].iloc[-mkts:])
        bar_dict['up']['trend_color'] = list(
            barometer_up['Trend Color'].iloc[-mkts:])
        bar_dict['up']['titlestr'] = 'Up'

        # Create entries for down trend
        barometer_down = barometer.sort_values(
            by=['Trend Strength %'], ascending=False)
        bar_dict['down']['short_name'] = list(
            barometer_down['Short_name'].iloc[-mkts:])
        bar_dict['down']['trend_strength'] = np.array(
            barometer_down['Trend Strength %'].iloc[-mkts:])
        bar_dict['down']['trend_color'] = list(
            barometer_down['Trend Color'].iloc[-mkts:])
        bar_dict['down']['titlestr'] = 'Down'

        # Create entries for neutral trend
        barometer_neutral = barometer.sort_values(
            by=['Absolute Trend Strength %'], ascending=True)
        bar_dict['neutral']['short_name'] = list(
            barometer_neutral['Short_name'].iloc[:mkts])
        bar_dict['neutral']['trend_strength'] = np.array(
            barometer_neutral['Trend Strength %'].iloc[:mkts])
        bar_dict['neutral']['trend_color'] = list(
            barometer_neutral['Trend Color'].iloc[:mkts])
        bar_dict['neutral']['titlestr'] = 'Neutral'

        # Create entries for strong trend
        bar_dict['strongly']['short_name'] = list(
            barometer_neutral['Short_name'].iloc[-mkts:])
        bar_dict['strongly']['trend_strength'] = np.array(
            barometer_neutral['Trend Strength %'].iloc[-mkts:])
        bar_dict['strongly']['trend_color'] = list(
            barometer_neutral['Trend Color'].iloc[-mkts:])
        bar_dict['strongly']['titlestr'] = 'Strongly'

        bar_dict = dict(bar_dict)

        return bar_dict
    

    @staticmethod
    def returns_data(params: dict, tables: dict) -> dict:        
        """
        Create data dictionary for plotting line graph trends

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
        returns_dict : Dict
            Dictionary of data to create a line graph of normalised price history.

        """
        # Generate DataFrame of normalized returns
        tenor = Formatting.create_normalized_data(params=params, tables=tables)

        # Create empty returns dict & add returns and labels
        returns_dict = {}
        returns_dict['time_series'] = tenor.to_dict()
        returns_dict['xlabel'] = 'Date'
        returns_dict['ylabel'] = 'Return %'
        returns_dict['line_labels'] = tenor.columns.to_list()
        returns_dict['titlestr'] = (
            'Relative Return Over Last ' +
            str(len(tenor)) +
            ' Trading Days' +
            ' - ' +
            params['end_date']
            )

        return returns_dict