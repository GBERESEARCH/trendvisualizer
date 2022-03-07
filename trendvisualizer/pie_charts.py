"""
Display pie charts of trend strength

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager as fm


class PieCharts():
    """
    Summary and breakdown pie charts of trend strength

    """
    @staticmethod
    def pie_summary(params, barometer):
        """
        Plot pie charts for each of the 6 tenors: 10D, 20D, 30D, 50D, 100D
        and 200D for the chosen trend indicator.

        Parameters
        ----------
        params : Dict
            indicator_type : Str
                The indicator to plot. Choose from 'adx', 'ma_cross',
                'price_cross', 'rsi', 'breakout'.
        barometer : DataFrame
            DataFrame showing trend strength for each ticker.

        Returns
        -------
        Summary graph of 6 pie charts.

        """

        # Dictionary to store piechart parameters
        params['pie_params'] = {}

        # Set style
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(params['mpl_chart_params'])
        plt.tight_layout()

        # Extract the relevant column prefix from the dictionary of defaults
        params['pie_params']['indicator_type_ref'] = params[
            'indicator_name_dict'][params['indicator_type']][0]

        # Get the list of tenors
        params['pie_params']['indicator_tenors'] = params[
            params['indicator_type']+'_list']

        # Initialize the graph object
        fig, ax1 = plt.subplots(figsize=(10, 8))#, facecolor='mediumaquamarine')

        #plt.figure(facecolor='grey')

        # Loop through each tenor
        for num, tenor in enumerate(params['pie_params']['indicator_tenors']):

            # Naming convention for the moving average crossover differs as it
            # comes from a tuple of 2 tenors
            if params['indicator_type'] == 'ma_cross':
                params['pie_params']['indicator'] = (
                    params['pie_params']['indicator_type_ref']
                    +'_'
                    +str(tenor[0])
                    +'_'
                    +str(
                    tenor[1]))

            # The other names just take a single tenor
            else:
                params['pie_params']['indicator'] = (
                    params['pie_params']['indicator_type_ref']
                    +'_'
                    +str(tenor))

            # Calculate the proportion of the indicator that are long, short
            # or neutral across the whole range of assets
            params['pie_params']['long'] = (
                len(barometer[barometer[params['pie_params']['indicator']
                                        +'_flag']==1])
                / len(barometer))

            params['pie_params']['short'] = (
                len(barometer[barometer[params['pie_params']['indicator']
                                        +'_flag']==-1])
                / len(barometer))

            params['pie_params']['neutral'] = (
                len(barometer[barometer[params['pie_params']['indicator']
                                        +'_flag']==0])
                / len(barometer))

            # Find the right spot on the plot
            ax1 = plt.subplot(2, 3, num+1)
            params['pie_params']['labels'] = 'Long', 'Short', 'Neutral'
            #colors = 'wheat', 'lavender', 'lightblue'
            params['pie_params']['sizes'] = [
                params['pie_params']['long'] * 100,
                params['pie_params']['short'] * 100,
                params['pie_params']['neutral'] * 100
                ]

            # Set how much the pie slices are separated
            params['pie_params']['explode'] = (0.15, 0.15, 0.15)

            params['pie_params']['angle'] = (
                135 * params['pie_params']['sizes'][2] / 100)

            # Create the pie chart
            _, texts, autotexts = ax1.pie(
                params['pie_params']['sizes'],
                explode=params['pie_params']['explode'],
                labels=params['pie_params']['labels'],
                autopct='%1.1f%%',
                wedgeprops={'edgecolor':'black',
                            'linewidth':2,
                            'antialiased':True},
                textprops={'color':'black'},
                shadow=True,
                labeldistance=1.15,
                #rotatelabels=True,
                #colors=colors,
                startangle=params['pie_params']['angle'])

            # Reformat direction and percentage labels
            percprop = fm.FontProperties()
            dirprop = fm.FontProperties()
            percprop.set_size('medium')
            percprop.set_weight('bold')
            dirprop.set_size('small')
            plt.setp(autotexts, fontproperties=percprop)
            plt.setp(texts, fontproperties=dirprop)
            autotexts[0].set_color('red')
            autotexts[1].set_color('red')
            autotexts[2].set_color('red')

            # If the long and short slices are very small, shift the short text
            # to prevent overlapping
            if params['pie_params']['neutral'] > 0.97:
                long_x = texts[0]._x # pylint: disable=protected-access
                long_y = texts[0]._y # pylint: disable=protected-access
                texts[1]._x = long_x - 0.1 # pylint: disable=protected-access
                texts[1]._y = long_y - 0.1 # pylint: disable=protected-access

            # Ensures that pie is drawn as a circle.
            ax1.axis('equal')

            # Set the individual chart title
            ax1.set_title(
                str(tenor)
                +' day '
                +params['pie_params']['indicator_type_ref'].upper(),
                fontsize=12,
                y=1)

        # Create overall chart title label
        params['charttitle'] = (
            'Trend direction of '
            +params['indicator_name_dict'][params['indicator_type']][1]
            +' indicators'
            +' - '+params['end_date'])

        # Assign this to the figure
        fig.suptitle(params['charttitle'],
                     fontsize=20,
                     fontweight=0,
                     color='black',
                     style='italic',
                     y=1)

        return params


    @classmethod
    def pie_breakdown(cls, params, tables):
        """
        Chart showing the proportions of long, short and neutral signals for a
        given indicator and tenor and the breakdown of these by sector

        Parameters
        ----------
        params : Dict
            indicator_type : Str
                The indicator to plot. Choose from 'adx', 'ma_cross',
                'price_cross', 'rsi', 'breakout'.
            pie_tenor : Int / Tuple
                The time period of the indicator. For the Moving Average
                crossover this is a tuple from the following pairs: (5, 200),
                (10, 30), (10, 50), (20, 50), (30, 100), (50, 200). For the
                other indicators this is an integer from the list: 10, 20, 30,
                50, 100, 200.
            sector_level : Int, optional
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
        tables : Dict
            barometer : DataFrame
                DataFrame showing trend strength for each ticker.

        Returns
        -------
        Displays the chart.

        """

        # Set style
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(params['mpl_chart_params'])
        plt.tight_layout()

        # make figure and assign axis objects
        fig = plt.figure(figsize=(10, 5))
        gridspec = fig.add_gridspec(16, 3)
        ax1 = fig.add_subplot(gridspec[:, 0])
        ax2 = fig.add_subplot(gridspec[3:14, 1])
        ax3 = fig.add_subplot(gridspec[3:14, 2])

        # pie chart parameters
        params = cls._init_pie_params(
            params=params, barometer=tables['barometer'])

        _, ax1_texts, ax1_autotexts = ax1.pie(
            params['pie_params']['ratios'],
            explode=params['pie_params']['explode'],
            labels=params['pie_params']['labels'],
            autopct='%1.1f%%',
            wedgeprops={'edgecolor':'black',
                        'linewidth':2,
                        'antialiased':True},
            shadow=True,
            labeldistance=1.1,
            startangle=params['pie_params']['angle'])

        # Reformat direction and percentage labels
        percprop = fm.FontProperties()
        dirprop = fm.FontProperties()
        percprop.set_size(params['pie_params']['pie_perc_size'])
        percprop.set_weight('bold')
        dirprop.set_size('small')
        plt.setp(ax1_autotexts, fontproperties=percprop)
        plt.setp(ax1_texts, fontproperties=dirprop)
        ax1_autotexts[0].set_color(params['pie_params']['pie_perc_color'])
        ax1_autotexts[1].set_color(params['pie_params']['pie_perc_color'])
        ax1_autotexts[2].set_color(params['pie_params']['pie_perc_color'])

        # Set piechart title
        ax1.set_title('Market Direction Proportions', fontsize=10)

        # Set sector names when using Norgate futures data
        if params['asset_type'] == 'CTA':
            params['pie_params']['sector_name'] = params[
                'commodity_sector_levels'][params['sector_level']-1]

        # Otherwise for Yahoo SPX data
        else:
            params['pie_params']['sector_name'] = params[
                'equity_sector_levels'][params['sector_level']-1]

        # bar chart parameters
        params, tables = cls._sector_split(params, tables)

        # Create long breakdown
        ax2 = cls._breakdown(
            axx=ax2, params=params, direction='long', tables=tables)

        # Create short breakdown
        ax3 = cls._breakdown(
            axx=ax3, params=params, direction='short', tables=tables)

        # Create chart title label
        params['charttitle'] = (
            'Trend direction of '
            +str(params['pie_tenor'])
            +' day '
            +params['indicator_name_dict'][params['indicator_type']][1]
            +' - '+params['end_date'])

        # general title
        fig.suptitle(params['charttitle'],
                     fontsize=20,
                     fontweight=0,
                     color='black',
                     style='italic',
                     y=0.9)

        plt.show()

        return params, tables


    @staticmethod
    def _init_pie_params(params, barometer):

        # Dictionary to store piechart parameters
        params['pie_params'] = {}

        params['pie_params']['indicator_type_ref'] = params[
            'indicator_name_dict'][params['indicator_type']][0]

        if params['indicator_type'] == 'ma_cross':
            params['pie_params']['indicator'] = (
                params['pie_params']['indicator_type_ref']
                +'_'
                +str(params['pie_tenor'][0])
                +'_'
                +str(params['pie_tenor'][1]))
        else:
            params['pie_params']['indicator'] = (
                params['pie_params']['indicator_type_ref']
                +'_'
                +str(params['pie_tenor']))

        # Calculate the proportions that are long, short or neutral
        params['pie_params']['long'] = len(barometer[barometer[
            params['pie_params']['indicator']+'_flag']==1]) / len(barometer)
        params['pie_params']['short'] = len(barometer[barometer[
            params['pie_params']['indicator']+'_flag']==-1]) / len(barometer)
        params['pie_params']['neutral'] = len(barometer[barometer[
            params['pie_params']['indicator']+'_flag']==0]) / len(barometer)

        params['pie_params']['labels'] = 'Long', 'Short', 'Neutral'
        params['pie_params']['ratios'] = [params['pie_params']['long'],
                                          params['pie_params']['short'],
                                          params['pie_params']['neutral']]
        params['pie_params']['explode'] = (0.1, 0.1, 0.1)
        params['pie_params']['angle'] = 45

        params['pie_params']['pie_perc_color'] = 'red'
        params['pie_params']['bar_perc_color'] = 'black'
        params['pie_params']['pie_perc_size'] = 'medium'
        params['pie_params']['bar_perc_size'] = 'x-small'

        params['pie_params']['xpos'] = -0.2
        params['pie_params']['bottom'] = 0
        params['pie_params']['width'] = .2

        return params


    @staticmethod
    def _sector_split(params, tables):

        # Suppress SettingWithCopyWarning caused by slicing DataFrame
        pd.options.mode.chained_assignment = None

        tables['sector_split'] = pd.crosstab(
            index=tables['barometer'][params['pie_params']['sector_name']],
            columns=(tables['barometer'][
                params['pie_params']['indicator']+'_flag']),
            margins=True)

        tables['sector_split'] = tables['sector_split'].rename(
            columns={1:'long',
                     0:'neutral',
                     -1:'short'})

        for column in ['long', 'neutral', 'short']:
            if column not in tables['sector_split'].columns:
                tables['sector_split'][column] = np.zeros(
                    (len(tables['sector_split'])))

                tables['sector_split'][column][-1] = 1

        tables['sector_split']['long proportion'] = (
            tables['sector_split']['long']
            / tables['sector_split']['long'][-1])

        tables['sector_split']['neutral proportion'] = (
            tables['sector_split']['neutral']
            / tables['sector_split']['neutral'][-1])

        tables['sector_split']['short proportion'] = (
            tables['sector_split']['short']
            / tables['sector_split']['short'][-1])

        tables['non_zero_split_long'] = (
            tables['sector_split'][['long proportion']])

        tables['non_zero_split_long'] = (
            tables['non_zero_split_long'].loc[
                (tables['non_zero_split_long']!=0).any(1)])

        params['pie_params']['ratios_long'] = list(
            tables['non_zero_split_long']['long proportion'][:-1])

        tables['non_zero_split_short'] = (
            tables['sector_split'][['short proportion']])

        tables['non_zero_split_short'] = (
            tables['non_zero_split_short'].loc[
                (tables['non_zero_split_short']!=0).any(1)])

        params['pie_params']['ratios_short'] = list(
            tables['non_zero_split_short']['short proportion'][:-1])

        # Suppress SettingWithCopyWarning caused by slicing DataFrame
        pd.options.mode.chained_assignment = "warn"

        return params, tables


    @staticmethod
    def _breakdown(axx, params, tables, direction):

        ratios = params['pie_params']['ratios_'+direction]
        for j, _ in enumerate(ratios):
            height = ratios[j]
            axx.bar(params['pie_params']['xpos'],
                    height=height,
                    width=params['pie_params']['width'],
                    edgecolor='black',
                    bottom=params['pie_params']['bottom'])

            params['pie_params']['ypos'] = params[
                'pie_params']['bottom'] + axx.patches[j].get_height() / 2
            params['pie_params']['bottom'] += height
            axx.text(params['pie_params']['xpos'],
                     params['pie_params']['ypos'],
                     "%d%%" % (axx.patches[j].get_height() * 100),
                     ha='center',
                     va='center',
                     color=params['pie_params']['bar_perc_color'],
                     fontsize=params['pie_params']['bar_perc_size'])

        axx.set_title('Sector Breakdown '+direction.title(), fontsize=10)
        axx.legend((list(
            tables['non_zero_split_'+direction].index[:-1])),
            bbox_to_anchor= (0.5, 1),
            fontsize=6)
        axx.axis('off')
        axx.set_xlim(- 2.5 * params['pie_params']['width'],
                     2.5 * params['pie_params']['width'])

        return axx
