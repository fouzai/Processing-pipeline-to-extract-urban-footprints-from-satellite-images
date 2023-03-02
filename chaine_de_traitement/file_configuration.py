from os import listdir
from os.path import join
import os
import shutil
def s2_file_band(file, band) :
    """

    :param file: chemin vers le répertoire qui contient les donnees S2
    :param band: liste qui decrit le nombre de band
    :return: chemin vers le dossier de sortie
    """
    files = os.listdir(file)
    band_path = join(os.path.split(file)[0],"bandes_s2")
    os.mkdir(band_path)
    list = []
    for i in range (len(files)) :
        if(files[i].lower().startswith("sentinel2") and files[i].lower().endswith("-0") ) :
            #print(files[i])
            pth = join(file,files[i])
            for j in range(len(band)) :
                path1 = files[i] + '_FRE_B'+ str(band[j]) + ".tif"
                path_final = join(pth,path1)
                path_copy = join(band_path,path1)
                shutil.copyfile(path_final,path_copy)
                list.append(path_final)
    if (len(list)==0) :
        print("pas de données sentinel 2 maja")
    else :
        return band_path


def s2_file_clm(file):
    files = os.listdir(file)
    band_path = join(os.path.split(file)[0],"masque_clm")
    os.mkdir(band_path)

    for i in range (len(files)) :
        if(files[i].lower().startswith("sentinel2") and files[i].lower().endswith("-0") ) :
            #print(files[i])
            pth = join(file,files[i],'MASKS')
            ch = files[i] + "_CLM_R1.tif"
            pth_src = join(pth,ch)
            pth_copy = join(band_path,ch)
            shutil.copyfile(pth_src,pth_copy)



    return pth_copy



path = "/home/fouzai/chaineTraitement/s2_maja"
band = [2,4]
#res=s2_file_band(path,band)
#print(res)
print(s2_file_clm(path))