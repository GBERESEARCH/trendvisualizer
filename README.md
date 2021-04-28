# trendvisualizer
## Visualize trend strength across various markets.

&nbsp;

### The library provides methods to:
  - Extract historical OHLC data for commodities from Norgate Data and S&P 500 from Yahoo Finance.
  - Calculate technical indicators over a range of time periods and aggregate to determine trend strength. 
  - Display charts of markets based on trend strength:

&nbsp;

### Installation
Install from PyPI:
```
$ pip install trendvisualizer
```


&nbsp;

To install in new environment using anaconda:
```
$ conda create --name trendvis
```
Activate new environment
```
$ activate trendvis
```
Install Python
```
(trendvis) $ conda install python==3.8.8
```
Install Spyder
```
(trendvis) $ conda install spyder==4.2.5
```

Install trendvisualizer
```
(trendvis) $ python -m pip install trendvisualizer
```

&nbsp;

### Setup
Import trend module and initialise a DataSet object

```
import trendstrength.trend as trend
mkt = trend.DataSetYahoo('2018-08-10', '2020-10-23')
```
Extract market data, calculate indicators and trend strength
```
mkt.prepyahoo()
```

&nbsp;

####	Display Bar chart
```
mkt.trendbarchart(mkts=20, trend='up')
```
![comm_bar_up](images/comm_bar_up.png)

```
mkt.trendbarchart(mkts=20, trend='strong')
```
![stock_bar_strong](images/stock_bar_strong.png)

```
mkt.trendbarchart(mkts=20, trend='neutral')
```
![comm_bar_neutral](images/comm_bar_neutral.png)

&nbsp;

####	Display Line chart
```
mkt.returnsgraph(days=60, trend='strong')
```
![stock_strong_60d_line](images/stock_strong_60d_line.png)
```
mkt.returnsgraph(days=120, mkts=10, trend='down')
```
![comm_120d_down_line](images/comm_120d_down_line.png)
```
mkt.returnsgraph(days=250, mkts=10, trend='up')
```
![stock_250d_up_line](images/stock_250d_up_line.png)

&nbsp;

####    Display Multiple chart grid
```
mkt.marketchart(days=60, trend='up')
```
![comm_mkt_up_return_60d](images/comm_mkt_up_return_60.png)
```
mkt.marketchart(days=120, trend='down', norm=False)
```
![stock_mkt_down_price_120d](images/stock_mkt_down_price_120d.png)  
```
mkt.marketchart(days=60, trend='strong', norm=False)
```
![comm_mkt_price_strong_500](images/comm_mkt_price_strong_500.png)  