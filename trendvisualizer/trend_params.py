"""
Default trend strength parameters

"""

# Dictionary containing all the default parameters
trend_params_dict = {
    'df_params':{
        'ma_list':[5, 10, 20, 30, 50, 100, 200],
        'macd_params':[12, 26, 9],
        'adx_list':[10, 20, 30, 50, 100, 200],
        'ma_cross_list':[(5, 200), (10, 30), (10, 50), (20, 50), (30, 100),
                         (50, 200)],
        'price_cross_list':[10, 20, 30, 50, 100, 200],
        'rsi_list':[10, 20, 30, 50, 100, 200],
        'breakout_list':[10, 20, 30, 50, 100, 200],
        'atr_list':[14],
        'trend_flags':[
            'MA_5_200_flag',
            'PX_MA_10_flag',
            'ADX_10_flag',
            'RSI_10_flag',
            'breakout_10_flag',
            'MA_10_30_flag',
            'MACD_flag',
            'MA_10_50_flag',
            'PX_MA_20_flag',
            'MA_20_50_flag',
            'ADX_20_flag',
            'RSI_20_flag',
            'breakout_20_flag',
            'PX_MA_30_flag',
            'ADX_30_flag',
            'RSI_30_flag',
            'breakout_30_flag',
            'MA_30_100_flag',
            'PX_MA_50_flag',
            'MA_50_200_flag',
            'ADX_50_flag',
            'RSI_50_flag',
            'breakout_50_flag',
            'PX_MA_100_flag',
            'ADX_100_flag',
            'RSI_100_flag',
            'breakout_100_flag',
            'PX_MA_200_flag',
            'ADX_200_flag',
            'RSI_200_flag',
            'breakout_200_flag'
            ],
        'mpl_line_params':{
            'figure.dpi':100,
            'axes.edgecolor':'black',
            'axes.titlepad':15,
            'axes.xmargin':0.05,
            'axes.ymargin':0.05,
            'axes.linewidth':2,
            'axes.facecolor':(0.8, 0.8, 0.9, 0.5),
            'xtick.major.pad':10,
            'ytick.major.pad':10,
            'lines.linewidth':3.0,
            'grid.color':'black',
            'grid.linestyle':':',
            'legend.frameon':True,
            'legend.framealpha':1,
            'legend.shadow':True,
            'legend.facecolor':'white',
            'legend.edgecolor':'black',
            'legend.title_fontsize':15,
            'legend.fontsize':10,
            },

        'mpl_bar_params':{
            'figure.dpi':100,
            'axes.edgecolor':'black',
            'axes.titlepad':15,
            'axes.xmargin':0.05,
            'axes.ymargin':0.05,
            'axes.linewidth':2,
            'axes.facecolor':(0.8, 0.8, 0.9, 0.5),
            'xtick.major.pad':10,
            'ytick.major.pad':10,
            'lines.linewidth':3.0,
            'grid.color':'black',
            'grid.linestyle':':'
            },

        'mpl_chart_params':{
            'figure.dpi':100,
            'axes.edgecolor':'black',
            'axes.titlepad':5,
            'axes.xmargin':0.05,
            'axes.ymargin':0.05,
            'axes.linewidth':0.5,
            'axes.facecolor':(0.8, 0.8, 0.9, 0.3),
            'xtick.major.pad':1,
            'ytick.major.pad':1,
            'lines.linewidth':2.0,
            'grid.color':'black',
            'grid.linestyle':':'
            },

        'mpl_summary_params':{
            'figure.dpi':100,
            'axes.edgecolor':'black',
            'axes.titlepad':15,
            'axes.titlesize':18,
            'axes.titley':1.02,
            'axes.xmargin':0.05,
            'axes.ymargin':0.05,
            'axes.linewidth':2,
            'axes.facecolor':(0.8, 0.8, 0.9, 0.5),
            #'legend.facecolor':(0.8, 0.8, 0.9, 0.5),
            'legend.facecolor':'white',
            'legend.edgecolor':'black',
            'legend.title_fontsize':10,
            'legend.fontsize':8,
            'legend.shadow':True,
            'legend.frameon':True,
            'xtick.major.pad':10,
            'xtick.major.size':12,
            'xtick.minor.size':8,
            'xtick.labelsize':12,
            'ytick.major.pad':10,
            'ytick.major.size':12,
            'ytick.minor.size':8,
            'ytick.labelsize':12,
            'lines.linewidth':3.0,
            'grid.color':'black',
            'grid.linestyle':':'
            },
        'window':None,
        'mkts':10,
        'chart_mkts':None,
        'trend':'strong',
        'days':60,
        'norm':True,
        'chart_dimensions':(8, 5),
        'lookback':500,
        'ticker_limit':None,
        'market_chart':False,
        'indicator_name_dict':{
            'adx':('ADX', 'ADX'),
            'ma_cross':('MA', 'MA Crossover'),
            'price_cross':('PX_MA', 'Price MA Crossover'),
            'rsi':('RSI', 'RSI'),
            'breakout':('breakout', 'Breakout')
            },
        'indicator_type':'adx',
        'asset_type':'CTA',
        'commodity_sector_levels':[
            'Asset Class',
            'Broad Sector',
            'Mid Sector',
            'Narrow Sector',
            'Underlying'
            ],
        'equity_sector_levels':[
            'Sector',
            'Industry Group',
            'Industry',
            'Sub-Industry',
            'Security'
            ],
        'ticker_types':{
            '&':'c_', # continuous future
            '#':'r_', # ratio
            '@':'s_', # spot cash commodity
            '$':'i_', # index
            '%':'y_'  # yield
            },

        'top_trend_params':{
            'initial_size':50,
            'max_per_sector':5,
            'final_size':20
            },

        'sector_level':2,
        'absolute':True,
        'summary_type':'swarm',
        'graph_ticker_types':['c', 's'],
        'dodge':False,
        'compact':False,
        'marker':'^',
        'violin':False,
        'source':'norgate',
        'tickers_adjusted':False,
        'tickers':None,
        'data_output':False,
        'start_date':None,
        'end_date':None,
        'pie_tenor':50,
        'data_types':'all'
        }
    }
