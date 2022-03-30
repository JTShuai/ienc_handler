# INEC_Demo

A demo based on [Geopandas](https://geopandas.org/) that read IENC data in Flanders in order to get a set of certain objects(e.g., bridges) information within a given range to reference position.

## Requirements
 - [Geopandas](https://geopandas.org/)
 - Python 3.9
 - [shapely](https://shapely.readthedocs.io/)

## Data
The Inland Electronic Navigation Charts(IENC) in Flanders can be found in [here](https://www.visuris.be/default.aspx?path=Diensten/Vaarkaarten)

## Results
[Here](https://github.com/JTShuai/INEC_Demo/tree/main/result) is the collection where the information on bridges within 40 km far away from Leuven is stored. 
- The '.html' files illustrate the searched bridge objects with their data.
- The '.pickle' file contains the corresponding Geopandas objects