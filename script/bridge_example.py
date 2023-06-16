# -*- coding: UTF-8 -*-
"""
@Author  ：Jiangtao Shuai
@Date    ：30.03.22

read all ENC .000 format files in data folder, and collect all bridges within a certain range of Leuven
"""

from ienc_handler.batch_collector import BatchCollector

params = {
    'data_root_path': './data',
    'reference_point': (50.87959, 4.70093),
    'reference_name': 'Leuven',
    'search_range': 40,
    'layer_name': 'bridge'
}

my_collector = BatchCollector(**params)
bridge_set = my_collector.getCollectionByDistance(True, True)



