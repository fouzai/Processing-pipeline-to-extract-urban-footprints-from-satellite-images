from main_chaine_traitement import chaineTraitement
from file_configuration import s2_file_band, s2_file_clm

w_size_foto = 11
w_size_var = 21
methode_foto = 'block'
threshold = 0.3
c_mask = 0b00010001

# chemin vers les données en entrée
path = "/home/fouzai/chaineTraitement/s2_maja"

# chemin vers la region d interet
aoi = "/home/fouzai/chaineTraitement/Saint-Laurent-du-Maroni.kmz"


# chemin vers le date de sortie
output_date = "/home/fouzai/chaineTraitement/output.txt"


# chemin vers les données d'entrées : les images
band = [2,3]
#input_directory = s2_file_band(path, band)
#input_directory ='/home/fouzai/chaineTraitement/test/'
# chemin vers les données d'entrées : les masques CLM
#mask_directory = s2_file_clm(path)
#mask_directory ='/home/fouzai/chaineTraitement/clm_band/'

# chemin vers le dossier de sortie
#output_directory = '/home/fouzai/chaineTraitement/res/'
# chemin vers le dossier de masque binaire
#mask_directory1 ='/home/fouzai/chaineTraitement/mask/'






chaineTraitement(path, aoi, output_date, c_mask, w_size_foto, w_size_var, methode_foto, threshold)