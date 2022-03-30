# -*- coding: UTF-8 -*-
'''
@Author  ：Jiangtao Shuai
@Date    ：30.03.22

read all ENC .000 format files in data folder, and collect all bridges within a certain range of Leuven
'''

from geopanda_extractor import getAllFileNames, getPointByCoordinate, GpdEncExtractor


DATA_PATH = './data'

'''
Leuven:
GPS: 50.87959 4.70093 (latitude, longitude)
'''
LEUVEN = (50.87959, 4.70093)
reference_point = getPointByCoordinate(LEUVEN[0], LEUVEN[1])

# set search range(kilometers)
RANGE = 40

# get all file names
enc_files = getAllFileNames(DATA_PATH)

bridges_collection = []
for file in enc_files:
    # read file
    reader = GpdEncExtractor(file)
    # get bridges information in a file
    bridges = reader.getGpdByLayerName('bridge')
    # filter
    near_bridges = reader.getFilteredGdfByDistance(bridges, reference_point, RANGE)
    if near_bridges is not None:
        bridges_collection.append(near_bridges)

print(len(bridges_collection))