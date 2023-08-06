import funciones
import tifffile
import numpy as np


f = str('/home/bruno/Documentos/TESIS/TESIS/Experimentos/exp_bordes/img_1x1/lsm/exp_1x1_melanoma_1.lsm')
im = tifffile.imread(f)
g, s, md, ph, dc = funciones.phasor(im, harmonic=1)

bins = np.arange(0, 256, 1)
Ro = 0.1

# Pruebas de las fuciones interactive y components_histogram
# funciones.interactive(dc, g, s, Ro)
# funciones.histogram_line(Ro, g, s, dc, 50)

# Prueba de la funcion phaso_plot para ambos casos con un solo phasor y con mas de uno
# funciones.phasor_plot([dc], [g], [s], [50])
# funciones.phasor_plot([dc, dc, dc], [g, g, g], [s, s, s], [5, 50, 100], same_phasor=True)
# plt.show()
