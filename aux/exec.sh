#!/bin/bash

#limiares=(0.91 0.92 0.93 0.94 0.95 0.96 0.97 0.98 0.99)
#limiares=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1)
#limiares=(0 0.01 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95 0.99 1)
limiares=(0.81 0.82 0.83 0.84 0.85 0.86 0.87 0.88 0.89)
for limiar in ${limiares[@]}; do
    echo $limiar
    /home/aure/PycharmProjects/graph4gis/venv/bin/python /home/aure/PycharmProjects/graph4gis/main.py /home/aure/lista_clip2.txt ${limiar}
done
