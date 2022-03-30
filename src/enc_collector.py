# -*- coding: UTF-8 -*-
"""
@Author  ：Jiangtao Shuai
@Date    ：30.03.22
"""
from geopanda_extractor import (
    GpdEncExtractor,
    getAllFileNames,
    getPointByCoordinate
)
import os.path
import pickle


class EncCollector:

    def __init__(self, data_root_path, reference_point, reference_name, search_range, layer_name):

        self.reference_point = getPointByCoordinate(reference_point[0], reference_point[1])
        self.reference_name = reference_name
        self.enc_files = getAllFileNames(data_root_path)
        self.layer_name = layer_name
        self.search_range = search_range

    def getCollectionByDistance(self, to_export=False, save_map=False):
        """
        in given data root folder, get a set of objects within a given range to reference point

        :param to_export: whether export the collected data
        :type to_export: bool
        :param save_map: whether save the related folium map
        :type save_map: bool
        :return: objects_collection
        :rtype: dict
        """
        # check if the required file already exists
        file_name = os.path.join('./result',
                                 f'{self.layer_name}_within_{self.search_range}km_to_{self.reference_name}.pickle')
        if os.path.exists(file_name):
            return self.loadCollection(file_name)

        objects_collection = {}

        for file in self.enc_files:
            # get folder code
            folder_code = file.split('.000')[0]
            folder_code = folder_code.split('/')[-1]

            # read file
            reader = GpdEncExtractor(file)
            # get objects information of a given layer name
            objects_gpd = reader.getGpdByLayerName(self.layer_name)

            # filter by distance
            near_objects_gpd = reader.getFilteredGdfByDistance(
                objects_gpd,
                self.reference_point,
                self.search_range
            )

            # check if it exists the related objects in the given range
            if near_objects_gpd is not None:
                # if it exists, collect it and its belonging layer
                objects_collection[folder_code] = (near_objects_gpd, reader)

                # store the collected data in pickle file
                if to_export:
                    self.exportCollection(objects_collection)
                # generate and store the corresponding folium map as .html file
                if save_map:
                    m = near_objects_gpd.explore("area", legend=False)
                    m.save(f"./result/{folder_code}.html")

        return objects_collection

    def exportCollection(self, objects_collection):
        """export the collection as .pickle file"""

        with open(
                os.path.join('./result',
                             f'{self.layer_name}_within_{self.search_range}km_to_{self.reference_name}.pickle'),
                'wb'
        ) as f:
            pickle.dump(objects_collection, f)

    def loadCollection(self, file_name):
        """load the exported pickle file"""

        with open(file_name, 'rb') as f:
            objects_collection = pickle.load(f)

        return objects_collection


if __name__ == '__main__':
    print('hello world')
