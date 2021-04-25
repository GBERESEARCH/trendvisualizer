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

Install trendstrength
```
(trend) $ python -m pip install trendstrength
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