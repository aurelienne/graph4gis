#!/bin/bash

for filename in $(ls /dados/radar/saoroque/cappi/cappi3km/2020/03/*.raw); do
  python ./recorte_radar.py ${filename} /dados/radar/saoroque/cappi/cappi3km_sp/2020/03/
done

for filename in $(ls /dados/radar/saoroque/cappi/cappi3km_sp/2020/03/*.raw); do
  python ./gera_bin_prec.py ${filename} /dados/radar/saoroque/cappi/cappi3km_sp_prec/2020/03/
done

dir_input="/dados/radar/saoroque/cappi/cappi3km_sp_prec/2020/03/"
dir_output="/dados/radar/saoroque/cappi/cappi3km_sp_prec_hourly/2020/03/"
python ./gera_acum_prec_hourly.py ${dir_input} ${dir_output} 2020030100 2020033123