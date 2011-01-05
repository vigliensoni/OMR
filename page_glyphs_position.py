from gamera.gui import gui
from gamera.gui.matplotlib_support import *
from gamera.core import *
init_gamera()



from gamera import knn
cknn = knn.kNNInteractive([], ["area", "aspect_ratio", "black_area", "compactness", "moments", "ncols_feature", "nholes", "nholes_extended", "nrows_feature", "skeleton_features", "top_bottom", "volume", "volume16regions", "volume64regions", "zernike_moments"], 0)
cknn.from_xml_filename('/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Liber_Usualis/_classifier_training/154/classifier_glyphs.xml')
image = load_image(r'/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Pitch_Recognition/127__no_staves.tiff')
ccs = image.cc_analysis()
cknn.classify_list_automatic(ccs)
for c in ccs:
	print c.label, c.get_main_id(), c
	