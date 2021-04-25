# Dictionary containing all the default parameters
trend_params_dict = {
    # lists of parameters for each of the trend flags calculated 
    # in fields function
    'df_ma_list':[10, 20, 30, 50, 100, 200],
    'df_macd_params':[12, 26, 9],
    'df_adx_list':[10, 20, 30, 50, 100, 200],
    'df_ma_cross_list':[(10, 30), (20, 50), (50, 200)],
    'df_price_cross_list':[10, 20, 30, 50, 100, 200],
    'df_rsi_list':[10, 20, 30, 50, 100, 200],
    'df_atr_list':[14],
    
     # list of the individual trend flag lists
     'df_trend_flag_list':[
         'df_ma_list', 
         'df_macd_params', 
         'df_adx_list', 
         'df_ma_cross_list', 
         'df_price_cross_list', 
         'df_rsi_list', 
         'df_atr_list'
         ],
    
     # list of default trend flags to be used if no alternatives 
     # are supplied
     'df_trend_flags_basic':[
         'MA_10_30',
         'MACD_flag',               
         'PX_MA_20',
         'MA_20_50',
         'ADX_20_flag',
         'PX_MA_50',
         'MA_50_200',
         'ADX_50_flag',
         'PX_MA_200',
         'ADX_200_flag'
         ],
     
     'df_trend_flags':[
         'PX_MA_10',
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
         ],
     
     # Parameters to overwrite mpl_style defaults
     'df_mpl_line_params':{
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
     
     'df_mpl_bar_params':{
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
     
     'df_mpl_chart_params':{
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
     
     'df_lookback':500,
     'df_ticker_limit':None,
     'df_mkts':5,
     'df_trend':'strong',
     'df_days':60,
     'df_norm':True,
     'df_market_chart':False, 
     'df_chart_dimensions':(8, 5),
     
     'df_comm_tickers':[
         '&6A_CCB', # AUD
         '&6B_CCB', # GBP
         '&6C_CCB', # CAD
         '&6E_CCB', # EUR
         '&6J_CCB', # JPY
         '&6M_CCB', # MXN
         '&6N_CCB', # NZD
         '&6S_CCB', # CHF
         '&AFB_CCB', # Eastern Australia Feed Barley
         '&AWM_CCB', # Eastern Australia Wheat
         #'&BAX_CCB', # Canadian Bankers Acceptance
         '&BRN_CCB', # Brent Crude Oil
         '&BTC_CCB', # Bitcoin 
         '&CC_CCB', # Cocoa 
         '&CGB_CCB', # Canadian 10 Yr Govt Bond 
         '&CL_CCB', # Crude Oil - Light Sweet
         '&CT_CCB', # Cotton #2
         '&DC_CCB', # Milk - Class III
         #'&DX_CCB', # US Dollar Index
         '&EH_CCB', # Ethanol
         '&EMD_CCB', # S&P MidCap 400 E-mini
         '&ES_CCB', # S&P 500 E-mini
         '&FBTP_CCB', # Euro-BTP Long Term
         '&FCE_CCB', # CAC 40
         '&FDAX_CCB', # DAX
         '&FESX_CCB', # EURO STOXX 50
         '&FGBL_CCB', # Euro-Bund - 10 Yr
         '&FGBM_CCB', # Euro-Bobl - 5 Yr
         '&FGBS_CCB', # Euro-Schatz - 2 Yr
         '&FGBX_CCB', # Euro-Buxl - 30 Yr
         '&FSMI_CCB', # Swiss Market Index
         '&FTDX_CCB', # TecDAX
         '&GAS_CCB', # Gas Oil
         '&GC_CCB', # Gold
         '&GD_CCB', # GS&P GSCI
         #'&GE_CCB', # Eurodollar
         '&GF_CCB', # Feeder Cattle    
         '&HE_CCB', # Lean Hogs    
         '&HG_CCB', # Copper    
         '&HO_CCB', # NY Harbor ULSD     
         '&HSI_CCB', # Hang Seng Index     
         '&KC_CCB', # Coffee C
         '&KE_CCB', # KC HRW Wheat
         '&KOS_CCB', # KOSPI 200
         '&LBS_CCB', # Lumber
         '&LCC_CCB', # London Cocoa
         '&LE_CCB', # Live Cattle
         #'&LES_CCB', # Euro Swiss
         #'&LEU_CCB', # Euribor
         '&LFT_CCB', # FTSE 100
         '&LLG_CCB', # Long Gilt
         '&LRC_CCB', # Robusta Coffee
         #'&LSS_CCB', # Short Sterling
         '&LSU_CCB', # White Sugar
         '&LWB_CCB', # Feed Wheat
         '&MHI_CCB', # Hang Seng Index - Mini
         '&MWE_CCB', # Hard Red Spring Wheat
         '&NG_CCB', # Henry Hub Natural Gas
         '&NIY_CCB', # Nikkei 225 Dollar    
         '&NKD_CCB', # Nikkei 225 Dollar
         '&NQ_CCB', # Nasdaq-100 - E-mini
         '&OJ_CCB', # Frozen Concentrated Orange Juice
         '&PA_CCB', # Palladium
         '&PL_CCB', # Platinum
         '&RB_CCB', # RBOB Gasoline
         '&RS_CCB', # Canola
         '&RTY_CCB', # Russell 2000 - E-mini
         '&SB_CCB', # Sugar No. 11
         '&SCN_CCB', # FTSE China A50 Index
         '&SI_CCB', # Silver
         '&SIN_CCB', # SGX Nifty 50 Index
         '&SJB_CCB', # Japanese Govt Bond - Mini
         '&SNK_CCB', # Nikkei 225 (SGX)
         '&SP_CCB', # S&P 500
         '&SSG_CCB', # MSCI Singapore Index
         ##*'&STW_CCB', # MSCI Taiwan Index
         '&SXF_CCB', # S&P/TSX 60 Index
         '&TN_CCB', # Ultra 10 Year U.S. T-Note
         '&UB_CCB', # Ultra U.S. T-Bond
         '&VX_CCB', # Cboe Volatility Index    
         '&WBS_CCB', # WTI Crude Oil
         '&YAP_CCB', # ASX SPI 200
         '&YG_CCB', # Gold - Mini
         '&YI_CCB', # Silver - Mini
         #'&YIB_CCB', # ASX 30 Day Interbank Cash Rate
         #'&YIR_CCB', # ASX 30 Day Interbank Cash Rate
         '&YM_CCB', # E-mini Dow
         #'&YXT_CCB', # ASX 10 Year Treasury Bond
         #'&YYT_CCB', # ASX 3 Year Treasury Bond
         '&ZB_CCB', # U.S. T-Bond
         '&ZC_CCB', # Corn
         '&ZF_CCB', # 5-Year US T-Note
         ##*'&ZG_CCB', # Gold 100oz
         ##*'&ZI_CCB', # Silver 5000oz
         '&ZL_CCB', # Soybean Oil
         '&ZM_CCB', # Soybean Meal
         '&ZN_CCB', # 10-Year US T-Note    
         '&ZO_CCB', # Oats
         #'&ZQ_CCB', # 30 Day Federal Funds
         '&ZR_CCB', # Rough Rice
         '&ZS_CCB', # Soybeans    
         '&ZT_CCB', # 2-Year US T-Note    
         '&ZW_CCB' # Chicago SRW Wheat
         ]
     }
