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
         'grid.linestyle':':',
         'legend.frameon':True,
         'legend.framealpha':1,
         'legend.shadow':True,
         'legend.facecolor':'white',
         'legend.edgecolor':'black',
         'legend.title_fontsize':15,
         'legend.fontsize':10,         
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
     
     'df_mpl_summary_params':{
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
     
     'df_lookback':500,
     'df_ticker_limit':None,
     'df_mkts':10,
     'df_trend':'strong',
     'df_days':60,
     'df_norm':True,
     'df_market_chart':False, 
     'df_chart_dimensions':(8, 5),
    
     'df_commodity_sector_levels':
         ['Asset Class', 
          'Broad Sector', 
          'Mid Sector', 
          'Narrow Sector',
          'Underlying'],
    
     'df_equity_sector_levels':[
         'Sector', 
         'Industry Group', 
         'Industry', 
         'Sub-Industry', 
         'Security'],   
     
     'df_ticker_types':{
         '&':'c_', # continuous future 
         '#':'r_', # ratio
         '@':'s_', # spot cash commodity
         '$':'i_', # index
         '%':'y_'  # yield
         },
    
     'df_sector_mappings':{
         '&6A_CCB':('Currencies', 'G10 Currencies', 'G10 Currencies', 'G10 Currencies', 'AUD'), # AUD
         '&6B_CCB':('Currencies', 'G10 Currencies', 'G10 Currencies', 'G10 Currencies', 'GBP'), # GBP
         '&6C_CCB':('Currencies', 'G10 Currencies', 'G10 Currencies', 'G10 Currencies', 'CAD'), # CAD
         '&6E_CCB':('Currencies', 'G10 Currencies', 'G10 Currencies', 'G10 Currencies', 'EUR'), # EUR
         '&6J_CCB':('Currencies', 'G10 Currencies', 'G10 Currencies', 'G10 Currencies', 'JPY'), # JPY
         '&6M_CCB':('Currencies', 'EM Currencies', 'EM Currencies', 'EM Currencies', 'MXN'), # MXN
         '&6N_CCB':('Currencies', 'G10 Currencies', 'G10 Currencies', 'G10 Currencies', 'NZD'), # NZD
         '&6S_CCB':('Currencies', 'G10 Currencies', 'G10 Currencies', 'G10 Currencies', 'CHF'), # CHF
         '&AFB_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Eastern Australia Feed Barley'), # Eastern Australia Feed Barley
         '&AWM_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Eastern Australia Wheat'), # Eastern Australia Wheat
         '&BAX_CCB':('Interest Rates', 'Interest Rates', 'Interest Rates', 'Interest Rates', 'Canadian Bankers Acceptance'), # Canadian Bankers Acceptance
         '&BRN_CCB':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'Brent Crude Oil'), # Brent Crude Oil
         '&BTC_CCB':('Currencies', 'Crypto Currencies', 'Crypto Currencies', 'Crypto Currencies', 'Bitcoin'), # Bitcoin 
         '&CC_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'Cocoa'), # Cocoa 
         '&CGB_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Canadian 10y'), # Canadian 10 Yr Govt Bond 
         '&CL_CCB':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'Crude Oil - Light Sweet'), # Crude Oil - Light Sweet
         '&CT_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'Cotton #2'), # Cotton #2
         '&DC_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'Milk - Class III'), # Milk - Class III
         '&DX_CCB':('Currencies', 'G10 Currencies', 'G10 Currencies', 'G10 Currencies', 'Benchmark'), # US Dollar Index
         '&EH_CCB':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'Ethanol'), # Ethanol
         '&EMD_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'S&P MidCap 400 E-mini'), # S&P MidCap 400 E-mini
         '&ES_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'S&P 500 E-mini'), # S&P 500 E-mini
         '&EUA_CCB':('Commodities', 'Energy', 'Energy', 'Energy', 'EUA (Carbon Emissions)'), # EUA (Carbon Emissions)
         '&FBTP_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Euro-BTP Long Term'), # Euro-BTP Long Term
         '&FCE_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'CAC 40'), # CAC 40
         '&FDAX_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'DAX'), # DAX
         '&FDAX9_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'DAX'), # DAX, Last in Close field
         '&FESX_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'EURO STOXX 50'), # EURO STOXX 50
         '&FESX9_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'EURO STOXX 50'), # EURO STOXX 50, Last in Close field
         '&FGBL_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Euro-Bund - 10 Yr'), # Euro-Bund - 10 Yr
         '&FGBM_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Euro-Bobl - 5 Yr'), # Euro-Bobl - 5 Yr
         '&FGBS_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Euro-Schatz - 2 Yr'), # Euro-Schatz - 2 Yr
         '&FGBX_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Euro-Buxl - 30 Yr'), # Euro-Buxl - 30 Yr
         '&FSMI_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'Swiss Market Index'), # Swiss Market Index
         '&FTDX_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'TecDAX'), # TecDAX
         '&GAS_CCB':('Commodities', 'Energy', 'Energy', 'Energy', 'Gas Oil'), # Gas Oil
         '&GC_CCB':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Gold'), # Gold
         '&GD_CCB':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # GS&P GSCI
         '&GE_CCB':('Interest Rates', 'Interest Rates', 'Interest Rates', 'Interest Rates', 'Eurodollar'), # Eurodollar
         '&GF_CCB':('Commodities','Diversified Agriculture', 'Livestock', 'Livestock', 'Feeder Cattle'), # Feeder Cattle    
         '&GWM_CCB':('Commodities', 'Energy', 'Energy', 'Energy', 'UK Natural Gas'), # UK Natural Gas
         '&HE_CCB':('Commodities','Diversified Agriculture', 'Livestock', 'Livestock', 'Lean Hogs'), # Lean Hogs    
         '&HG_CCB':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Copper'), # Copper    
         '&HO_CCB':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'NY Harbor ULSD'), # NY Harbor ULSD
         '&HSI_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'Hang Seng Index'), # Hang Seng Index
         '&HTW_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'MSCI Taiwan Index'), # MSCI Taiwan Index      
         '&KC_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'Coffee C'), # Coffee C
         '&KE_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'KC HRW Wheat'), # KC HRW Wheat
         '&KOS_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'KOSPI 200'), # KOSPI 200
         '&LBS_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'Lumber'), # Lumber
         '&LCC_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'London Cocoa'), # London Cocoa
         '&LE_CCB':('Commodities','Diversified Agriculture', 'Livestock', 'Livestock', 'Live Cattle'), # Live Cattle
         '&LES_CCB':('Interest Rates', 'Interest Rates', 'Interest Rates', 'Interest Rates', 'Euro Swiss'), # Euro Swiss
         '&LEU_CCB':('Interest Rates', 'Interest Rates', 'Interest Rates', 'Interest Rates', 'Euribor'), # Euribor
         '&LEU9_CCB':('Interest Rates', 'Interest Rates', 'Interest Rates', 'Interest Rates', 'Euribor'), # Euribor, Official Close
         '&LFT_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'FTSE 100'), # FTSE 100
         '&LFT9_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'FTSE 100'), # FTSE 100, Official Close
         '&LLG_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Long Gilt'), # Long Gilt
         '&LRC_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'Robusta Coffee'), # Robusta Coffee
         '&LSS_CCB':('Interest Rates', 'Interest Rates', 'Interest Rates', 'Interest Rates', 'Short Sterling'), # Short Sterling
         '&LSU_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'White Sugar'), # White Sugar
         '&LWB_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Feed Wheat'), # Feed Wheat
         '&MHI_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'Hang Seng Index'), # Hang Seng Index - Mini
         '&MWE_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Hard Red Spring Wheat'), # Hard Red Spring Wheat
         '&NG_CCB':('Commodities', 'Energy', 'Energy', 'Energy', 'Henry Hub Natural Gas'), # Henry Hub Natural Gas
         '&NIY_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'Nikkei 225'), # Nikkei 225 Yen    
         '&NKD_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'Nikkei 225'), # Nikkei 225 Dollar
         '&NQ_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'Nasdaq-100 - E-mini'), # Nasdaq-100 - E-mini
         '&OJ_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'Frozen Concentrated Orange Juice'), # Frozen Concentrated Orange Juice
         '&PA_CCB':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Palladium'), # Palladium
         '&PL_CCB':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Platinum'), # Platinum
         '&RB_CCB':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'RBOB Gasoline'), # RBOB Gasoline
         '&RS_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Canola'), # Canola
         '&RTY_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'Russell 2000 - E-mini'), # Russell 2000 - E-mini
         '&SB_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'Sugar No. 11'), # Sugar No. 11
         '&SCN_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'FTSE China A50 Index'), # FTSE China A50 Index
         '&SI_CCB':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Silver'), # Silver
         '&SIN_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'SGX Nifty 50 Index'), # SGX Nifty 50 Index
         '&SJB_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Japanese Govt Bond - Mini'), # Japanese Govt Bond - Mini
         '&SNK_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'Nikkei 225'), # Nikkei 225 (SGX)
         '&SP_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'S&P 500'), # S&P 500
         '&SSG_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'MSCI Singapore Index'), # MSCI Singapore Index
         '&STW_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'MSCI Taiwan Index'), # MSCI Taiwan Index, Discontinued
         '&SXF_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'S&P/TSX 60 Index'), # S&P/TSX 60 Index
         '&TN_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Ultra 10 Year U.S. T-Note'), # Ultra 10 Year U.S. T-Note
         '&UB_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'Ultra U.S. T-Bond'), # Ultra U.S. T-Bond
         '&VX_CCB':('Volatility', 'Volatility', 'Volatility', 'Volatility', 'Cboe Volatility Index'), # Cboe Volatility Index    
         '&WBS_CCB':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'WTI Crude Oil'), # WTI Crude Oil
         '&YAP_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'ASX SPI 200'), # ASX SPI 200
         '&YAP4_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'ASX SPI 200'), # ASX SPI 200, Day
         '&YAP10_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'ASX SPI 200'), # ASX SPI 200, Night
         '&YG_CCB':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Gold - Mini'), # Gold - Mini
         '&YI_CCB':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Silver - Mini'), # Silver - Mini
         '&YIB_CCB':('Interest Rates', 'Interest Rates', 'Interest Rates', 'Interest Rates', 'ASX 30 Day Interbank Cash Rate'), # ASX 30 Day Interbank Cash Rate
         '&YIR_CCB':('Interest Rates', 'Interest Rates', 'Interest Rates', 'Interest Rates', 'ASX 90 Day Bank Accepted Bills'), # ASX 90 Day Bank Accepted Bills
         '&YM_CCB':('Equity Indices', 'Equity Indices','Equity Indices','Equity Indices', 'E-mini Dow'), # E-mini Dow
         '&YXT_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'ASX 10 Year Treasury Bond'), # ASX 10 Year Treasury Bond
         '&YYT_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'ASX 3 Year Treasury Bond'), # ASX 3 Year Treasury Bond
         '&ZB_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', 'U.S. T-Bond'), # U.S. T-Bond
         '&ZC_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Corn'), # Corn
         '&ZF_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', '5-Year US T-Note'), # 5-Year US T-Note
         '&ZG_CCB':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Gold'), # Gold 100oz, Discountinued
         '&ZI_CCB':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Silver'), # Silver 5000oz, Discontinued
         '&ZL_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Soybean Oil'), # Soybean Oil
         '&ZM_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Soybean Meal'), # Soybean Meal
         '&ZN_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', '10-Year US T-Note'), # 10-Year US T-Note    
         '&ZO_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Oats'), # Oats
         '&ZQ_CCB':('Interest Rates', 'Interest Rates', 'Interest Rates', 'Interest Rates', '30 Day Federal Funds'), # 30 Day Federal Funds
         '&ZR_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Rough Rice'), # Rough Rice
         '&ZS_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Soybeans'), # Soybeans    
         '&ZT_CCB':('Bonds','Government Bonds','Government Bonds','Government Bonds', '2-Year US T-Note'), # 2-Year US T-Note    
         '&ZW_CCB':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Chicago SRW Wheat'), # Chicago SRW Wheat
         '#GSR':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Benchmark'), # Gold/Silver Ratio
         '$BCOM':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # Bloomberg Commodity Index
         '$BCOMAG':('Commodities','Diversified Agriculture', 'Agriculture', 'Agriculture', 'Benchmark'), # Bloomberg Agriculture Sub-Index
         '$BCOMEN':('Commodities', 'Energy', 'Energy', 'Energy', 'Benchmark'), # Bloomberg Energy Sub-Index
         '$BCOMGR':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Benchmark'), # Bloomberg Grains Sub-Index
         '$BCOMIN':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Benchmark'), # Bloomberg Industrial Metals Sub-Index
         '$BCOMLI':('Commodities','Diversified Agriculture', 'Livestock', 'Livestock', 'Benchmark'), # Bloomberg Livestock Sub-Index
         '$BCOMPE':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'Benchmark') , # Bloomberg Petroleum Sub-Index
         '$BCOMPR':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Benchmark'), # Bloomberg Precious Metals Sub-Index
         '$BCOMSO':('Commodities','Diversified Agriculture', 'Agriculture', 'Softs', 'Benchmark'), # Bloomberg Softs Sub-Index
         '$BCOMTR':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # Bloomberg Commodity Total Return Index
         '$BCOMXE':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # Bloomberg Ex-Energy Sub-Index
         '$CRB':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # Refinitiv/CoreCommodity CRB Index
         '$FC':('Commodities','Diversified Agriculture', 'Livestock', 'Livestock', 'Feeder Cattle'), # CME Feeder Cattle Index
         '$LH':('Commodities','Diversified Agriculture', 'Livestock', 'Livestock', 'Lean Hogs'), # CME Lean Hogs Index
         '$LMEX':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Benchmark'), # LMEX Index
         '$RBABCA':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # RBA Bulk Commodities Sub-Index (AUD)
         '$RBABCU':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # RBA Bulk Commodities Sub-Index (USD)
         '$RBABMA':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Benchmark'), # RBA Base Metals Sub-Index (AUD)
         '$RBABMU':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Benchmark'), # RBA Base Metals Sub-Index (USD)
         '$RBACPA':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # RBA Commodity Prices Index (AUD)
         '$RBACPU':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # RBA Commodity Prices Index (USD)
         '$RBANRCPA':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # RBA Non-Rural Commodity Prices Sub-Index (AUD)
         '$RBANRCPU':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # RBA Non-Rural Commodity Prices Sub-Index (USD)
         '$RBARCPA':('Commodities', 'Diversified Agriculture', 'Diversified Agriculture', 'Diversified Agriculture', 'Benchmark'), # RBA Rural Commodity Prices Sub-Index (AUD)
         '$RBARCPU':('Commodities', 'Diversified Agriculture', 'Diversified Agriculture', 'Diversified Agriculture', 'Benchmark'), # RBA Rural Commodity Prices Sub-Index (USD)
         '$SPGSCI':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # S&P GSCI Spot Index
         '$SPGSCITR':('Commodities', 'Commodities', 'Commodities', 'Commodities', 'Benchmark'), # S&P GSCI Total Return Index
         '@AA':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium Alloy - LME Official Cash
         '@AA03S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium Alloy - LME 03 Months Seller
         '@AAWS':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium Alloy - LME Warehouse Opening Stocks
         '@AL':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium - LME Official Cash
         '@AL03S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium - LME 03 Months Seller
         '@ALAUD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium - LME Official Cash (AUD)
         '@ALCAD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium - LME Official Cash (CAD)
         '@ALWS':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium - LME Warehouse Opening Stocks
         '@BFOE':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'Crude Oil'), # Brent Crude Europe FOB Spot
         '@C2Y':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Corn'), # Corn #2 Yellow Central Illinois Average Price Spot
         '@CO':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Cobalt'), # Cobalt - LME Official Cash
         '@CO03S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Cobalt'), # Cobalt - LME 03 Months Seller
         '@CO15S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Cobalt'), # Cobalt - LME 15 Months Seller
         '@COWS':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Cobalt'), # Cobalt - LME Warehouse Opening Stocks
         '@CU':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Copper'), # Copper - LME Official Cash
         '@CU03S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Copper'), # Copper - LME 03 Months Seller
         '@CUAUD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Copper'), # Copper - LME Official Cash (AUD)
         '@CUCAD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Copper'), # Copper - LME Official Cash (CAD)
         '@CUWS':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Copper'), # Copper - LME Warehouse Opening Stocks
         '@FE':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Iron Ore'), # Iron Ore CFR China 62% Fe Spot
         '@FEAUD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Iron Ore'), # Iron Ore CFR China 62% Fe Spot (AUD)
         '@FECAD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Iron Ore'), # Iron Ore CFR China 62% Fe Spot (CAD)
         '@GC':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Gold'), # Gold - London PM Fix
         '@HHNG':('Commodities', 'Energy', 'Energy', 'Energy', 'Natural Gas'), # Henry Hub Natural Gas Spot
         '@HO':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'Heating Oil'), # Heating Oil Spot
         '@NA':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium Alloy (NASAAC) - LME Official Cash
         '@NA03S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium Alloy (NASAAC) - LME 03 Months Seller
         '@NAWS':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Aluminium'), # Aluminium Alloy (NASAAC) - LME Warehouse Opening Stocks
         '@NI':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Nickel'), # Nickel - LME Official Cash
         '@NI03S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Nickel'), # Nickel - LME 03 Months Seller
         '@NIAUD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Nickel'), # Nickel - LME Official Cash (AUD)
         '@NICAD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Nickel'), # Nickel - LME Official Cash (CAD)
         '@NIWS':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Nickel'), # Nickel - LME Warehouse Opening Stocks
         '@PA':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Palladium'), # Palladium - London PM Fix
         '@PAAUD':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Palladium'), # Palladium - London PM Fix (AUD)
         '@PACAD':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Palladium'), # Palladium - London PM Fix (CAD)
         '@PB':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Lead'), # Lead - LME Official Cash
         '@PB03S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Lead'), # Lead - LME 03 Months Seller
         '@PBAUD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Lead'), # Lead - LME Official Cash (AUD)
         '@PBCAD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Lead'), # Lead - LME Official Cash (CAD)
         '@PBWS':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Lead'), # Lead - LME Warehouse Opening Stocks
         '@PL':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Platinum'), # Platinum - London PM Fix
         '@PLAUD':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Platinum'), # Platinum - London PM Fix (AUD)
         '@PLCAD':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Platinum'), # Platinum - London PM Fix (CAD)
         '@RBOB':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'RBOB Gasoline'), # RBOB Gasoline Spot
         '@S1Y':('Commodities','Diversified Agriculture', 'Agriculture', 'Grains', 'Soybeans'), # Soybeans #1 Yellow Central Illinois Average Price Spot
         '@SI':('Commodities', 'Metals', 'Precious Metals', 'Precious Metals', 'Silver'), # Silver - London Fix
         '@SN':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Tin'), # Tin - LME Official Cash
         '@SN03S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Tin'), # Tin - LME 03 Months Seller
         '@SN15S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Tin'), # Tin - LME 15 Months Seller
         '@SNAUD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Tin'), # Tin - LME Official Cash (AUD)
         '@SNCAD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Tin'), # Tin - LME Official Cash (CAD)
         '@SNWS':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Tin'), # Tin - LME Warehouse Opening Stocks
         '@U3O8':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Uranium'), # Uranium Spot
         '@U3O8AUD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Uranium'), # Uranium Spot (AUD)
         '@U3O8CAD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Uranium'), # Uranium Spot (CAD)
         '@WTI':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'Crude Oil'), # West Texas Intermediate Crude Oil Spot
         '@WTIAUD':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'Crude Oil'), # West Texas Intermediate Crude Oil Spot (AUD)
         '@WTICAD':('Commodities', 'Energy', 'Petroleum', 'Petroleum', 'Crude Oil'), # West Texas Intermediate Crude Oil Spot (CAD)
         '@YCX':('Commodities', 'Energy', 'Energy', 'Energy', 'Thermal Coal'), # Thermal Coal Spot
         '@YCXAUD':('Commodities', 'Energy', 'Energy', 'Energy', 'Thermal Coal'), # Thermal Coal Spot (AUD)
         '@YCXCAD':('Commodities', 'Energy', 'Energy', 'Energy', 'Thermal Coal'), # Thermal Coal Spot (CAD)
         '@ZN':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Zinc'), # Zinc - LME Official Cash
         '@ZN03S':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Zinc'), # Zinc - LME 03 Months Seller
         '@ZNAUD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Zinc'), # Zinc - LME Official Cash (AUD)
         '@ZNCAD':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Zinc'), # Zinc - LME Official Cash (CAD)
         '@ZNWS':('Commodities', 'Metals', 'Industrial Metals', 'Industrial Metals', 'Zinc'), # Zinc - LME Warehouse Opening Stocks
         },
     
     'df_equity_sectors':{
         'Oil & Gas Drilling':('Energy','Energy','Energy Equipment & Services'),
         'Oil & Gas Equipment & Services':('Energy','Energy','Energy Equipment & Services'),
         'Integrated Oil & Gas':('Energy','Energy','Oil, Gas & Consumable Fuels'),
         'Oil & Gas Exploration & Production':('Energy','Energy','Oil, Gas & Consumable Fuels'),
         'Oil & Gas Refining & Marketing':('Energy','Energy','Oil, Gas & Consumable Fuels'),
         'Oil & Gas Storage & Transportation':('Energy','Energy','Oil, Gas & Consumable Fuels'),
         'Coal & Consumable Fuels':('Energy','Energy','Oil, Gas & Consumable Fuels'),
         'Commodity Chemicals':('Materials','Materials','Chemicals'),
         'Diversified Chemicals':('Materials','Materials','Chemicals'),
         'Fertilizers & Agricultural Chemicals':('Materials','Materials','Chemicals'),
         'Industrial Gases':('Materials','Materials','Chemicals'),
         'Specialty Chemicals':('Materials','Materials','Chemicals'),
         'Construction Materials':('Materials','Materials','Construction Materials'),
         'Metal & Glass Containers':('Materials','Materials','Containers & Packaging'),
         'Paper Packaging':('Materials','Materials','Containers & Packaging'),
         'Aluminum':('Materials','Materials','Metals & Mining'),
         'Diversified Metals & Mining':('Materials','Materials','Metals & Mining'),
         'Copper':('Materials','Materials','Metals & Mining'),
         'Gold':('Materials','Materials','Metals & Mining'),
         'Precious Metals & Minerals':('Materials','Materials','Metals & Mining'),
         'Silver':('Materials','Materials','Metals & Mining'),
         'Steel':('Materials','Materials','Metals & Mining'),
         'Forest Products':('Materials','Materials','Paper & Forest Products'),
         'Paper Products':('Materials','Materials','Paper & Forest Products'),
         'Aerospace & Defense':('Industrials','Capital Goods','Aerospace & Defense'),
         'Building Products':('Industrials','Capital Goods','Building Products'),
         'Construction & Engineering':('Industrials','Capital Goods','Construction & Engineering'),
         'Electrical Components & Equipment':('Industrials','Capital Goods','Electrical Equipment'),
         'Heavy Electrical Equipment':('Industrials','Capital Goods','Electrical Equipment'),
         'Industrial Conglomerates':('Industrials','Capital Goods','Industrial Conglomerates'),
         'Construction Machinery & Heavy Trucks':('Industrials','Capital Goods','Machinery'),
         'Agricultural & Farm Machinery':('Industrials','Capital Goods','Machinery'),
         'Industrial Machinery':('Industrials','Capital Goods','Machinery'),
         'Trading Companies & Distributors':('Industrials','Capital Goods','Trading Companies & Distributors'),
         'Commercial Printing':('Industrials','Commercial & Professional Services','Commercial Services & Supplies'),
         'Environmental & Facilities Services':('Industrials','Commercial & Professional Services','Commercial Services & Supplies'),
         'Office Services & Supplies':('Industrials','Commercial & Professional Services','Commercial Services & Supplies'),
         'Diversified Support Services':('Industrials','Commercial & Professional Services','Commercial Services & Supplies'),
         'Security & Alarm Services':('Industrials','Commercial & Professional Services','Commercial Services & Supplies'),
         'Human Resource & Employment Services':('Industrials','Commercial & Professional Services','Professional Services'),
         'Research & Consulting Services':('Industrials','Commercial & Professional Services','Professional Services'),
         'Air Freight & Logistics':('Industrials','Transportation','Air Freight & Logistics'),
         'Airlines':('Industrials','Transportation','Airlines'),
         'Marine':('Industrials','Transportation','Marine'),
         'Railroads':('Industrials','Transportation','Road & Rail'),
         'Trucking':('Industrials','Transportation','Road & Rail'),
         'Airport Services':('Industrials','Transportation','Transportation Infrastructure'),
         'Highways & Railtracks':('Industrials','Transportation','Transportation Infrastructure'),
         'Marine Ports & Services':('Industrials','Transportation','Transportation Infrastructure'),
         'Auto Parts & Equipment':('Consumer Discretionary','Automobiles & Components','Auto Components'),
         'Tires & Rubber':('Consumer Discretionary','Automobiles & Components','Auto Components'),
         'Automobile Manufacturers':('Consumer Discretionary','Automobiles & Components','Automobiles'),
         'Motorcycle Manufacturers':('Consumer Discretionary','Automobiles & Components','Automobiles'),
         'Consumer Electronics':('Consumer Discretionary','Consumer Durables & Apparel','Household Durables'),
         'Home Furnishings':('Consumer Discretionary','Consumer Durables & Apparel','Household Durables'),
         'Homebuilding':('Consumer Discretionary','Consumer Durables & Apparel','Household Durables'),
         'Household Appliances':('Consumer Discretionary','Consumer Durables & Apparel','Household Durables'),
         'Housewares & Specialties':('Consumer Discretionary','Consumer Durables & Apparel','Household Durables'),
         'Leisure Products':('Consumer Discretionary','Consumer Durables & Apparel','Leisure Products'),
         'Apparel, Accessories & Luxury Goods':('Consumer Discretionary','Consumer Durables & Apparel','Textiles, Apparel & Luxury Goods'),
         'Footwear':('Consumer Discretionary','Consumer Durables & Apparel','Textiles, Apparel & Luxury Goods'),
         'Textiles':('Consumer Discretionary','Consumer Durables & Apparel','Textiles, Apparel & Luxury Goods'),
         'Casinos & Gaming':('Consumer Discretionary','Consumer Services','Hotels, Restaurants & Leisure'),
         'Hotels, Resorts & Cruise Lines':('Consumer Discretionary','Consumer Services','Hotels, Restaurants & Leisure'),
         'Leisure Facilities':('Consumer Discretionary','Consumer Services','Hotels, Restaurants & Leisure'),
         'Restaurants':('Consumer Discretionary','Consumer Services','Hotels, Restaurants & Leisure'),
         'Education Services':('Consumer Discretionary','Consumer Services','Diversified Consumer Services'),
         'Specialized Consumer Services':('Consumer Discretionary','Consumer Services','Diversified Consumer Services'),
         'Distributors':('Consumer Discretionary','Retailing','Distributors'),
         'Internet & Direct Marketing Retail':('Consumer Discretionary','Retailing','Internet & Direct Marketing Retail'),
         'Department Stores':('Consumer Discretionary','Retailing','Multiline Retail'),
         'General Merchandise Stores':('Consumer Discretionary','Retailing','Multiline Retail'),
         'Apparel Retail':('Consumer Discretionary','Retailing','Specialty Retail'),
         'Computer & Electronics Retail':('Consumer Discretionary','Retailing','Specialty Retail'),
         'Home Improvement Retail':('Consumer Discretionary','Retailing','Specialty Retail'),
         'Specialty Stores':('Consumer Discretionary','Retailing','Specialty Retail'),
         'Automotive Retail':('Consumer Discretionary','Retailing','Specialty Retail'),
         'Homefurnishing Retail':('Consumer Discretionary','Retailing','Specialty Retail'),
         'Drug Retail':('Consumer Staples','Food & Staples Retailing','Food & Staples Retailing'),
         'Food Distributors':('Consumer Staples','Food & Staples Retailing','Food & Staples Retailing'),
         'Food Retail':('Consumer Staples','Food & Staples Retailing','Food & Staples Retailing'),
         'Hypermarkets & Super Centers':('Consumer Staples','Food & Staples Retailing','Food & Staples Retailing'),
         'Brewers':('Consumer Staples','Food, Beverage & Tobacco','Beverages'),
         'Distillers & Vintners':('Consumer Staples','Food, Beverage & Tobacco','Beverages'),
         'Soft Drinks':('Consumer Staples','Food, Beverage & Tobacco','Beverages'),
         'Agricultural Products':('Consumer Staples','Food, Beverage & Tobacco','Food Products'),
         'Packaged Foods & Meats':('Consumer Staples','Food, Beverage & Tobacco','Food Products'),
         'Tobacco':('Consumer Staples','Food, Beverage & Tobacco','Tobacco'),
         'Household Products':('Consumer Staples','Household & Personal Products','Household Products'),
         'Personal Products':('Consumer Staples','Household & Personal Products','Personal Products'),
         'Health Care Equipment':('Health Care','Health Care Equipment & Services','Health Care Equipment & Supplies'),
         'Health Care Supplies':('Health Care','Health Care Equipment & Services','Health Care Equipment & Supplies'),
         'Health Care Distributors':('Health Care','Health Care Equipment & Services','Health Care Providers & Services'),
         'Health Care Services':('Health Care','Health Care Equipment & Services','Health Care Providers & Services'),
         'Health Care Facilities':('Health Care','Health Care Equipment & Services','Health Care Providers & Services'),
         'Managed Health Care':('Health Care','Health Care Equipment & Services','Health Care Providers & Services'),
         'Health Care Technology':('Health Care','Health Care Equipment & Services','Health Care Technology'),
         'Biotechnology':('Health Care','Pharmaceuticals, Biotechnology & Life Sciences','Biotechnology'),
         'Pharmaceuticals':('Health Care','Pharmaceuticals, Biotechnology & Life Sciences','Pharmaceuticals'),
         'Life Sciences Tools & Services':('Health Care','Pharmaceuticals, Biotechnology & Life Sciences','Life Sciences Tools & Services'),
         'Diversified Banks':('Financials','Banks','Banks'),
         'Regional Banks':('Financials','Banks','Banks'),
         'Thrifts & Mortgage Finance':('Financials','Banks','Thrifts & Mortgage Finance'),
         'Other Diversified Financial Services':('Financials','Diversified Financials','Diversified Financial Services'),
         'Multi-Sector Holdings':('Financials','Diversified Financials','Diversified Financial Services'),
         'Specialized Finance':('Financials','Diversified Financials','Diversified Financial Services'),
         'Consumer Finance':('Financials','Diversified Financials','Consumer Finance'),
         'Asset Management & Custody Banks':('Financials','Diversified Financials','Capital Markets'),
         'Investment Banking & Brokerage':('Financials','Diversified Financials','Capital Markets'),
         'Diversified Capital Markets':('Financials','Diversified Financials','Capital Markets'),
         'Financial Exchanges & Data':('Financials','Diversified Financials','Capital Markets'),
         'Mortgage REITs':('Financials','Diversified Financials','Mortgage Real Estate Investment Trusts (REITs)'),
         'Insurance Brokers':('Financials','Insurance','Insurance'),
         'Life & Health Insurance':('Financials','Insurance','Insurance'),
         'Multi-line Insurance':('Financials','Insurance','Insurance'),
         'Property & Casualty Insurance':('Financials','Insurance','Insurance'),
         'Reinsurance':('Financials','Insurance','Insurance'),
         'IT Consulting & Other Services':('Information Technology','Software & Services','IT Services'),
         'Data Processing & Outsourced Services':('Information Technology','Software & Services','IT Services'),
         'Internet Services & Infrastructure':('Information Technology','Software & Services','IT Services'),
         'Application Software':('Information Technology','Software & Services','Software'),
         'Systems Software':('Information Technology','Software & Services','Software'),
         'Communications Equipment':('Information Technology','Technology Hardware & Equipment','Communications Equipment'),
         'Technology Hardware, Storage & Peripherals':('Information Technology','Technology Hardware & Equipment','Technology Hardware, Storage & Peripherals'),
         'Electronic Equipment & Instruments':('Information Technology','Technology Hardware & Equipment','Electronic Equipment, Instruments & Components'),
         'Electronic Components':('Information Technology','Technology Hardware & Equipment','Electronic Equipment, Instruments & Components'),
         'Electronic Manufacturing Services':('Information Technology','Technology Hardware & Equipment','Electronic Equipment, Instruments & Components'),
         'Technology Distributors':('Information Technology','Technology Hardware & Equipment','Electronic Equipment, Instruments & Components'),
         'Semiconductor Equipment':('Information Technology','Semiconductors & Semiconductor Equipment','Semiconductors & Semiconductor Equipment'),
         'Semiconductors':('Information Technology','Semiconductors & Semiconductor Equipment','Semiconductors & Semiconductor Equipment'),
         'Alternative Carriers':('Communication Services','Communication Services','Diversified Telecommunication Services'),
         'Integrated Telecommunication Services':('Communication Services','Communication Services','Diversified Telecommunication Services'),
         'Wireless Telecommunication Services':('Communication Services','Communication Services','Wireless Telecommunication Services'),
         'Advertising':('Communication Services','Media & Entertainment','Media'),
         'Broadcasting':('Communication Services','Media & Entertainment','Media'),
         'Cable & Satellite':('Communication Services','Media & Entertainment','Media'),
         'Publishing':('Communication Services','Media & Entertainment','Media'),
         'Movies & Entertainment':('Communication Services','Media & Entertainment','Entertainment'),
         'Interactive Home Entertainment':('Communication Services','Media & Entertainment','Entertainment'),
         'Interactive Media & Services':('Communication Services','Media & Entertainment','Interactive Media & Services'),
         'Electric Utilities':('Utilities','Utilities','Electric Utilities'),
         'Gas Utilities':('Utilities','Utilities','Gas Utilities'),
         'Multi-Utilities':('Utilities','Utilities','Multi-Utilities'),
         'Water Utilities':('Utilities','Utilities','Water Utilities'),
         'Independent Power Producers & Energy Traders':('Utilities','Utilities','Independent Power and Renewable Electricity Producers'),
         'Renewable Electricity':('Utilities','Utilities','Independent Power and Renewable Electricity Producers'),
         'Diversified REITs':('Real Estate','Real Estate','Equity Real Estate Investment Trusts (REITs)'),
         'Industrial REITs':('Real Estate','Real Estate','Equity Real Estate Investment Trusts (REITs)'),
         'Hotel & Resort REITs':('Real Estate','Real Estate','Equity Real Estate Investment Trusts (REITs)'),
         'Office REITs':('Real Estate','Real Estate','Equity Real Estate Investment Trusts (REITs)'),
         'Health Care REITs':('Real Estate','Real Estate','Equity Real Estate Investment Trusts (REITs)'),
         'Residential REITs':('Real Estate','Real Estate','Equity Real Estate Investment Trusts (REITs)'),
         'Retail REITs':('Real Estate','Real Estate','Equity Real Estate Investment Trusts (REITs)'),
         'Specialized REITs':('Real Estate','Real Estate','Equity Real Estate Investment Trusts (REITs)'),
         'Diversified Real Estate Activities':('Real Estate','Real Estate','Real Estate Management & Development'),
         'Real Estate Operating Companies':('Real Estate','Real Estate','Real Estate Management & Development'),
         'Real Estate Development':('Real Estate','Real Estate','Real Estate Management & Development'),
         'Real Estate Services':('Real Estate','Real Estate','Real Estate Management & Development'),
         }
     }
