import os
from fototex.foto import Foto, FotoSector, FotoBatch, FotoSectorBatch
from fototex.foto_tools import degrees_to_cardinal
import numpy as np
from matplotlib import pyplot as plt
from skimage import io
import otbApplication
def operation_morphologique(input_raster,type_op,r) :
    """"appliquer des operation morphologique à un raster
    input_raster : chemin vers un raster
    type_op : le type de l opertation morphologique :  dilate ou erode ou opening ou closing
    """
    path_tempo = input_raster[:-4]+'_'+ type_op + ".tif"


    app = otbApplication.Registry.CreateApplication("BinaryMorphologicalOperation")

    app.SetParameterString("in", input_raster)
    app.SetParameterString("out", path_tempo)
    app.SetParameterInt("channel", 1)
    app.SetParameterInt("xradius", r)
    app.SetParameterInt("yradius", r)
    app.SetParameterString("filter", type_op)

    app.ExecuteAndWriteOutput()

    return path_tempo


def foto_traitement(input_raster, output_directory, w_size_f, methode_foto, w_size_v, threshold):
    """" traitement des sortie de fototex pour détécter la tahce urbaine
    input_raster : chemin vers le raster
    output_directory : dossier de sortie pour sauvegarder les résultats
    w_size_f : taille de la fenetre d'analyse de fototex
    methode_f : methode de fototex : block ou moving_window
    w_size_v : taille de la fenetre pour calculer la variance
    threshold : seuil de seuillage de la variance
    """
    image_file = os.path.join(input_raster)
    sample_image = io.imread(image_file)

    foto_obj = Foto(image_file, band=1, method=methode_foto, in_memory=True)

    foto_obj.run(window_size=w_size_f, keep_dc_component=False)
    foto_obj.out_dir = output_directory
    foto_obj.save_rgb()
    raster = io.imread(foto_obj.rgb_file)


    output_variance = foto_obj.rgb_file[:-4] + '_variance.tif'
    ch = 'var(im1b1N' + str(w_size_v) + 'x' + str(w_size_v) + ')'
    app = otbApplication.Registry.CreateApplication("BandMathX")

    app.SetParameterStringList("il", [foto_obj.rgb_file])
    app.SetParameterString("out", output_variance)
    app.SetParameterString("exp", ch)

    app.ExecuteAndWriteOutput()

    print("Calcul variance OK", output_variance)


    #output_traitement = os.getcwd() + '/tache_urbaine.tif'
    output_traitement = foto_obj.rgb_file[:-4] + '_tache_urbaine.tif'
    print(" traitement chemin ", output_traitement)
    ch1 = "im1b1 >= " + str(threshold) + " ? 1 : 0 "
    app = otbApplication.Registry.CreateApplication("BandMath")

    app.SetParameterStringList("il", [output_variance])
    app.SetParameterString("out", output_traitement)
    app.SetParameterString("exp", ch1)

    app.ExecuteAndWriteOutput()
    os.remove(output_variance)

    output_dilate = operation_morphologique(output_traitement,"dilate",5)
    output_finale = operation_morphologique(output_dilate,"erode",2)

    return ("tache urbaine : ", output_finale)


