from gamera.toolkits.aruspix.ax_file import AxFile
from gamera.toolkits.aruspix.ax_page import AxPage
from gamera.toolkits.aruspix.ax_staff import AxStaff


from gamera.core import *
from gamera.toolkits import musicstaves
from gamera.toolkits.musicstaves import stafffinder_miyao
#from gamera.toolkits.musicstaves import musicstaves_rl_fujinaga
#from gamera.toolkits.musicstaves import MusicStaves_linetracking as MusicStaves

from gamera.gui import gui
from gamera.gui.matplotlib_support import *
from gamera import knn
import os

################################
### RETRIEVING STAFF POSITION
### Gabriel Vigliensoni
### 2010.09.15
################################


init_gamera()

stavelines = []
#stafflines = {}
#glyphs_dict = {}
notes = ['C','B','A','G','F','E','D'] ## ['C','D','E','F','G','A','B']
note = 0
notecode = notes[note]

image = load_image(r"/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Liber_Usualis/127__only_staves.tiff")
image = image.to_onebit()
print str(image.ncols) + ' * ' + str(image.nrows)
#print image.nrows

sf = stafffinder_miyao.StaffFinder_miyao(image)
sf.find_staves()
st_space = sf.staffspace_height
print 'StaffSpace is ', st_space

staves = sf.get_average()
#polygon = sf.get_polygon()

for i, staff in enumerate(staves):
#	print "Staff %d has %d staves:" % (i+1, len(staff))
	
	for j, line in enumerate(staff):
#		print "    %d. line at y-position:" % (j+1), line.average_y
		stavelines.append([i+1, j+1, line.average_y])
		#stafflines.append(i, j, average_y)
#		print "Its positions is " + str(polygon[i][j].vertices) 
print stavelines
#print stafflines

musicstaves_no_staves = musicstaves.MusicStaves_rl_fujinaga(image, 0, 0)
musicstaves_no_staves.remove_staves(u'all', 4)
image_no_st = musicstaves_no_staves.image

print '1'


################################
### RETRIEVING GLYPH NAMES
### Gabriel Vigliensoni
### 2010.09.15
################################

neume_down = ['punctum', 'virga', 'clivis', 'cephalicus', 'porrectus']
neume_up = ['podatus', 'epiphonus', 'scandicus', 'torculus', 'quilisma']
neume_count = 0
actual_glyph_name = []



cknn = knn.kNNInteractive([], ["area", "aspect_ratio", "black_area", "compactness", "moments", "ncols_feature", "nholes", "nholes_extended", "nrows_feature", "skeleton_features", "top_bottom", "volume", "volume16regions", "volume64regions", "zernike_moments"], 0)
cknn.from_xml_filename('/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Liber_Usualis/_classifier_training/132/classifier_glyphs.xml')
#image = load_image(r'/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Pitch_Recognition/127__no_staves.tiff') 154
print '2'
ccs = image_no_st.cc_analysis()
print '3'
cknn.classify_list_automatic(ccs)
print '4'
for c in ccs:
	if c.get_main_id()[:6] == 'neume.':
		neume_count = neume_count + 1
		
		
		for l, letter in enumerate(c.get_main_id()[6:]):

			if letter == '.':
				actual_glyph_name = c.get_main_id()[6:6+l]
				print 'Not recognized yet', c.get_main_id()[6:], actual_glyph_name
				break
		if actual_glyph_name == neume_up:
			actual_glyph_name = ['oooops']
			
		
		 
		for i, line in enumerate(stavelines):
			dif = (line[2] - c.offset_y)				### THIRD ELEMENT OF THE LIST IS LINE Y-POSITION
			if 0 < dif < (st_space/3): 						### FIND THE OPTIMAL DIFFERENCE DEPENDING IN THE STAFFLINES HEIGHT
				print 'Neume', c.label, (c.get_main_id()[6:]), 'in staff', line[0], 'line', line[1], 'note', notes[((line[1]-1)*2)], c
				break
		#print
#	else:
#		print c.label, c.get_main_id(), c

print 'There are', len(ccs), 'recognized glyphs and', neume_count, 'notes'

def xul(a):
	return a
	
xul(2)
