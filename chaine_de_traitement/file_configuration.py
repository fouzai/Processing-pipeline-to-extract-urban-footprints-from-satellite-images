from os import listdir
from os.path import join
import os
import shutil

def verif_sentinel(file_image) :
    files = os.listdir(file_image)
    if (files[0].lower().startswith("sentinel") and files[0].lower().endswith("-0")) :
        return True
    else:
        return False





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



    return band_path



def Landsat_file_qa(file):
    files = os.listdir(file)
    band_path = join(os.path.split(file)[0],"masque_qa")
    os.mkdir(band_path)

    for i in range (len(files)) :
        if((files[i].lower().startswith("lc") or  files[i].lower().startswith("lt")) and (files[i].lower().endswith("t1") or  files[i].lower().endswith("t2")) ) :
            #print(files[i])
            print("ok")
            pth = join(file, files[i])
            ch = files[i] + "_QA_PIXEL.TIF"
            pth_src = join(pth, ch)
            pth_copy = join(band_path,ch)
            shutil.copyfile(pth_src,pth_copy)



    return band_path




def landsat_file_band(file, band) :
    """

    :param file: chemin vers le répertoire qui contient les donnees landsat
    :param band: liste qui decrit le nombre de band
    :return: chemin vers le dossier de sortie
    """
    files = os.listdir(file)
    band_path = join(os.path.split(file)[0],"bandes_landsat")
    os.mkdir(band_path)
    list = []
    for i in range (len(files)) :
        if(files[i].lower().startswith("l")) :
            #print(files[i])
            pth = join(file,files[i])
            for j in range(len(band)) :
                path1 = files[i] + '_SR_B'+ str(band[j]) + ".TIF"
                path_final = join(pth,path1)
                path_copy = join(band_path,path1)
                shutil.copyfile(path_final,path_copy)
                list.append(path_final)
    if (len(list)==0) :
        print("pas de données Landsat")
    else :
        return band_path









#path = "/home/fouzai/chaineTraitement/s2_maja"
#band = [2,4]
#res=s2_file_band(path,band)
#print(res)
#print(s2_file_clm(path))