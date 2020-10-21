# trendbarometer
## Measure which markets are more strongly trending and visualize. 

&nbsp;

### The library provides methods to:
  - Extract historical OHLC data for commodities from Norgate Data and S&P 500 from Yahoo Finance.
  - Calculate technical indicators over a range of time periods and aggregate to determine trend strength. 
  - Display charts of markets based on trend strength:

&nbsp;

### Installation
Install via GitHub:
```
pip install git+https://github.com/GBERESEARCH/trendbarometer
```
Most of the dependencies are straightforward but installing TA-Lib can sometimes be problematic. 

&nbsp;

### Setup
Import barometer module and initialise a DataSet object

```
import barometer as bar
mkt = vol.DataSetYahoo('2018-08-10', '2020-09-28')
```
Extract market data, calculate indicators and trend strength
```
mkt.prepyahoo().createbarometer()
```

&nbsp;

####	Display Bar chart
```
mkt.trendbarchart(mkt.barometer, 20)
```
![stock_bar_top](images/stock_bar_top.png)

```
mkt.trendbarchart(mkt.barometer, 20, top=False)
```
![comm_bar_bottom](images/comm_bar_bottom.png)

&nbsp;

Prepare and normalize data
```
mkt.prepdata()
```
```
norm_3m = mkt.normalise(mkt.chart_data, 60) 
norm_6m = mkt.normalise(mkt.chart_data, 120) 
norm_1y = mkt.normalise(mkt.chart_data, 250)
```

&nbsp;

####	Display Line chart
```
mkt.returnsgraph(norm_3m)
```
![stock_60d_line](images/stock_60d_line.png)
```
mkt.returnsgraph(norm_6m)
```
![comm_120d_line](images/comm_120d_line.png)
```
mkt.returnsgraph(norm_1y)
```
![stock_250d_line](images/stock_250d_line.png)

&nbsp;

Prepare market data
```
mkt.prepdata(mkts=20)
```
####    Display Multiple chart grid
```
mkt.marketchart(days=60)
```
![stock_mkt_return_60d](images/stock_mkt_return_60d.png)
```
mkt.marketchart(days=60, norm=False)
```
![comm_mkt_price_250](images/comm_mkt_price_250.png)  