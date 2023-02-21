import os
from os.path import join
import pandas as pd

from TimeSeriesImageGapfilling_chaineTraitement import GapFilling
from fototex_chaineTraitement import foto_traitement
from creation_masque_nuage_chaineTraitement import cloud_mask
from calcul_pourcentage_nuage_chaineTraitement import calc_p_nuages_sentinel2_csv


def chaineTraitement(input_image, input_mask, output_file, resultat_file, aoi, output_date, c_mask, wsize_f, wsize_v, meth_foto, threshold) :

    cloud_mask(input_mask, output_file,c_mask)
    csv_path = calc_p_nuages_sentinel2_csv(output_file, aoi)
    print(csv_path)
    df = pd.read_excel(csv_path,engine='openpyxl')
    pnuage_min = min(df['pourcentage_nuage'])
    print(pnuage_min)
    if (pnuage_min < 5 ) :
        gapfilling_path = GapFilling(input_image, output_file, resultat_file, output_date)

        foto_traitement(gapfilling_path,resultat_file, wsize_f, meth_foto, wsize_v, threshold)
        print(" resultat OK")
    else :
        print(" pas de Gapfilling")
        df1 = df.loc[df['pourcentage_nuage']==pnuage_min]
        print ('au moins une image qui contient moins de 5% de nuage : ')
        print("l image qui contient le moins de nuages : ")
        print(df1.iloc[0]['identifiant_image'])
        ch_identifiant = df1.iloc[0]['identifiant_image'] [:-16]
        print(ch_identifiant)
        files = os.listdir(input_image)
        print(files)
        band = 0
        file_image = []
        for i in range(len(files)) :
            if (files[i].startswith(ch_identifiant)) :
                print(files[i])
                band = band + 1
                file_image.append(files[i])

        print(band)
        if (band == 1 ) :
            path_image = join(input_image, file_image[0])
            print(path_image)
            foto_traitement(path_image,resultat_file, wsize_f, meth_foto, wsize_v, threshold)
            print(" resultat OK")

        else :
            print("traitement a venir")
            b = input('traitement de la tache urbaine avec quelle bande ?')
            ch_identifiant_final = ch_identifiant + '_FRE_B'+b+'.tif'
            path_image = join(input_image,ch_identifiant_final)
            print(path_image)
            foto_traitement(path_image,resultat_file, wsize_f, meth_foto, wsize_v, threshold)






