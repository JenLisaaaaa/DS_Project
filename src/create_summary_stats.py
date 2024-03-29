import pandas as pd
import load_zero_coupon as ldzc
import load_bbg_data as lbbg
import clean_data as cld
import config
import numpy as np
import math

DATA_DIR = config.DATA_DIR
USE_BBG = config.USE_BBG
PAPER_END_DT = config.PAPER_END_DT


def summary_stats(series1, series2, series3, series4, series5):   
    # Summary statistics for each series
    summary1 = series1.describe()
    summary2 = series2.describe()
    summary3 = series3.describe()
    summary4 = series4.describe()
    summary5 = series5.describe()
    
    # Autocorrelation for each series
    autocorr1 = series1.autocorr(lag=1)
    autocorr2 = series2.autocorr(lag=1)
    autocorr3 = series3.autocorr(lag=1)
    autocorr4 = series4.autocorr(lag=1)
    autocorr5 = series5.autocorr(lag=1)
    
    # Combine all statistics into a DataFrame
    stats_df = pd.concat([summary1, summary2, summary3, summary4, summary5], axis=1)
    stats_df.columns = [series1.name, series2.name, series3.name, series4.name, series5.name]
    stats_df.loc['Autocorrelation'] = [autocorr1, autocorr2, autocorr3, autocorr4, autocorr5]

    stats_df = stats_df.round(3)
    
    return stats_df.transpose()


if __name__ == "__main__":
    if USE_BBG:
        bbg_df = cld.clean_bbg_data(PAPER_END_DT, data_dir=DATA_DIR)
    else:
        bbg_df = lbbg.load_bbg_data(data_dir=DATA_DIR)

    one_year_zc_df = cld.clean_one_year_zc(bbg_df.index, PAPER_END_DT, data_dir=DATA_DIR)

    print(summary_stats(bbg_df['dividend yield'], bbg_df['index'], bbg_df['futures'], 
                        one_year_zc_df['1_year_yield'], one_year_zc_df['1_y_dis_factor']))
    
