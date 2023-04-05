#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: youssef.fouzai@ird.fr
"""
from main_chaine_traitement import chaineTraitement

# Chemin vers les données d'entrée
path = "/home/fouzai/chaineTraitement/landsat_donwload"

# Chemin vers la region d'interêt
aoi = "/home/fouzai/chaineTraitement/Saint-Laurent-du-Maroni.kmz"

# Chemin vers la date de sortie
output_date = "/home/fouzai/chaineTraitement/output.txt"

# Paramètres foto + traitement
band = [2, 3]
w_size_foto = 11
w_size_var = 21
methode_foto = "block"
threshold = 0.3

chaineTraitement(path, aoi, output_date, w_size_foto, w_size_var, methode_foto, threshold, band)
