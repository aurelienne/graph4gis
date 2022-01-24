# Graph4GIS – From gridded data into geographical graphs

# About
The main objective of the tool is to allow the construction and analysis of geographic graphs from gridded data. In this construction, each node represents a grid point, and the edges represent similarities between the correspondent time series.

In this initial version, only simple binary formats are accepted. It was originally designed to handle weather radar data, but it can also be applied to other data with the same format. 

# Structure
The application is divided into 3 main modules: Data, Graph and Output. The first is responsible for reading the input data and doing all the data processing. 
A time series is created for each grid point, and then a similarity value between each pair of points is calculated. This value may come from two similarity functions that the program provides (Pearson Correlation or Mutual Information). The second module is in charge of creating the adjacency matrix and building the network from it. There are 3 methodologies available for building networks: Global-Threshold, Backbone and Configuration Model. In the same module, several functions for calculating network metrics are available. The Output module has the objective of exporting all the data and results generated by the tool: a shapefile of points and lines representing the constructed network, a CSV file with the global metrics of the network and a variety of graphs that the tool makes available.

# How to execute
Create a config file based on the samples provided (config_rmsp.ini and config_tamanduatei.ini), filling with the characteristics of the input data.
Then, you can run:

    python main.py <config_file> <input_files_list> <threshold> <type_of_threshold> <network_id>
    
Where:
threshold= minimum threshold value for creating the edges
type_of_threshold= md (max diameter) / p (percentile)
network_id= identification for saving output files.

# Requirements
Python 3.0+ and libs: igraph, networkx, matplotlib, numpy, pandas, scipy, osgeo 

# License
This project is licensed under the terms of the GNU GPL v3.0

# Developers 
Aurelienne Jorge (aurelienne@gmail.com) 
Leonardo B. L. Santos
Izabelly C. Costa

# References
JORGE, A. A. S.; COSTA I.C.; SANTOS L.B.L. Geographical Complex Networks applied to describe meteorological data. In: Proceedings XXI GEOINFO;2020. P.258–263. 
JORGE, A. A. S.; DINIZ, I. S.; FREITAS, V. L. S.; COSTA I.C.; SANTOS L.B.L. Global-threshold and backbone high-resolution weather radar networks are significantly complementary in a watershed. Submitted to Computers & Geosciences.
JORGE, A. A. S.; COSTA I.C.; SANTOS L.B.L. Relations between topological metrics and meteorological properties in precipitation events based on weather radar networks. To be submitted.
