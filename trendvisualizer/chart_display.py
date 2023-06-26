"""
Display various charts of Trend Strength

"""
import warnings
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import axes, cm
from matplotlib.dates import MO, WeekdayLocator, MonthLocator
from matplotlib.ticker import MaxNLocator, AutoMinorLocator, PercentFormatter
from trendvisualizer.chart_prep import Formatting


class Graphs():
    """
    Barchart, Line Graph, Summary Charts,Piecharts displaying trend strength
    of various markets

    """
    @classmethod
    def trendbarchart(
        cls,
        params: dict,
        barometer: pd.DataFrame) -> None:
        """
        Create a barchart of the most or least trending markets.

        Parameters
        ----------
        params : Dict
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
        barometer : DataFrame
            DataFrame showing trend strength for each ticker.

        Returns
        -------
        Returns barchart of trend strength for selected markets / trend type.

        """

        # Initialize the figure
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(params['mpl_bar_params'])
        num_markets = min(params['mkts'], 20)
        _, ax1 = plt.subplots(figsize=(6,int(num_markets/3)))
        plt.tight_layout()

        # Set the xticks to be integer values
        ax1.xaxis.set_major_locator(MaxNLocator(6))#integer=True))

        # Set the x axis to be in percentages
        ax1.xaxis.set_major_formatter(PercentFormatter(1))

        # Set the spacing between y axis and labels
        ax1.yaxis.set_tick_params(pad=15)

        # Set axis tick label size
        font_scaler = min(int(0.6 * (50 - params['mkts'])), 12)
        ax1.tick_params(axis='both', which='both', labelsize=font_scaler)

        # Set the yticks to be horizontal
        plt.yticks(rotation=0)

        # If the trend flag is set to 'up', show the markets with
        # greatest up trend indication
        if params['trend'] == 'up':
            ax1, titlestr = cls._bar_up(
                ax1=ax1, params=params, barometer=barometer)

        # If the trend flag is set to 'down', show the markets with
        # greatest down trend indication
        elif params['trend'] == 'down':
            ax1, titlestr = cls._bar_down(
                ax1=ax1, params=params, barometer=barometer)

        # If the trend flag is set to 'neutral', show the markets with
        # lowest trend indication
        elif params['trend'] == 'neutral':
            ax1, titlestr = cls._bar_neutral(
                ax1=ax1, params=params, barometer=barometer)

        # If the trend flag is set to 'strong', show the markets with
        # greatest trend indication both up and down
        elif params['trend'] == 'strong':
            ax1, titlestr = cls._bar_strong(
                ax1=ax1, params=params, barometer=barometer)

        # Label xaxis
        plt.xlabel("Trend Strength", fontsize=font_scaler*1.2, labelpad=10)

        # Set title
        plt.suptitle(titlestr+' Trending Markets'+' - '+params['end_date'],
                     fontsize=18,
                     fontweight=0,
                     color='black',
                     style='italic',
                     y=1.04)

        plt.show()


    @staticmethod
    def _bar_up(
        ax1: axes.Axes,
        params: dict,
        barometer: pd.DataFrame) -> tuple[axes.Axes, str]:

        # Set the x-axis range
        ax1.set_xlim(left=0, right=1)

        # Sort by Trend Strength
        barometer = barometer.sort_values(
            by=['Trend Strength %'], ascending=True)

        plt.barh(barometer['Short_name'][-params['mkts']:],
                 barometer['Trend Strength %'][-params['mkts']:],
                 color=list(barometer['Trend Color'][-params['mkts']:]))
        titlestr = 'Up'

        return ax1, titlestr


    @staticmethod
    def _bar_down(
        ax1: axes.Axes,
        params: dict,
        barometer: pd.DataFrame) -> tuple[axes.Axes, str]:

        # Set the x-axis range
        ax1.set_xlim(left=-1, right=0)

        # Sort by Trend Strength
        barometer = barometer.sort_values(
            by=['Trend Strength %'], ascending=False)

        plt.barh(barometer['Short_name'][-params['mkts']:],
                 barometer['Trend Strength %'][-params['mkts']:],
                 color=list(barometer['Trend Color'][-params['mkts']:]))
        titlestr = 'Down'

        return ax1, titlestr


    @staticmethod
    def _bar_neutral(
        ax1: axes.Axes,
        params: dict,
        barometer: pd.DataFrame) -> tuple[axes.Axes, str]:

        # Set the x-axis range
        ax1.set_xlim(left=-1, right=1)

        # Sort by Absolute Trend Strength
        barometer = barometer.sort_values(
            by=['Absolute Trend Strength %'], ascending=True)

        plt.barh(barometer['Short_name'][:params['mkts']],
                 barometer['Trend Strength %'][:params['mkts']],
                 color=list(barometer['Trend Color'][:params['mkts']]),
                 #height=0.5,
                 )
        titlestr = 'Neutral'

        return ax1, titlestr


    @staticmethod
    def _bar_strong(
        ax1: axes.Axes,
        params: dict,
        barometer: pd.DataFrame) -> tuple[axes.Axes, str]:

        # Set the x-axis range
        ax1.set_xlim(left=-1, right=1)

        # Sort by Absolute Trend Strength
        barometer = barometer.sort_values(
            by=['Absolute Trend Strength %'], ascending=True)

        plt.barh(barometer['Short_name'][-params['mkts']:],
                 barometer['Trend Strength %'][-params['mkts']:],
                 color=list(barometer['Trend Color'][-params['mkts']:]))
        titlestr = 'Strongly'

        return ax1, titlestr


    @classmethod
    def returnsgraph(
        cls,
        params: dict,
        tables: dict) -> None:
        """
        Create a line graph of normalised price history

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
        Line graph of closing prices for each ticker in tenor.

        """

        tenor = Formatting.normdata(params=params, tables=tables)

        # Initialize the figure
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(params['mpl_line_params'])
        plt.tight_layout()
        _, ax1 = plt.subplots(figsize=(16,8))

        # Plot the lineplot
        ax1.plot(tenor)

        # axis formatting
        ax1 = cls._returns_ticks(ax1, tenor)

        # Set x axis range
        ax1.set_xlim(min(tenor.index), max(tenor.index))

        # Shift label to avoid overlapping tick marks
        ax1.yaxis.labelpad = 40
        ax1.xaxis.labelpad = 20

        # Set a horizontal line at 100
        ax1.axhline(y=100, linewidth=1, color='k')

        # Set x and y labels and title
        ax1.set_xlabel('Date', fontsize=18)
        ax1.set_ylabel('Return %', fontsize=18, rotation=0)

        # Set the legend
        upper_anchor = 1.15 + params['mkts']/250
        #plt.legend(loc='upper left', labels=tenor.columns)
        plt.legend(
            bbox_to_anchor=(0.5, upper_anchor), #1.21), #-0.4,1), #1.05, 1),
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
        dynamic_y = 1.05 + params['mkts']/500
        plt.suptitle('Relative Return Over Last '
                     +str(len(tenor))+' Trading Days'+' - '+params['end_date'],
                     fontsize=25,
                     fontweight=0,
                     color='black',
                     style='italic',
                     y=dynamic_y) #1.08) #0.98)

        plt.show()


    @staticmethod
    def _returns_ticks(
        ax1: axes.Axes,
        tenor: pd.DataFrame) -> axes.Axes:

        # create a variable to choose interval between xticks based on
        # length of history
        week_scaler = int(round(len(tenor) / 30))
        month_scaler = int(round(len(tenor) / 120))

        # Set major xticks as every 4th Monday or monthly at a specified
        # interval
        scale_week_tick = WeekdayLocator(byweekday=MO, interval=week_scaler)
        scale_month_tick = MonthLocator(interval=month_scaler)

        # Set axis format as DD-MMM-YYYY or MMM-YYYY
        days_fmt = mdates.DateFormatter('%d-%b-%Y')
        months_fmt = mdates.DateFormatter('%b-%Y')

        # If less than 90 days history use day format and locate major
        # xticks on 4th Monday
        if len(tenor) < 90:
            ax1.xaxis.set_major_formatter(days_fmt)
            ax1.xaxis.set_major_locator(scale_week_tick)

        # Otherwise use month format and locate major xticks at monthly
        # (or greater) intervals
        else:
            ax1.xaxis.set_major_formatter(months_fmt)
            ax1.xaxis.set_major_locator(scale_month_tick)

        # Set minor xticks to be 4 within each major xtick
        minor_tick = AutoMinorLocator(4)
        ax1.xaxis.set_minor_locator(minor_tick)

        # Set size of ticks
        ax1.tick_params(which='both', width=1)
        ax1.tick_params(which='major', length=8)
        ax1.tick_params(which='minor', length=4)

        # Set prices to the right as we are concerned with the current
        # level
        ax1.yaxis.set_major_locator(MaxNLocator(11))
        ax1.yaxis.set_label_position('right')
        ax1.yaxis.tick_right()

        # Set ytick labels
        yticklabels = (
            int(round(tenor.min().min(), -1)),
            100 - int((abs(100 - round(tenor.min().min(), -1))) / 2),
            100,
            100 + int((abs(100 - round(tenor.max().max(), -1))) / 2),
            int(round(tenor.max().max(), -1)))

        ax1.set_yticks(yticklabels)

        return ax1


    @classmethod
    def marketchart(
        cls,
        params: dict,
        tables: dict) -> dict:
        """
        Create a chart showing the top and bottom 20 trending markets.

        Parameters
        ----------
        params : Dict
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
        tables : Dict
            Dictionary of key tables.

        Returns
        -------
        Returns chart of multiple markets.

        """

        # If a mkts parameter has been specified then create a tuple of chart
        # dimensions
        if params['chart_mkts'] is not None:
            params = Formatting.mkt_dims(params)

        params['num_charts'] = int(
            params['chart_dimensions'][0] * params['chart_dimensions'][1])

        data_list = Formatting.datalist(
            params=params, barometer=tables['barometer'], market_chart=True,
            num_charts=params['num_charts'])

        # Set style
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(params['mpl_chart_params'])

        # create a color palette
        palette = cm.get_cmap('tab20')

        # Initialize the figure
        fig, ax1 = plt.subplots(figsize=(int(params['chart_dimensions'][1]*3),
                                        int(params['chart_dimensions'][0]*2)))
        fig.subplots_adjust(top=0.85)
        fig.tight_layout()

        # multiple line plot
        num=0
        for ticker in data_list:
            num += 1
            if num < 21:
                colr = num
            else:
                colr = num - 20

            label = params['ticker_short_name_dict'][ticker]

            # Find the right spot on the plot
            ax1 = plt.subplot(
                params['chart_dimensions'][0],
                params['chart_dimensions'][1],
                num)

            # Plot the lineplot
            # Pandas error regarding multi indexing requires converting axes to
            # numpy arrays
            axis_dates = np.array(
                tables['ticker_dict'][ticker].index[-params['days']:])
            if params['norm']:
                axis_prices = np.array(
                    tables['ticker_dict'][ticker]['Close'][-params['days']:]
                    .div(tables['ticker_dict'][ticker]['Close'][
                        -params['days']:].iloc[0])
                    .mul(100))

            else:
                axis_prices = np.array(
                    tables['ticker_dict'][ticker]['Close'][-params['days']:])

            ax1.plot(axis_dates,
                    axis_prices,
                    marker='',
                    color=palette(colr),
                    linewidth=1.9,
                    alpha=0.9,
                    label=label)

            # xticks only on bottom graphs
            if num in range(
                    params['num_charts'] - params['chart_dimensions'][1] + 1):
                plt.tick_params(labelbottom=False)

            # Add title
            plt.title(label,
                      loc='left',
                      fontsize=10,
                      fontweight=0,
                      color='black' )

            # axis formatting
            ax1 = cls._market_ticks(ax1, params)

            # Set xtick labels at 70 degrees
            plt.xticks(rotation=70)

        # Create chart title label
        params['charttitle'] = Formatting.get_charttitle(params=params)

        # general title
        fig.suptitle(params['charttitle'],
                     fontsize=20,
                     fontweight=0,
                     color='black',
                     style='italic',
                     y=1.05)

        return params


    @staticmethod
    def _market_ticks(
        ax1: axes.Axes,
        params: dict) -> axes.Axes:

        # create a variable to choose interval between xticks based
        # on length of history
        week_scaler = int(round(params['days'] / 30))
        month_scaler = int(round(params['days'] / 120))

        # Set major xticks as every 4th Monday or monthly at a
        # specified interval
        scale_week_tick = WeekdayLocator(byweekday=MO,
                                         interval=week_scaler)
        scale_month_tick = MonthLocator(interval=month_scaler)

        # Set axis format as DD-MMM-YYYY or MMM-YYYY
        days_fmt = mdates.DateFormatter('%d-%b-%Y')
        months_fmt = mdates.DateFormatter('%b-%Y')

        # If less than 90 days history use day format and locate
        # major xticks on 4th Monday
        if params['days'] < 90:
            ax1.xaxis.set_major_formatter(days_fmt)
            ax1.xaxis.set_major_locator(scale_week_tick)

        # Otherwise use month format and locate major xticks at
        # monthly (or greater) intervals
        else:
            ax1.xaxis.set_major_formatter(months_fmt)
            ax1.xaxis.set_major_locator(scale_month_tick)

        # Set minor xticks to be 4 within each major xtick
        minor_tick = AutoMinorLocator(4)
        ax1.xaxis.set_minor_locator(minor_tick)

        # Set size of ticks
        ax1.tick_params(which='both', width=0.5, labelsize=8)
        ax1.tick_params(which='major', length=2)
        ax1.tick_params(which='minor', length=1)

        # Set prices to the right as we are concerned with the
        # current level
        ax1.yaxis.set_label_position('right')
        ax1.yaxis.tick_right()

        return ax1


    @classmethod
    def summaryplot(
        cls,
        params: dict,
        tables: dict) -> tuple[dict, dict]:
        """
        Plot a summary of the strength of trend across markets

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
                Whether to show absolute trend strength (from 0 - 100%) or
                show positive and negative trends seperately

            summary_type : Str, optional
                The type of chart to display. The default is Swarmplot.

            graph_ticker_types : Str or List
                Ticker types to use. Choose from 'c': continuous futures,
                'r':ratios, 's':spot cash commodities, 'i':indices, 'y':yields.
                The default is ['c', 's']

            violin : Bool
                Whether to show a violin plot on the strip plot

        tables : Dict
            Dictionary of key tables.

        Returns
        -------
        Seaborn Swarmplot  / Stripplot of the data.

        """
        # Suppress userwarning warnings caused by overlapping data
        warnings.filterwarnings("ignore", category=UserWarning)

        # Configure sector name, marker size, trend type and drop rows from
        # barometer DataFrame as appropriate
        params, tables['chart_barometer'] = Formatting.summary_config(
                params=params, barometer=tables['barometer'])

        # sns.set_style("darkgrid", {"axes.edgecolor": "black"})
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update(params['mpl_summary_params'])

        if params['compact']:
            params['plot_height'] = params['plot_height'] / 4

        # Create Seaborn swarm plot
        if params['summary_type'] == 'swarm':
            _, ax1 = plt.subplots(figsize=(8, params['plot_height']))

            ax1 = cls._create_swarm(ax1=ax1, params=params, tables=tables)

        # Create Seaborn strip plot
        if params['summary_type'] == 'strip':
            _, ax1 = plt.subplots(figsize=(8, params['plot_height']))

            ax1 = cls._create_strip(ax1=ax1, params=params, tables=tables)

        # Return warnings to default setting
        warnings.filterwarnings("default", category=UserWarning)

        return params, tables


    @staticmethod
    def _create_swarm(
        ax1: axes.Axes,
        params: dict,
        tables: dict) -> axes.Axes:

        ax1 = sns.swarmplot(data=tables['chart_barometer'],
                            x=params['trend_type'],
                            y="Trend",
                            hue=params['sector_name'],
                            hue_order=params['sector_list'],
                            dodge=params['dodge'],
                            palette='cubehelix',
                            marker=params['marker'],
                            s=params['marker_size']
                           )

        ax1.set(ylabel="")
        ax1.set_xlabel(params['trend_type'], fontsize=12)
        ax1.xaxis.set_major_formatter(PercentFormatter(1))
        ax1.set_xlim(params['axis_range'])
        ax1.tick_params(axis='both', which='major', labelsize=12)
        ax1.set_title('Trend Strength by Sector'
                      +' - '
                      +params['end_date'],
                      fontsize=18, y=1)
        ax1.legend(bbox_to_anchor= (1.1, 1),
                  title_fontsize=10,
                  fontsize=8,
                  title='Sector',
                  shadow=True,
                  frameon=True,
                  facecolor='white')

        return ax1


    @staticmethod
    def _create_strip(
        ax1: axes.Axes,
        params: dict,
        tables: dict) -> axes.Axes:

        if params['violin']:
            ax1 = sns.violinplot(x=params['trend_type'],
                                y=params['sector_name'],
                                data=tables['chart_barometer'],
                                inner='quartile',
                                #color=".8",
                                linewidth=1,
                                palette="coolwarm",
                                scale='count')
        ax1 = sns.stripplot(x=params['trend_type'],
                           y=params['sector_name'],
                           data=tables['chart_barometer'],
                           dodge=True,
                           alpha=0.5,
                           jitter=0.2,
                           order=params['sector_list'],
                           marker=params['marker'],
                           palette='viridis',
                           s=params['marker_size'])

        ax1.set_title('Trend Strength by Sector'
                      +' - '
                      +params['end_date'],
                      fontsize=18, y=1)
        ax1.xaxis.set_major_formatter(PercentFormatter(1))
        ax1.set_xlim(params['axis_range'])
        ax1.tick_params(axis='both', which='major', labelsize=12)
        ax1.tick_params(axis='both', which='minor', labelsize=12)
        ax1.set(ylabel="")
        ax1.set_xlabel(params['trend_type'], fontsize=12)

        return ax1
