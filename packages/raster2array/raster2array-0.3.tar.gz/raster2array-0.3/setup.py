from setuptools import setup

setup(name = 'raster2array', 
      version = '0.3', 
      description = 'Converts a esri raster to numpy array using rasterio', 
      author = 'Ramendra Sahoo', 
      packages = ['raster2array'],
      install_requires=['numpy', 'gdal'],
      zip_safe = False)