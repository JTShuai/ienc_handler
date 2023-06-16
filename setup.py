from setuptools import setup, find_packages


setup(
    name='ienc_handler',
    version='1.0',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=['shapely', 'geopandas', 'pandas', 'fiona','geopy',],
)