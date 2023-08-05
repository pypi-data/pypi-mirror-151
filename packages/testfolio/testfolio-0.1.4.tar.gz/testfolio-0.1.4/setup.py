# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testfolio']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.0', 'yfinance>=0.1.70']

setup_kwargs = {
    'name': 'testfolio',
    'version': '0.1.4',
    'description': 'Quick portfolio backtesting using historical market data',
    'long_description': '# testfolio\n<a target="new" href="https://pypi.org/pypi/testfolio"><img border=0 src="https://img.shields.io/pypi/pyversions/testfolio"></a>\n<a target="new" href="https://pypi.org/pypi/testfolio"><img border=0 src="https://img.shields.io/pypi/dm/testfolio"></a>\n<a target="new" href="https://pypi.org/pypi/testfolio"><img border=0 src="https://img.shields.io/pypi/v/testfolio"></a>\n<a target="new" href="https://www.codefactor.io/repository/github/bradleyhe/testfolio"><img border=0 src="https://img.shields.io/codefactor/grade/github/BradleyHe/testfolio"></a>\n\nBacktest your portfolio allocations using historical market data from Yahoo Finance.\n\n## Quick Start\n### Installation\nYou can install **testfolio** using pip:\n``` {.sourceCode .bash}\n$ pip install testfolio -U\n```\n\n### Requirements\n**testfolio** depends on [yfinance](https://github.com/ranaroussi/yfinance) for retrieving market data; as such, the requirements match its requirements.\n- [Python](https://www.python.org) \\>= 3.4+\n- [Pandas](https://github.com/pydata/pandas) \\>= 0.23.1\n- [Numpy](http://www.numpy.org) \\>= 1.11.1\n- [requests](http://docs.python-requests.org/en/master/) \\>= 2.14.2\n- [lxml](https://pypi.org/project/lxml/) \\>= 4.5.1\n- [Matplotlib](https://matplotlib.org/) \\>= 3.5.0\n\n### Example Usage\n#### Creating a backtest\nStock tickers are specified in the allocation, along with their respective percent allocations. Rebalancing frequency, start date, and end date can also be specified.\n```python\nimport testfolio as tsf\n\nallocation_1 = {\n    \'SPY\': 0.6,\n    \'TLT\': 0.4\n}\n\nbacktest_1 = tsf.Backtest(allocation_1, rebalance=\'q\', name=\'60/40 Portfolio\')\nprint(backtest_1)\n```\n\n#### Output\n```text\n------------------- Metrics -------------------\nName: 60/40 Portfolio\nAllocation: {\'SPY\': 0.6, \'TLT\': 0.4}\nStarting Value: $1000.00\nEnding Value: $4889.48\nStart Date: 2002-08-01\nEnd Date: 2022-05-13\nCAGR: 8.35%\nMaximum Drawdown: -27.87%\nSTD (annualized): 8.95%\nSharpe Ratio: 0.81\nSortino Ratio: 1.23\nMarket Correlation: 0.81\n-----------------------------------------------\n```\n\nOptions for creating the backtest can be seen below:\n```python\nbacktest = Backtest(\n            # Must be a dictionary with ticker keys corresponding to allocation percentages that sum to 1.\n            allocation, \n    \n            # Portfolios are rebalanced quarterly by default. Other options include \'m\' (monthly), \'y\' (yearly), and \n            # \'no\' (no rebalancing)\n            rebalance=\'q\', \n            \n            # Must be in YYYY-mm-dd string format. Set to the earliest possible date when all tickers existed by \n            # default. Will be rounded to the 1st of the next month.\n            start_date=\'2020-01-01\',\n            \n            # Must be in YYYY-mm-dd string format. Set to today by default. Will be rounded to the 1st of the last month.\n            end_date=\'2022-03-02\',\n    \n            # Set to 1000 by default.\n            start_val=1000,\n    \n            # If True, then dividends are reinvested into its security. If False, then dividends generated are not \n            # incorporated into the portfolio.\n            invest_dividends=False,\n    \n            # Set to "Portfolio n" where n is the nth portfolio made by default.\n            name=\'Example Portfolio\')\n```\nAliases for broad market indices are available as well, and are set to the below mapping:\n```python\nALIAS_TO_TICKER = {\n    \'S&P 500\': \'VFINX\',\n    \'Long Term Treasury\': \'VUSTX\',\n    \'Total US Bond Market\': \'VBMFX\',\n    \'Total US Stock Market\': \'VTSMX\',\n    \'Total Intl Stock Market\': \'VGTSX\',\n    \'Gold\': \'GC=F\',\n    \'Intermediate Term Treasury\': \'IEF\',\n    \'Short Term Treasury\': \'VFISX\',\n    \'REIT\': \'VGSIX\',\n    \'US Small Cap\': \'NAESX\',\n    \'US Mid Cap\': \'VMCIX\'\n}\n```\nIn addition to the attributes set during creation, Backtest objects have the following attributes:\n```python\nbacktest = Backtest(allocation)\n\n# pandas DataFrame containing the value of the portfolio every month. Columns include each of the tickers, the total \n# portfolio value, and drawdown.\nbacktest.hist \n\n# Maximum drawdown \nbacktest.max_drawdown\n\n# Compound annual growth rate \nbacktest.cagr\n\n# Annualized standard deviation of returns\nbacktest.std\n\n# Sharpe ratio (using 3 month T-Bill as risk free asset)\nbacktest.sharpe\n\n# Sortino ratio (using 3 month T-Bill as risk free asset)\nbacktest.sortino\n\n# Pearson correlation coefficient with the S&P 500\nbacktest.correlation\n```\n\n\n#### Graphing backtests\n\n```python\nallocation_2 = {\n    \'Total US Stock Market\': 0.60,\n    \'Total Intl Stock Market\': 0.20,\n    \'Total US Bond Market\': 0.20\n}\n\nbacktest_2 = tsf.Backtest(allocation_2, rebalance=\'q\', name=\'Three Fund Portfolio\')\ntsf.graph_return(backtest_1, backtest_2, start_val=1000, logarithmic=True, path=\'returns.png\')\ntsf.graph_drawdown(backtest_1, backtest_2, path=\'drawdowns.png\')\n```\n\n#### Output\n![returns](https://github.com/BradleyHe/testfolio/raw/main/example/returns.png)\n![drawdowns](https://github.com/BradleyHe/testfolio/raw/main/example/drawdowns.png)\n\n',
    'author': 'Bradley He',
    'author_email': 'bhe6001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BradleyHe/testfolio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
