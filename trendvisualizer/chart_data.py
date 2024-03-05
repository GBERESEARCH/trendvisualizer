import numpy as np
import pandas as pd
import collections

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
    
