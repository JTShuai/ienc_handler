# -*- coding: UTF-8 -*-
"""
@Author  ：Jiangtao Shuai
@Date    ：30.03.22

read all ENC .000 format files in data folder, and collect all bridges within a certain range of Leuven
"""

from enc_collector import EncCollector

params = {
    'data_root_path': './data',
    'reference_point': (50.87959, 4.70093),
    'reference_name': 'Leuven',
    'search_range': 40,
    'layer_name': 'bridge'
}

my_collector = EncCollector(**params)
bridge_set = my_collector.getCollectionByDistance(True, True)



