
from os import listdir
from os.path import join
import os
import otbApplication
import os
import datetime
import operator as op


def create_stack_raster(input_directory):
    """" créér un stack de raster
    input_directory : chemin vers le dossier qui contient les images

    """

    def last_4chars(x):
        return (x[11:19])

    files = os.listdir(input_directory)
    files = sorted(files, key=last_char)
    file = sorted(files, key=last_4chars)

    files1 = []
    for i in range(len(file)):
        if (file[i].lower().endswith("tif")):
            files1.append(join(input_directory, file[i]))

    output_stack = join(input_directory, "stack.tif")
    app = otbApplication.Registry.CreateApplication("ConcatenateImages")
    app.SetParameterStringList("il", files1)
    app.SetParameterString("out", output_stack)
    app.ExecuteAndWriteOutput()
    print("creation stack avec succes")
    return (output_stack, file, files1)


def extractId(ch):
    """"extraire un identifiant d'une image sentinel 2
    ch : identifiant de l image
    """
    if (len(ch) == 59):
        id = ch[11:19]
    return (int(id))


def last_char(x):
    return (x[54:55])


def nombreBand(files):
    """"détérminer le nombre de bande des images dans un dossier
    files : répertoire des images
    """

    list_stack = []
    extract_id = []
    occ = []
    for i in range(len(files)):
        if (files[i].lower().endswith('tif')):
            if (files[i].lower().startswith('sentinel2')):
                list_stack.append(files[i])

    for i in range(len(list_stack)):
        extract_id.append(extractId(list_stack[i]))
    for i in range(len(extract_id)):
        occ.append(op.countOf(extract_id, extract_id[i]))
    res = occ.count(occ[0]) == len(occ)
    return (occ[0], res)


def date_output(list_id, dossier):
    """"créér un fichier texte avec les dates des images selon l'ordre chronologique à partir des identifiants des images
    list_id : une liste qui contient tous les identifiants des images
    dossier : chemin vers le répertoire pour enregistrer le fichier texte
    """
    occ, res = nombreBand(list_id)
    if (occ == 1):
        dates = []
        for i in range(len(list_id)):
            if (list_id[i].lower().endswith('tif') and list_id[i].lower().startswith('sentinel')):
                date_time_str = list_id[i][11:19]
                date_time_obj = datetime.datetime.strptime(date_time_str, '%Y%m%d')
                dates.append(date_time_obj)
        dates.sort()
        lines = dates
        path_export = join(dossier, "date.txt")
        with open(path_export, 'w') as f:
            for line in lines:
                f.write(str(line)[0:4] + str(line)[5:7] + str(line)[8:10])
                f.write('\n')
        print("creation fichier txt avec succes")
        return (path_export)
    else:
        if (res):
            new_list_id = []
            for i in range(0, len(list_id), occ):
                new_list_id.append(list_id[i])

            dates = []
            list_id = new_list_id
            for i in range(len(list_id)):
                if (list_id[i].lower().endswith('tif') and list_id[i].lower().startswith('sentinel')):
                    date_time_str = list_id[i][11:19]
                    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y%m%d')
                    dates.append(date_time_obj)
            dates.sort()
            lines = dates
            path_export1 = join(dossier, "date.txt")
            with open(path_export1, 'w') as f:
                for line in lines:
                    f.write(str(line)[0:4] + str(line)[5:7] + str(line)[8:10])
                    f.write('\n')
            print("creation fichier txt avec succes")
            return (path_export1)



        else:
            print(" nombre de bande non equivalent, une ou plusieurs bandes manque")


def GapFilling(image_directory, mask_directory, output_file, output_date):
    """"créér un Gapfilling pour une synthèse d'image sans nuages
    image_directory : chemin vers répertoire d'image
    mask_directory  : chemin vers repertoire de masques de nuage
    output_file : chemin vers le répértoire de sortie
    output_date : chemin vers un fichier texte avec la date de sortie YYMMDD
    """
    image_stack1, image_stack2, image_stack3 = create_stack_raster(image_directory)
    print("image stack :  ", image_stack2)
    mask_stack = create_stack_raster(mask_directory)
    input_date = date_output(image_stack2, output_file)
    output_file_gap = join(output_file, 'gapfilling.tif')
    print(image_stack2)
    print(mask_stack[0])
    print(output_file_gap)
    print(input_date)
    nb_comp, res = nombreBand(image_stack2)

    print("le nombre de composantes : ", type(nb_comp))

    nb_comp = int(nb_comp)

    app = otbApplication.Registry.CreateApplication("ImageTimeSeriesGapFilling")
    app.SetParameterString("in", image_stack1)
    app.SetParameterString("mask", mask_stack[0])
    app.SetParameterString("out", output_file_gap, )
    app.SetParameterInt("comp", nb_comp)
    app.SetParameterString("it", "linear")
    app.SetParameterString("id", input_date)
    app.SetParameterString("od", output_date)
    app.ExecuteAndWriteOutput()

    os.remove(image_stack1)
    os.remove(mask_stack[0])

    return (output_file_gap)

