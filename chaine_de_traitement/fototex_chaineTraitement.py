import os
from fototex.foto import Foto, FotoSector, FotoBatch, FotoSectorBatch
from fototex.foto_tools import degrees_to_cardinal
import numpy as np
from matplotlib import pyplot as plt
from skimage import io

def foto_traitement(input_raster, w_size_f, methode_foto, w_size_v, threshold):
    """" traitement des sortie de fototex pour détécter la tahce urbaine
    input_raster : chemin vers le raster
    w_size_f : taille de la fenetre d'analyse de fototex
    methode_f : methode de fototex : block ou moving_window
    w_size_v : taille de la fenetre pour calculer la variance
    threshold : seuil de seuillage de la variance
    """
    image_file = os.path.join(input_raster)
    sample_image = io.imread(image_file)

    foto_obj = Foto(image_file, band=1, method=methode_foto, in_memory=True)

    foto_obj.run(window_size=w_size_f, keep_dc_component=False)
    foto_obj.save_rgb()
    raster = io.imread(foto_obj.rgb_file)

    import otbApplication
    output_variance = os.getcwd() + '/variance.tif'
    ch = 'var(im1b1N' + str(w_size_v) + 'x' + str(w_size_v) + ')'
    app = otbApplication.Registry.CreateApplication("BandMathX")

    app.SetParameterStringList("il", [foto_obj.rgb_file])
    app.SetParameterString("out", output_variance)
    app.SetParameterString("exp", ch)

    app.ExecuteAndWriteOutput()

    print("Calcul variance OK", output_variance)

    import otbApplication
    #output_traitement = os.getcwd() + '/tache_urbaine.tif'
    output_traitement = image_file[:-4] + '_tache_urbaine.tif'
    print(" traitement chemin ", output_traitement)
    ch1 = "im1b1 >= " + str(threshold) + " ? 1 : 0 "
    app = otbApplication.Registry.CreateApplication("BandMath")

    app.SetParameterStringList("il", [output_variance])
    app.SetParameterString("out", output_traitement)
    app.SetParameterString("exp", ch1)

    app.ExecuteAndWriteOutput()
    os.remove(output_variance)
    return ("tache urbaine : ", output_traitement)


