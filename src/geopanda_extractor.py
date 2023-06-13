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
import matplotlib
import matplotlib.pyplot as plt
import os.path
import webbrowser
from shapely import geometry
from shapely.geometry import Polygon, LineString, Point
from copy import deepcopy
import geopy.distance


def getGpsCoordFromPoint(point: Point):
    """
    get longitude and latitude from Point object

    :param point: shapely point object
    :type point: geometry
    :return: longitude, latitude
    :rtype: string
    """

    c_lon, c_lat = point.coords.xy
    c_lon, c_lat = c_lon[0], c_lat[0]

    return c_lon, c_lat


def getPointByCoordinate(latitude, longitude):
    """
    transform lat/lon point to WGS84 shapely point

    :return: (longitude ,latitude)
    :rtype: shapely.geometry
    """
    p = gpd.points_from_xy([longitude], [latitude], crs=f"EPSG:{GpdEncExtractor.EPSG}")[0]

    return p


def getAllFileNames(data_path):
    """get all ENC file names in the data folder"""

    files_list = glob.glob(data_path + '/*/*.000')

    return files_list


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
        # if the given layer_name is not contained in data
        if layer_name not in self.enc_layers.keys():
            return None

        layer_gdf = self.enc_layers[layer_name].copy()

        # geographic coordinate system (GCS) -> projected coordinate system (PCS)
        """
        here, actually the transformation dose not be executed, because 
        the further distance calculation is based on gps coordinate.
        
        ENC geometry data is based on epsg4326 (geographic), 
        the following line is only used to remind me to notice to_crs() method
        """
        geometrylayer = layer_gdf.geometry



        layer_gdf = layer_gdf.to_crs(epsg=4326)

        # add area and centroid information
        # layer_gdf["area"] = layer_gdf.area
        #layer_gdf['centroid'] = layer_gdf.centroid

        #layer_gdf = layer_gdf.to_crs(epsg=3857)
        #layer_gdf["area"] = layer_gdf.area

        return geometrylayer

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

        # check the validation
        if layer_gdf is None:
            return None

        # get distance
        layer_gdf = self.getDistanceToRefPoint(layer_gdf, reference_point)

        # filter the data
        filtered_gdf = deepcopy(layer_gdf)

        range_filter = (filtered_gdf['distance'] <= radius)
        filtered_gdf = filtered_gdf.loc[range_filter]

        # check if there is bridge in the given range
        if filtered_gdf.shape[0] == 0:
            return None

        return filtered_gdf


if __name__ == '__main__':
    PATH = 'C:\\Users\\martibae\\Documents\\ENC_code\\INEC_Demo\\data\\7V7KLEDI'
    FILE = os.path.join(PATH, '7V7KLEDI.000')

    DATA_PATH = '../data'

    getAllFileNames(DATA_PATH)
    '''
    Leuven:
    GPS: 50.87959 4.70093 (latitude, longitude)
    '''
    LEUVEN = (50.87959, 4.70093)

    reader = GpdEncExtractor(FILE)

    target_p = getPointByCoordinate(LEUVEN[0], LEUVEN[1])

    coastline = reader.getGpdByLayerName('COALNE')
    coastline.to_file("coastline.geojson", driver='GeoJSON')
    deptharea = reader.getGpdByLayerName('DEPARE')
    deptharea.to_file("deptharea.geojson", driver='GeoJSON')
    bridges = reader.getGpdByLayerName('bridge')
    bridges.to_file("bridges.geojson", driver='GeoJSON')
    #near_bridges = reader.getFilteredGdfByDistance(bridges, target_p, 42)

    #print(near_bridges)
