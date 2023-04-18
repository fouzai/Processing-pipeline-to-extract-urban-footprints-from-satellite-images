from os import listdir
from os.path import join


def extract_xml_file(input_file) :
    """" retourner le chemin d'un fichier xml dans un dossier
    input_file : chemin vers un repertoire
    """
    files = listdir(input_file)
    for i in range(len(files)) :
        if files[i].lower().endswith(".xml") :
            if files[i].find("aux")== -1 or files[i].find("tif")== -1:
                return join(input_file,files[i])



dir = "/home/fouzai/chaineTraitement/s2_maja/SENTINEL2A_20200115-141049-119_L2A_T21NZG_C_V1-0"

#extract_xml_file(dir)
#ch = extract_xml_file(dir)
#print(ch)


def xml_char(x):
    return (x[-49:-41])


def return_path(directory) :
    """" creer une liste avec les chemins des fichiers xml
    directory : repertoire qui contient les images sentinel 2 maja
    """
    files = listdir(directory)
    path_xml = []
    for i in range(len(files)) :
        if (files[i].lower().endswith("v1-0") or files[i].lower().startswith("sentinel2") ) :
            file_path = join(directory,files[i])
            path_xml.append(extract_xml_file(file_path))

    path_xml_sorted = sorted(path_xml, key=xml_char, reverse=True)

    return path_xml_sorted


def create_wasp_script(file, date_output, path_output) :
    """ creer le script pour faire tourner wasp
    file : liste avec les chemins vers les fichiers xml
    date_output : date de sortie de waso de la forme YYYYMMDD
    path_output : dossier de sortie
    """
    f = open("/home/fouzai/chaineTraitement/script.txt", "w")
    f.write("./bin/WASP \ ")
    f.write("\n")
    f.write("--input ")
    for lines in file :
        f.write(lines)
        f.write(" \ ")
        f.write("\n")
    f.write("--out ")
    f.write(path_output)
    f.write(" \ ")
    f.write("\n")
    f.write("--date ")
    f.write(date_output)
    f.write(" \ ")
    f.write("\n")
    f.write("--synthalf 23 \ ")
    f.close()


date = "20200320"
path = "/home/fouzai/chaineTraitement/wasp_resultat"

print(return_path("/home/fouzai/chaineTraitement/s2_maja"))
file= return_path("/home/fouzai/chaineTraitement/s2_maja")
create_wasp_script(file, date, path)