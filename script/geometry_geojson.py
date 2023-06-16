# -*- coding: UTF-8 -*-
'''
@Author  ：Jiangtao Shuai
@Date    ：16/06/2023 6:10 PM 
'''


from ienc_handler.feature_extractor import (
    GpdEncExtractor,
    getAllFileNames,
    getPointByCoordinate
)
import os.path
import sys
import getopt


if __name__ == '__main__':
    # Command-line arguments
    arguments = sys.argv[1:]
    short_options = "hi:l:o:v"
    long_options = ["help", "input=", 'layer=', "output=", "verbose"]

    try:
        # Parsing the options and arguments
        opts, args = getopt.getopt(arguments, short_options, long_options)
    except getopt.GetoptError as error:
        print(str(error))
        sys.exit(2)

    input_file = None
    layer_name = None
    output_file = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
                "-i or --input: input IENC file", '\n',
                "-l or --layer: layer (feature) name,", 'multiple layers use comma, e.g., <layer1,layer2>', '\n',
                "-o or --output: output file,", 'multiple layers use comma, e.g., <file1.geojson,file2.geojson>', '\n',
                "Usage: \n python <file>.py -i <ienc-file>.000 -l <layer-name> -o <output-file>.geojson  \n or \n",
                "python <file>.py --input=<ienc-file>.000 --layer=<layer-name> --output=<output-file>.geojson"
            )
        elif opt in ("-i", "--input"):
            input_file = arg
            print("Input file:", input_file)
        elif opt in ("-l", "--layer"):
            layer_name = arg.split(',')
            print("Layer name:", layer_name)
        elif opt in ("-o", "--output"):
            output_file = arg.split(',')
            print("Output file:", output_file)

    if len(layer_name) != len(output_file):
        print('current layer: ', layer_name, f' has {len(layer_name)} items')
        print('current output: ', output_file, f' has {len(output_file)} items')

        raise Exception("layer number has to be equal to output number")

    if input_file and layer_name and output_file:
        reader = GpdEncExtractor(input_file)
        for l_name, output_f in zip(layer_name, output_file):
            geo_data = reader.getGeometryByName(l_name)
            reader.saveAsGeoJson(geo_data, output_f)

            print(f"layer(feature) {l_name} is stored at {output_f}")
    else:
        print('please provide all input: file name, layer name, output name')


