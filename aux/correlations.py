import sys
import pandas as pd
import calc

data_file = sys.argv[1]

df = pd.read_csv(data_file)
reject, pvalue, b, m, R2 = calc.Stats().ttest_regression(df['area_min'].values, df['diameter'].values)
print(reject, pvalue, b, m, R2)
reject, pvalue, b, m, R2 = calc.Stats().ttest_regression(df['area_med'].values, df['diameter'].values)
print(reject, pvalue, b, m, R2)
reject, pvalue, b, m, R2 = calc.Stats().ttest_regression(df['area_max'].values, df['diameter'].values)
print(reject, pvalue, b, m, R2)
reject, pvalue, b, m, R2 = calc.Stats().ttest_regression(df['pico_area_px'].values, df['diameter'].values)
print(reject, pvalue, b, m, R2)
reject, pvalue, b, m, R2 = calc.Stats().ttest_regression(df['area_med'].values, df['shortpath_mean'].values)
print(reject, pvalue, b, m, R2)
