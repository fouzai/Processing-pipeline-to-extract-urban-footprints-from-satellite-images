# calculer le pourcentage de nuage
calc_p_nuages_sentinel2_file(path, aoi,"pourcentages.csv")

from TimeSeriesImageGapfilling_chaineTraitement import GapFilling
# chemin vers les données d'entrées : les images
input_directory ='/home/fouzai/chaineTraitement/test/'
# chemin vers les données d'entrées : les masques
mask_directory ='/home/fouzai/chaineTraitement/mask/'

# chemin vers le dossier de sortie
output_directory = '/home/fouzai/chaineTraitement/res/'

# chemin vers le date de sortie
output = "/home/fouzai/chaineTraitement/output.txt"

# créér un gapfilling à une date t donnée
GapFilling(input_directory, mask_directory, output_directory, output)