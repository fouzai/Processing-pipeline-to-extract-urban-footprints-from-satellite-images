#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youssef.fouzai@ird.fr
"""

from os import listdir
import geopandas as gpd
from os.path import join
import os
import numpy as np
import rasterio
from os.path import join, basename
from rasterio import features
import numpy.ma as ma
import pandas as pd


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
    is_cloud_shadow = apply_binary_mask(values, [0b00000001])
    nb_pixels_cloud_shadow = np.sum(values_counts[is_cloud_shadow])
    nb_pixels_data = np.sum(values_counts)
    return nb_pixels_data, nb_pixels_cloud_shadow


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
    return nb_pixels_data, nb_pixels_cloud_shadow


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
    return values2 != 0


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


def extraire_date(prodid):
    date1 = prodid
    return({
        'dateprod': date1[11:19],
        'yearprod': date1[11:15],
        'monthprod': date1[15:17]})


def extraire_date_landsat(prodid):
    date1 = prodid
    return({
        'dateprod': date1[17:25],
        'yearprod': date1[17:21],
        'monthprod': date1[21:23]})


def calc_p_nuages_sentinel2_csv(input_dir,geom_path):
    """"Calculer le pourcentage de nuage sur une zone d interet et sauvegarder le resultat dans un fichier xlsx
    input_dir : chemin vers le dossier qui contient les masques de nuage
    geom_path : le chemin vers le polygone en kmz
    """
    # Activer fiona driver pour KML / KMZ
    gpd.io.file.fiona.drvsupport.supported_drivers["LIBKML"] = 'r'
    aoi = geom_path
    files = os.listdir(input_dir)
    tifs = [filename for filename in files if filename.lower().endswith("tif")]
    df = pd.DataFrame(columns=['identifiant_image', 'dateprod', 'yearprod', 'monthprod', 'surface_totale', 'syrface_nuage','pourcentage_nuage'])
    for i in range(len(tifs)):
        # print(join(directory,tifs[i]))
        path = join(input_dir, tifs[i])
        surf = calc_p_nuages_sentinel2(path, aoi)
        # print(tifs[i], surf)
        # print(extraire_date(tifs[i]))
        # new_row = [tifs[i],]
        k = extraire_date(tifs[i])
        pource = (surf[1] / surf[0]) * 100
        new_row = [tifs[i], k["dateprod"], k["yearprod"], k["monthprod"], surf[0], surf[1], pource]
        df.loc[len(df)] = new_row

    pth_export = join(input_dir, "pourcentage_nuage.xlsx")
    df.to_excel(pth_export)
    return pth_export


def calc_p_nuages_landsat_csv(input_dir,geom_path):
    """"Calculer le pourcentage de nuage sur une zone d interet et sauvegarder le resultat dans un fichier xlsx
    input_dir : chemin vers le dossier qui contient les masques de nuage
    geom_path : le chemin vers le polygone en kmz
    """
    # Activer fiona driver pour KML / KMZ
    gpd.io.file.fiona.drvsupport.supported_drivers["LIBKML"] = 'r'
    aoi = geom_path
    files = os.listdir(input_dir)
    tifs = [filename for filename in files if filename.lower().endswith("tif")]
    df = pd.DataFrame(columns=['identifiant_image', 'dateprod', 'yearprod', 'monthprod', 'surface_totale', 'surface_nuage','pourcentage_nuage'])
    for i in range(len(tifs)):
        # print(join(directory,tifs[i]))
        path = join(input_dir, tifs[i])
        surf = calc_p_nuages_landsat(path, aoi)
        # print(tifs[i], surf)
        # print(extraire_date(tifs[i]))
        # new_row = [tifs[i],]
        k = extraire_date_landsat(tifs[i])
        pource = (surf[1] / surf[0]) * 100
        new_row = [tifs[i], k["dateprod"], k["yearprod"], k["monthprod"], surf[0], surf[1], pource]
        df.loc[len(df)] = new_row

    pth_export = join(input_dir, "pourcentage_nuage.xlsx")
    df.to_excel(pth_export)
    return pth_export



