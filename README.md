BitcoinTimeSeriesAnalysis
==============================

Version: 1.0a0

Platform: Windows

Summary: Bitcoin Daily Closing Price Analysis

Keywords: bitcoin UnivarianteTimeSeries Visualization ExtractionFeatures

Installation:
Create a virtual environment variable and, then, run requirements.txt
```bash
1) python -m venv myvenv_bitcoin
2) myvenv_bitcoin\Scripts\activate
3) pip install -r requirements.txt
```

Usage:
To process the data set with the information of the bitcoin prices, you must download in the following link,
https://www.kaggle.com/mczielinski/bitcoin-historical-data, the following files:
  - bitstamp_2012_01_01_to_2019_03_13.csv
  - coinbase_2014_12_01_to_2019_01_09.csv
and place it on the following route within the project: src\data. Then, you must change the directory to src\data and run the script processing_bitcoin.py

```bash
python processing_bitcoin.py
```

To analyze the Bitcoin prices, you must run the notebook called UNIVARIATE_TIME_SERIES_ANALYSIS_AND_AUTOMATIC_FEATURE_EXTRATION - BITCOIN.ipynb

```bash
1) ipython kernel install --user --name=myvenv_bitcoin
2) jupyter notebook
```

Project Organization
------------
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── bitstamp_2012_01_01_to_2019_03_13.csv   <- Bitcoin Data taken from Kaggle  https://www.kaggle.com/mczielinski/bitcoin-historical-data
    │   └── coinbase_2014_12_01_to_2019_01_09.csv   <- Bitcoin Data taken from Kaggle
    https://www.kaggle.com/mczielinski/bitcoin-historical-data
    │           
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to generate Bitcoin data
    │   │   └── processing_bitcoin.py <- Apply analysis on prices closing daily bitcoin    
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │  
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │   │   └── timeserie_graph.py
    │   │    
    │   └── auxiliary_functions.py
    │           
    └── UNIVARIATE_TIME_SERIES_ANALYSIS_AND_AUTOMATIC_FEATURE_EXTRATION - BITCOIN.ipynb   <- Notebook to visualize the results of the Bitcoin Time Serie analysis

Author:
Maria Francys Lanza Garcia

Author-email:
mariafrancysucv@gmail.com
