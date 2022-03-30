# -*- coding: UTF-8 -*-
'''
THIS IS AN INCOMPLETE SCRIPT!

This script is based on GDAL library and records some notes of gdal.
The required functions are finished in geopanda_extractor.py with Geopandas library instead of GDAL.
This script should be completed in further work.

read Electronic Navigation Charts (ENC) data

@Author  ：Jiangtao Shuai
@Date    ：29.03.22
'''

from osgeo import gdal, ogr, osr
import os.path
import json

def wkbFlatten(x):
    return x & (~ogr.wkb25DBit)

class EncExtracotr:
    def __init__(self, filename):
        self.dataset = ogr.Open(filename)
        self.name = self.dataset.GetName()
        # self.geo_tran = self.dataset.GetGeoTransform()
        self.feature_classes = {}

    def getAllLayerNames(self, is_print = False):
        """
        get a list of layer names in dataset
        :return: layer_name_list
        :rtype: List
        """
        layer_name_list = []
        for i in range(self.dataset.GetLayerCount()):
            layer = self.dataset.GetLayerByIndex(i)
            spa_ref = layer.GetSpatialRef()
            layer_name = layer.GetName()
            layer_name_list.append(layer_name)
            layerDefn = layer.GetLayerDefn()
            if is_print:
                print(f'Layer {layerDefn.GetName()} is of type {layerDefn.GetGeomType()} and has {layerDefn.GetFieldCount()} fields')

        return layer_name_list

    def getFeatureInLayer(self, layer_name):
        """
        get a list of features in a given layer

        :param layer_name: A selected layer name
        :type layer_name: string
        :return: feature_list
        :rtype: List
        """
        feature_list = []
        layer = self.dataset.GetLayerByName(layer_name)
        # reset order before iteration
        layer.ResetReading()

        for i in range(layer.GetFeatureCount()):
            feature = layer.GetNextFeature()
            feature_list.append(feature)

        return feature_list

    def getAttributeSetInLayer(self, layer_name):
        """
        get attributes set in a layer
        :param layer_name:
        :type layer_name:
        :return:
        :rtype:
        """
        attribute_map = {}

        layer = self.dataset.GetLayerByName(layer_name)
        layer_defn = layer.GetLayerDefn()

        # traversal all fields in the layer
        for i in range(layer_defn.GetFieldCount()):
            field = layer_defn.GetFieldDefn(i)
            attr_name = field.GetNameRef()
            attr_value = field.GetType()

            attribute_map[attr_name] = attr_value

        return attribute_map

    def getAttributeInFeature(self, layer_name):
        """
        get each feature's attribute value in a given layer
        :param layer_name:
        :type layer_name:
        :return:
        :rtype:
        """
        attr_name_map = {}
        feature_list = self.getFeatureInLayer(layer_name)

        # feature = feature_list[0]
        #
        # test = feature.GetDefnRef()

        attribute_map = self.getAttributeSetInLayer(layer_name)
        feature_types = list(attribute_map.keys())
        result = []
        for feature in feature_list:
            type_value_map = {}

            for f_type in feature_types:
                field_value = feature.GetFieldAsString(f_type)

                type_value_map[f_type] = field_value
            result.append(type_value_map)
        return result




    def getSpatialInLayer(self, layer_name):
        layer = self.dataset.GetLayerByName(layer_name)
        spatial_ref = layer.GetSpatialRef()

        if not spatial_ref.IsGeographic():
            print('Source does not have a geographic coordinate system')

        s_name = spatial_ref.GetName()
        s_attri_value = spatial_ref.GetAttrValue('AXIS')


        test = spatial_ref.ExportToWkt()
        print(test)

        old_cs = osr.SpatialReference()
        # old_cs.ImportFromWkt(self.dataset.GetProjectionRef())

        new_cs = osr.SpatialReference()
        new_cs.ImportFromWkt(test)

        # TODO spatial reference
        # create a transform object to convert between coordinate systems
        transform = osr.CoordinateTransformation(old_cs, new_cs)

        return spatial_ref


if __name__ == '__main__':
    PATH = '../data/7V7ALBK1-4'
    FILE = os.path.join(PATH, '7V7ALBK1.000')
    CATA = os.path.join(PATH, 'CATALOG.031')

    extractor = EncExtracotr(FILE)
    layer_list = extractor.getAllLayerNames()
    feature_list = extractor.getFeatureInLayer('bridge')
    attribute_map = extractor.getAttributeSetInLayer('bridge')
    attr_name_map = extractor.getAttributeInFeature('bridge')
    layers = extractor.getAllLayerNames()
    # points = extractor.getGeomInFeature('bridge')



    '''
    GEOGCS["WGS 84",  
        DATUM["WGS_1984", SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]], AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],
        AXIS["Latitude",NORTH],
        AXIS["Longitude",EAST],
        AUTHORITY["EPSG","4326"]
        ]
               
    
    '''


    print(feature_list)