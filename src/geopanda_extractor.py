# -*- coding: UTF-8 -*-
'''
@Author  ：Jiangtao Shuai
@Date    ：30.03.22
'''
import geopandas as gpd
import pandas as pd
import fiona
from sys import stdout
import numpy as np
import glob
from pickle import dumps
import matplotlib.pyplot as plt
import os.path
import folium
import webbrowser
from shapely import geometry
from shapely.geometry import Polygon, LineString, Point
from copy import deepcopy
import geopy.distance


def getGpsCoordFromPoint(point:Point):

    c_lon, c_lat = point.coords.xy
    c_lon, c_lat = c_lon[0], c_lat[0]

    return c_lon, c_lat


class GpdEncExtractor:
    """
    read ENC data by geopandas
    """
    #
    EPSG = 4326

    def __init__(self, filename):
        self.enc_layers = {}
        # load data from ENC
        for layer_name in fiona.listlayers(filename):
            self.enc_layers[layer_name] = gpd.read_file(filename, layer=layer_name)

    def getGpdByLayerName(self, layer_name):
        """
        get the required GeoDataFrame object by the given layer name of ENC data

        :param layer_name: selected layer name
        :type layer_name: string
        :return: layer_gdf
        :rtype: GeoDataFrame
        """
        layer_gdf = self.enc_layers[layer_name].copy()

        # geographic coordinate system (GCS) -> projected coordinate system (PCS)
        """
        here, actually the transformation dose not be executed, because 
        the further distance calculation is based on gps coordinate.
        
        ENC geometry data is based on epsg4326 (geographic), 
        the following line is only used to remind me to notice to_crs() method
        """
        layer_gdf = layer_gdf.to_crs(epsg=4326)

        # add area and centroid information
        layer_gdf["area"] = layer_gdf.area
        layer_gdf['centroid'] = layer_gdf.centroid

        return layer_gdf

    def getDistanceToRefPoint(self, layer_gdf, reference_point: geometry):
        """
        get the distance(kilometer) from each ENC object centroid to the reference point in the given layer

        :param layer_gdf: the selected gpd dataframe
        :type layer_gdf: gpd.GeoDataFrame
        :param reference_point: the reference point
        :type reference_point: shapely.geometry
        :return: layer_gpd
        :rtype: gpd.GeoDataFrame
        """
        # dis_info = layer_gdf['centroid']

        # get longitude and latitude of the reference point
        ref_lon, ref_lat = getGpsCoordFromPoint(reference_point)

        def calculateDistance(centroid_p):

            # get longitude and latitude of centroid point
            c_lon, c_lat = getGpsCoordFromPoint(centroid_p)

            dist = geopy.distance.geodesic((c_lat, c_lon), (ref_lat, ref_lon))

            return dist.kilometers

        layer_gdf['distance'] = layer_gdf['centroid'].apply(calculateDistance)


        return layer_gdf

    def getFilteredGdfByDistance(self, layer_gdf, reference_point: geometry, radius):
        """
        get ENC objects data within a given range from the reference point

        :param layer_gdf: the selected geo dataframe
        :type layer_gdf: gpd.GeoDataFrame
        :param reference_point: the reference point
        :type reference_point: shapely.geometry
        :param radius: the filtering range
        :type radius: int
        :return: filtered gpd dataframe
        :rtype:
        """

        # get distance
        layer_gdf = self.getDistanceToRefPoint(layer_gdf, reference_point)

        # filter the data
        filtered_gdf = deepcopy(layer_gdf)

        range_filter = (filtered_gdf['distance'] <= radius)
        filtered_gdf = filtered_gdf.loc[range_filter]

        return filtered_gdf

    def getPointByCoordinate(self, latitude, longitude ):
        """
        transform lat/lon point to WGS84 shapely point

        :return: (longitude ,latitude)
        :rtype: shapely.geometry
        """
        p = gpd.points_from_xy([longitude], [latitude], crs=f"EPSG:{GpdEncExtractor.EPSG}")[0]


        return p


# 实时 map 文件
class Map:
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start

    def showMap(self, map_obj):
        # Create the map
        my_map = map_obj

        # Display the map
        my_map.save("map.html")
        webbrowser.open("map.html")


if __name__ == '__main__':
    PATH = '../data/7V7ALBK1-4'
    FILE = os.path.join(PATH, '7V7ALBK1.000')

    '''
    Leuven:
    GPS: 50.87959 4.70093 (latitude, longitude)
    '''
    # (lat,lon)
    LEUVEN = (50.87959, 4.70093)


    reader = GpdEncExtractor(FILE)

    target_p = reader.getPointByCoordinate(LEUVEN[0],LEUVEN[1])

    bridges = reader.getGpdByLayerName('bridge')
    # print(bridges)
    show_distance = reader.getDistanceToRefPoint(bridges, target_p)
    # print(show_distance)
    near_bridges = reader.getFilteredGdfByDistance(bridges, target_p, 42)

    print(near_bridges)



    '''
    # read a single ENC file
    enclayers = {}
    for layername in fiona.listlayers(FILE):
        enclayers[layername] = gpd.read_file(FILE, layer=layername)

    # bridge_layer = enclayers['bridge']
    bridge_gdf = enclayers['bridge'].copy()
    bridge_gdf = bridge_gdf.to_crs(epsg=4326)
    '''

    '''
    UserWarning: 
        Geometry is in a geographic CRS. Results from 'area' are likely incorrect. 
        Use 'GeoSeries.to_crs()' to re-project geometries to a projected CRS before this operation.
    
    bridge_gdf["area"] = bridge_gdf.area
    bridge_gdf['centroid'] = bridge_gdf.centroid
    # bridge_gdf['boundary'] = bridge_gdf.boundary
    '''

    '''plot the figure'''
    # w = 6.4
    # h = 4.8
    # zoom = 2
    # # # Plot depthe area polygons
    # # bridge_layer.plot(figsize=(zoom * w, zoom * h))
    #
    # bridge_gdf.plot("area", legend=True)
    # plt.show()
    '''在实时地图中打开'''
    # m = bridge_gdf.explore("area", legend=False)
    # coords = [51.5074, 0.1278]
    # map = Map(center=coords, zoom_start=13)
    # map.showMap(m)
