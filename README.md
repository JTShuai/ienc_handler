# ienc_handler

A demo based on [Geopandas](https://geopandas.org/) that read IENC data in order to get a set of certain objects(e.g., bridges) information.

## Installation
In root path, run `pip install -e .`

## Requirements
 - [Geopandas](https://geopandas.org/)
 - Python 3.9
 - [shapely](https://shapely.readthedocs.io/)
 - fiona
 - pandas

## Data
The Inland Electronic Navigation Charts(IENC) in Flanders can be found in [here](https://www.visuris.be/default.aspx?path=Diensten/Vaarkaarten).
File structure in `data/` folder:
```
ienc_handler
├── data
│   ├── <map-name-1>
│   │   ├── <map-name-1>.000
│   │   ├── ...
│   ├── <map-name-2>
│   ...
```

## Usage
See the examples in [script](https://github.com/JTShuai/ienc_handler/tree/main/script).
1. `bridge_example.py`: get the specified objects in a given searching range w.r.t a given reference position.
2. `geometry_geojson.py`: run 
    ```shell 
    python geometry_geojson.py -i <enc-map-name>.000 -l <layer1, e.g., bridge>,<layer2, e.g., COALNE> -o <layer1>.geojson,<layer2>.geojson
    ```

## Results
[Here](https://github.com/JTShuai/ienc_handler/tree/main/result) is an example outcome that gathers bridges located within a 40 km radius of Leuven:
- The '.html' files illustrate the searched bridge objects with their data.
- The '.pickle' file contains the corresponding Geopandas objects