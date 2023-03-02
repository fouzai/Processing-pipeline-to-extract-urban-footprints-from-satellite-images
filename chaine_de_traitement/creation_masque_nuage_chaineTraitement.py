from os import listdir
import geopandas as gpd
from os.path import join
import os
import numpy as np
import rasterio
from os.path import join, basename
from rasterio import features
import numpy.ma as ma

def cloud_mask(dataset,c_mask) :
    """" creer un masque de nuage binaire
    dataset : directory vers les fichier CLM_Band pour sentinel 2 et fichier QA_pixel pour Landsat
    output  : directory de sortie
    c_mask  : bit a masquer : exemple  0b00000010 pour sentinel2
    """
    output = join(os.path.split(dataset)[0],"mask")
    os.mkdir(output)
    files = os.listdir(dataset)
    tifs = [filename for filename in files if filename.lower().endswith("tif")]
    for i in range(len(tifs)) :
        f_clm_pixel = rasterio.open(join(dataset,tifs[i]))
        kwds = f_clm_pixel.profile
        band_clm = f_clm_pixel.read(1)
        mask = (np.bitwise_and(band_clm, c_mask) > 0)
        output_file = tifs[i][:-4]+"_mask.tif"
        with rasterio.open(join(output,output_file), 'w', **kwds) as r_output:
            r_output.write(mask.astype(np.uint8),1)
        print(output_file + " est créé")

    return output


# chemin vers les données d'entrées
#dataset = "/home/fouzai/chaineTraitement/clm_band"

# chemin vers les données de sorties
#output = "/home/fouzai/chaineTraitement/mask"

#masque de comparaison




#créér un masque bianire et l'enregistrer au chemin de sortie
#cloud_mask(dataset,output,c_mask)