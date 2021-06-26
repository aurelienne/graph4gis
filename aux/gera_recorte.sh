#!/bin/bash

for filename in $(ls /dados/radar/saoroque/cappi/cappi3km/2019/03/*.raw); do
  python ./recorte_radar.py ${filename} /dados/radar/saoroque/cappi/cappi3km_rmsp/2019/03/
done