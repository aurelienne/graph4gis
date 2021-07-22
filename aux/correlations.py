import sys
import pandas as pd
import calc
from matplotlib import pyplot

data_file = sys.argv[1]

df = pd.read_csv(data_file)
#pyplot.hist(df['duracao'].values, bins=30)
#pyplot.show()
#sys.exit()

meteo_metrics = ["duracao", "pico_pmax", "pico_pmed", "pico_area_km2", "pico_area_px", "vel_min", "vel_med",
                 "vel_max", "area_min", "area_med", "area_max", "pmed_med", "pmax_med", "num_eventos_simult"]
netwk_metrics = ["vertices", "edges", "cluster_coef", "avg_degree", "diameter", "shortpath_mean",
                 "avg_betweeness", "num_components", "giant_component_v", "giant_component_e", "singletons"]

df1 = df.loc[(df["duracao"] <= 2)]
df2 = df.loc[(df["duracao"] > 2) & (df["duracao"] <= 3)]

for meteo_metric in meteo_metrics:
    for netwk_metric in netwk_metrics:
        reject, pvalue, b, m, R2 = calc.Stats().ttest_regression(df2[meteo_metric].values,
                                                                 df2[netwk_metric].values)
        if R2 >= 0.5:
            print(meteo_metric + " X " + netwk_metric + ":")
            print(reject, pvalue, b, m, R2)
