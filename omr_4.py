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
glyph_list = []

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

print 'a'
gid = ''

################################
### RETRIEVING GLYPH NAMES
### Gabriel Vigliensoni
### 2010.09.15
################################

neume_down = ['punctum', 'virga', 'clivis', 'cephalicus', 'porrectus']
neume_up = ['podatus.2', 'epiphonus', 'scandicus', 'torculus', 'quilisma']
neume_count = 0
actual_glyph_name = []

#def is_neume(glyph):
#	if glyph.get_main_id()[:6] == 'neume.':
#		print 'it is a NEUME'
#		return glyph
#	else:
#		glyph = glyph
#		print 'it is not a NEUME'
#		return

def up_or_down(glyph):

	gid = glyph.get_main_id()
	#print 'gid', gid
	for n in neume_down:
		#print n
		if gid == n:
			glyph = 'neume down'
			break
		#print gid, n
	for n in neume_up:
		if gid == n:
			glyph = 'neume up'
			break
		#print gid, n
	print glyph
	#else:
	#	glyph = 'orale!'
	return glyph




print 'b'

cknn = knn.kNNInteractive([], ["area", "aspect_ratio", "black_area", "compactness", "moments", "ncols_feature", "nholes", "nholes_extended", "nrows_feature", "skeleton_features", "top_bottom", "volume", "volume16regions", "volume64regions", "zernike_moments"], 0)
cknn.from_xml_filename('/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Liber_Usualis/_classifier_training/132/classifier_glyphs.xml')
#image = load_image(r'/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Pitch_Recognition/127__no_staves.tiff') 154



ccs = image_no_st.cc_analysis()

cknn.classify_list_automatic(ccs)
print 'c'
for c in ccs:
	for l, letter in enumerate(c.get_main_id()):
		glyph_family = ''
		glyph_char = ''
		if letter == '.':
			glyph_kind = c.get_main_id()[0:l]
			actual_glyph = c.get_main_id()[l+1:]
			for a, letra in enumerate(c.get_main_id()[l+1:]):
#				print a, letra
				if letra == '.':
					glyph_family = c.get_main_id()[l+1:l+1+a]
					glyph_char = c.get_main_id()[l+1+a+1:]
					break
			break
	#glyph_list.append([c.label, glyph_kind, glyph_family, glyph_char, c.offset_x, c.offset_y, c.ncols, c.nrows])
	
	glyph_list.append([c.label, glyph_kind, actual_glyph, glyph_family, glyph_char, c.offset_x, c.offset_y, c.ncols, c.nrows])
		

#	for i, line in enumerate(stavelines):
#		dif = (line[2] - c.offset_y)				### THIRD ELEMENT OF THE LIST IS LINE Y-POSITION
#		if 0 < dif < (st_space/3): 						### FIND THE OPTIMAL DIFFERENCE DEPENDING IN THE STAFFLINES HEIGHT
#			print 'Neume', c.label, (c.get_main_id()[6:]), 'in staff', line[0], 'line', line[1], 'note', notes[((line[1]-1)*2)], c
#			break
		#print
#	else:
#		print c.label, c.get_main_id(), c
for i, gc in enumerate(glyph_list):
	print glyph_list[i]
	
print 'There are', len(ccs), 'recognized glyphs and', neume_count, 'notes'


	

