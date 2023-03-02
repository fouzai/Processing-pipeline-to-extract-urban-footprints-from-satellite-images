from main_chaine_traitement import chaineTraitement
from file_configuration import s2_file_band, s2_file_clm



# chemin vers les données en entrée
path = "/home/fouzai/chaineTraitement/s2_maja"

# chemin vers la region d interet
aoi = "/home/fouzai/chaineTraitement/Saint-Laurent-du-Maroni.kmz"


# chemin vers le date de sortie
output_date = "/home/fouzai/chaineTraitement/output.txt"


#parametres foto + traitement
band = [2,3]
w_size_foto = 11
w_size_var = 21
methode_foto = 'block'
threshold = 0.3
c_mask = 0b00010001




chaineTraitement(path, aoi, output_date, c_mask, w_size_foto, w_size_var, methode_foto, threshold,band)