# -*- coding: utf-8 -*-
"""
Created on Tue May 17 17:24:09 2022

@author: ramendra
"""

class RasterFile:
    def __init__(self, raster):
        self.raster_name = raster
        
    def rasterInfo(self):
        import rasterio
        ds = rasterio.open(self.raster_name)
        xRes = ds.meta['transform'][0]
        yRes = ds.meta['transform'][4] * (-1)
        ncols = ds.width
        nrows = ds.height
        
        return {'ncols' : ncols, 'nrows' : nrows, 
                'xRes' : xRes, 'yRes' : yRes}
    
    def convert2array(self):
        import rasterio
        ds = rasterio.open(self.raster_name)
        ar = ds.read(1)
        return ar    
    
    @staticmethod
    def array_max(array):
        import numpy as np
        return np.nanmax(array)
        