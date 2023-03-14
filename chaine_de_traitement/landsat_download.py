import os
import tarfile
from os.path import join
import os
from calcul_pourcentage_nuage_chaineTraitement import lire_kmz
import geopandas as gpd
import numpy as np
import tarfile
from eodag import EODataAccessGateway
from shapely.geometry import Polygon
geom = Polygon([[-52.25436024547791, 4.849005730128553], [-52.2342066128699, 4.87897079785489], [-52.25031858914861, 4.915304055969233], [-52.2947305585838, 4.957712521390143], [-52.3434865363878, 4.94774305865965],[-52.36586445923182,4.902414519442758],[-52.33985767679302,4.838700417255624],[-52.25436024547791 ,4.849005730128553 ]])
#gpd.io.file.fiona.drvsupport.supported_drivers["LIBKML"] = 'rw'
#geom = lire_kmz('/home/fouzai/Téléchargements/kmz_jpg_Gutemberg/Gutemberg/Cayenne.kml')
#map = gpd.read_file('/home/fouzai/Téléchargements/kmz_jpg_Gutemberg/Gutemberg/Cayenne.kml')
#df= pd.DataFram
#dag = EODataAccessGateway()

#search_results, total_count = dag.search(productType="LANDSAT_TM_C2L2", start='2010-01-01', end='2010-03-01', geom=geom)
#prod = search_results[0]
#print(search_results)
#prod.download(outputs_prefix='/home/fouzai/chaineTraitement/landsat_donwload',extract=False)

def landsat_download(file, s_date, e_date, ROI) :
    """

    :param file: path where to download the images
    :param s_date: start date
    :param e_date: end date
    :param poly: ROI kml
    """
    gpd.io.file.fiona.drvsupport.supported_drivers["LIBKML"] = 'rw'

    map = gpd.read_file(ROI)

    g = [i for i in map.geometry]
    p = g[0].boundary
    k = p.coords.xy
    res = np.dstack(k).tolist()
    new_poly = Polygon(res[0])

    dag = EODataAccessGateway()

    search_results, total_count = dag.search(productType="LANDSAT_C2L2", start=s_date, end=e_date,
                                             geom=new_poly)

    print(search_results)

    if(total_count > 0) :
        search_results[0].download(outputs_prefix=file, extract=False)
        print("ok")
    else :
        print("No product found ")

    list_file = os.listdir(file)
    for i in range(len(list_file)) :
        if list_file[i].lower().endswith('tar.gz') :
            file_gz_path = join(file,list_file[i])
            file_extract_path = join(file, list_file[i][:-7])
            ff = tarfile.open(file_gz_path)
            ff.extractall(file_extract_path)
            ff.close()
            os.remove(file_gz_path)



path_file = '/home/fouzai/chaineTraitement/landsat_donwload'
s_date = '2018-01-01'
end_date = '2018-03-01'
roi = '/home/fouzai/Téléchargements/kmz_jpg_Gutemberg/Gutemberg/Saint-Laurent-du-Maroni.kmz'

landsat_download(path_file, s_date , end_date , roi)