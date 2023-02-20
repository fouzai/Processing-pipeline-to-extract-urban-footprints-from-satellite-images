from os import listdir
import geopandas as gpd
from os.path import join
import os
import numpy as np
import rasterio
from os.path import join, basename
from rasterio import features
import numpy.ma as ma

def calc_p_nuages_landsat(dataset, polygone):
    """ Calculer le pourcentage de nuage sur une zone
    dataset : chemin vers raster data
    geom_utm : le chemin vers le polygone en kmz
    """
    # src_transform = dataset.transform
    # position et dimension fenetre
    """win_geom_utm = rasterio.windows.from_bounds(*bounds_geom_utm, src_transform)
    win_geom_utm = win_geom_utm.round_offsets().round_lengths()
    w = src.read(1, window=win_geom_utm)
    win_transform = src.window_transform(win_geom_utm)"""

    poly = lire_kmz(polygone)
    d_rast = attr_qb(dataset)

    # reprojeter le polygone en espg 32621
    geom_utm = poly.to_crs(d_rast['crs'])
    # limites du buffer 5000 m ?
    bounds_geom_utm = geom_utm.buffer(5000).total_bounds
    # position et dimension fenetre, arrondi
    win_geom_utm = rasterio.windows.from_bounds(*bounds_geom_utm, transform=d_rast['transform'])
    win_geom_utm = win_geom_utm.round_offsets().round_lengths()

    # extraire donnee fenetre
    with rasterio.open(dataset) as src:
        w = src.read(1, window=win_geom_utm)
        win_transform = src.window_transform(win_geom_utm)

    # rasterisation
    mask_zu = features.rasterize(
        geom_utm,
        out_shape=w.shape,
        fill=1,
        transform=win_transform,
        all_touched=True,
        default_value=0,
        dtype=np.uint8
    )
    mw = ma.masked_array(w, mask=mask_zu)

    ma_values, values_counts = np.unique(mw, return_counts=True)
    values = ma_values.compressed()
    values_counts = values_counts[~ma_values.mask]
    is_cloud_shadow = apply_binary_mask(values, [0b0000001000011110])
    nb_pixels_cloud_shadow = np.sum(values_counts[is_cloud_shadow])
    nb_pixels_data = np.sum(values_counts)
    return (nb_pixels_data, nb_pixels_cloud_shadow)


def calc_p_nuages_sentinel2(dataset, polygone):
    """ Calculer le pourcentage de nuage sur une zone
    dataset : chemin vers raster data
    geom_utm : le chemin vers le polygone en kmz
    """
    # src_transform = dataset.transform
    # position et dimension fenetre
    """win_geom_utm = rasterio.windows.from_bounds(*bounds_geom_utm, src_transform)
    win_geom_utm = win_geom_utm.round_offsets().round_lengths()
    w = src.read(1, window=win_geom_utm)
    win_transform = src.window_transform(win_geom_utm)"""

    poly = lire_kmz(polygone)
    d_rast = attr_qb(dataset)

    # reprojeter le polygone en espg 32621
    geom_utm = poly.to_crs(d_rast['crs'])
    # limites du buffer 5000 m ?
    bounds_geom_utm = geom_utm.buffer(5000).total_bounds
    # position et dimension fenetre, arrondi
    win_geom_utm = rasterio.windows.from_bounds(*bounds_geom_utm, transform=d_rast['transform'])
    win_geom_utm = win_geom_utm.round_offsets().round_lengths()

    # extraire donnee fenetre
    with rasterio.open(dataset) as src:
        w = src.read(1, window=win_geom_utm)
        win_transform = src.window_transform(win_geom_utm)

    # rasterisation
    mask_zu = features.rasterize(
        geom_utm,
        out_shape=w.shape,
        fill=1,
        transform=win_transform,
        all_touched=True,
        default_value=0,
        dtype=np.uint8
    )
    mw = ma.masked_array(w, mask=mask_zu)

    ma_values, values_counts = np.unique(mw, return_counts=True)
    values = ma_values.compressed()
    values_counts = values_counts[~ma_values.mask]
    is_cloud_shadow = apply_binary_mask(values, [0b00010001])
    nb_pixels_cloud_shadow = np.sum(values_counts[is_cloud_shadow])
    nb_pixels_data = np.sum(values_counts)
    return (nb_pixels_data, nb_pixels_cloud_shadow)


def lire_kmz(path_kmz):
    """ lire un fichier KMZ
    path_kmz : chemin vers le fichier kmz
    """
    gdf = gpd.read_file(path_kmz, driver='LIBKML')
    return gdf.geometry


def apply_binary_mask(values, compare_mask):
    """Compte le nombre total de valeurs correspondant au masque binaire
    values : table de valeurs
    compare_mask : masque binaire
    """
    values2 = np.bitwise_and(values, compare_mask)
    return (values2 != 0)


def attr_qb(path_tif):
    with rasterio.open(path_tif) as src:
        dict_qb = src.meta.copy()
    nom_fichier = basename(path_tif)
    l_nom = nom_fichier.split('_')
    dict_qb.update({
        'sensor': l_nom[0],
        'geom_proc_level': l_nom[1],
        'pathrow': l_nom[2],
        'date': l_nom[3]
    })
    return dict_qb


# Activer fiona driver pour KML / KMZ
gpd.io.file.fiona.drvsupport.supported_drivers["LIBKML"] = 'r'
# chemin vers les données d'entrées
directory = "/home/fouzai/chaineTraitement/test/"

geom_path = [f for f in listdir(directory) if f.lower().endswith("kmz")][0]
print(join(directory, geom_path))
# charger la zone d'interet
aoi = join(directory, geom_path)

# trouver tout les rasters
files = os.listdir(directory)
tifs = [filename for filename in files if filename.lower().endswith("tif")]
# calculer les pourcentages
# charger l'image
for i in range(len(tifs)):
    # print(join(directory,tifs[i]))
    path = join(directory, tifs[i])
    surf = calc_p_nuages_sentinel2(path, aoi)
    print(tifs[i], surf)


