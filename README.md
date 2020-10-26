# trendbarometer
## Measure which markets are more strongly trending and visualize. 

&nbsp;

### The library provides methods to:
  - Extract historical OHLC data for commodities from Norgate Data and S&P 500 from Yahoo Finance.
  - Calculate technical indicators over a range of time periods and aggregate to determine trend strength. 
  - Display charts of markets based on trend strength:

&nbsp;

### Installation
Install from PyPI:
```
$ pip install trendbarometer
```
Most of the dependencies are straightforward but installing TA-Lib requires a little extra work. 

See [TA Lib README](https://github.com/mrjbq7/ta-lib) for more details.

&nbsp;

To install in new environment using anaconda:
```
$ conda create --name trend
```
Activate new environment
```
$ activate trend
```
Install Python
```
(trend) $ conda install python
```
Install Spyder
```
(trend) $ conda install spyder=4
```
From the TA Lib README:
##### Windows

Download [ta-lib-0.4.0-msvc.zip](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-msvc.zip)
and unzip to ``C:\ta-lib``.

> This is a 32-bit binary release.  If you want to use 64-bit Python, you will
> need to build a 64-bit version of the library. Some unofficial (**and
> unsupported**) instructions for building on 64-bit Windows 10, here for
> reference:
>
> 1. Download and Unzip ``ta-lib-0.4.0-msvc.zip``
> 2. Move the Unzipped Folder ``ta-lib`` to ``C:\``
> 3. Download and Install Visual Studio Community 2015
>    * Remember to Select ``[Visual C++]`` Feature
> 4. Build TA-Lib Library
>    * From Windows Start Menu, Start ``[VS2015 x64 Native Tools Command
>      Prompt]``
>    * Move to ``C:\ta-lib\c\make\cdr\win32\msvc``
>    * Build the Library ``nmake``

Alternatively there are unofficial windows binaries for both 32-bit and 64-bit here:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

These are installed (after downloading) via pip:
```
(trend) $ python -m pip install TA_Lib-0.4.17-cp38-cp38-win_amd64.whl 
```

Install TA-Lib for Python
```
(trend) $ python -m pip install TA-Lib 
```

Install Trend Barometer
```
(trend) $ python -m pip install trendbarometer
```

&nbsp;

### Setup
Import barometer module and initialise a DataSet object

```
import trendbarometer.barometer as bar
mkt = vol.DataSetYahoo('2018-08-10', '2020-10-23')
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