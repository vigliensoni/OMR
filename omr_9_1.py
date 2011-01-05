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
from gamera import classify

from gamera import knn
import os
import math


################################
### RETRIEVING STAFF POSITION
### Gabriel Vigliensoni
### 2010.09.15
################################


init_gamera()

stavelines = []
glyph_list = []

notes = ['F','E','D','C','B','A','G','F','E','D','C','B','A','G','F','E','D','C','B'] # ['C','D','E','F','G','A','B'] #notes = ['0','1','2','3','4','5','6','7','8','9','10','11','12']  # 
neume_down = ['punctum', 'virga', 'clivis', 'cephalicus', 'porrectus']
neume_up = ['podatus', 'epiphonus', 'scandicus', 'torculus', 'quilisma']

note = 0
notecode = notes[note]

image = load_image(r"/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Liber_Usualis/143__only_staves.tiff") #157
image = image.to_onebit()
print str(image.ncols) + ' * ' + str(image.nrows)
#print image.nrows

sf = stafffinder_miyao.StaffFinder_miyao(image)
sf.find_staves()
st_space = sf.staffspace_height
print 'StaffSpace is ', st_space

staves = sf.get_average()
#polygon = sf.get_polygon()
#print polygon
no_of_staves = 4
er = 0 # number of errors in the page (understanding errors as glyphs which are n.cols<10 and n.rows<10)

################################
### RETRIEVING LINE POSITION AND CREATING SPACES POSITION
### Gabriel Vigliensoni
### 2010.09.30
################################


for i, staff in enumerate(staves): ####### LINES AND SPACES STARTING AS 0 ONE LINE ABOVE THE STAFF. SO THE FIRST LINE IS NUMBER 3, SECOND 5, ETC.
	for j in range(no_of_staves-1):
		print staff[j].average_y, (staff[j].average_y + staff[j+1].average_y)/2, staff[j+1].average_y
		#print
		stavelines.append([i+1, (j+1)*2+1, staff[j].average_y])
		stavelines.append([i+1, (j+1)*2+2, (staff[j].average_y + staff[j+1].average_y)/2]) ### 0.5 for making a round up
		#stavelines.append([i+1, (j+1)*2+2, staff[j+1].average_y])
	p3 = staves[i][0].average_y
	p5 = staves[i][1].average_y
	p7 = staves[i][2].average_y
	p9 = staves[i][3].average_y
	stavelines.append([i+1, 0, (3 * p3 - p5)/2 - (p5 - p3)]) ### 0 
	stavelines.append([i+1, 1, (2 * p3 - p5)]) ### 1 OK ### EXTRA LINES AND SPACES
	stavelines.append([i+1, 2, (3 * p3 - p5)/2]) ### 2
	stavelines.append([i+1, 9, p9])              ### 9
	stavelines.append([i+1,10, (3 * p9 - p7)/2]) ### 10
	stavelines.append([i+1,11, (2 * p9 - p7)]) ### 11
	stavelines.append([i+1,12, (5 * p9 - 3 * p7)/2]) ### 12
	
stavelines.sort()
print stavelines

musicstaves_no_staves = musicstaves.MusicStaves_rl_fujinaga(image, 0, 0)
musicstaves_no_staves.remove_staves(u'all', no_of_staves)
image_no_st = musicstaves_no_staves.image

gid = ''

################################
### RETRIEVING GLYPH NAMES
### Gabriel Vigliensoni
### 2010.09.15
################################


neume_count = 0
actual_glyph_name = []

def up_or_down(glyph, kind): ### Is the glyph an UP or a DOWN
	if glyph == 'punctum' and kind == 'verticalepisema': ### Fisrt, the criteria for punctums (that can be U or D)
		return 'D'
	elif glyph == 'punctum' and kind == 'dot':
		return 'U'
		
	for n in neume_down:								### Then, all the other neumes
		if glyph == n:
			return 'D'
	for n in neume_up:

		if glyph == n:
			return 'U'
	return


print 'CLASSIFYING'
cknn = knn.kNNInteractive([], ["area", "aspect_ratio", "black_area", "compactness", "moments", "ncols_feature", "nholes", "nholes_extended", "nrows_feature", "skeleton_features", "top_bottom", "volume", "volume16regions", "volume64regions", "zernike_moments"], 8) #int k
print '		a'
cknn.from_xml_filename('/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Liber_Usualis/_classifier_training/154_corrected/classifier_glyphs.xml') #154
print '		b'
cknn.load_settings('/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Liber_Usualis/_classifier_training/154_corrected/classifier_settings.xml')
print '		c'
#image = load_image(r'/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Pitch_Recognition/127__no_staves.tiff') 

ccs = image_no_st.cc_analysis()

#cknn.classify_list_automatic(ccs)
#for co in ccs:
#	print co.get_main_id()

grouping_function = classify.ShapedGroupingFunction(16) # maximum solveable subgraph size
class_im = cknn.group_and_update_list_automatic(ccs, grouping_function, max_parts_per_group = 8)

for c in class_im:
	#print c.get_main_id()
	staff_number = '' 
	uod = ''
	staff_number = '' # Comment for have the non-neumes in position
	line_number = ''
	note = ''
	#print c
	if c.nrows<10 and c.ncols<10: # If error found
		er = er + 1
	else:
		sep_c = c.get_main_id().split('.')
	#	print sep_c
		if len(sep_c) <= 3:
			for i in range(3-len(sep_c)):
				sep_c.append('')
		if sep_c[0] == 'neume':
			uod = up_or_down(sep_c[1], sep_c[2])
			neume_count = neume_count + 1
			for i, stave in enumerate(stavelines):
				#print i, 
				if uod == 'D':
					if -4 <= stave[2] - c.offset_y <= (st_space/2):						# was only smaller that ...
						staff_number = stave[0]
						line_number = stave[1]
						note = notes[line_number]
						break
				elif uod == 'U':
					if -4 <= stave[2] - (c.offset_y + c.nrows) <= (st_space/2):			# was only smaller that ...
						staff_number = stave[0]
						line_number = stave[1]-1
						note = notes[line_number]
						break
		elif sep_c[0] == 'clef':
			for stave in stavelines:
				if abs((c.offset_y + c.nrows/2) - stave[2]) <= 4:
					staff_number = stave[0]
					line_number = stave[1]
		else:
			uod = ''
			staff_number = '' # Comment for have the non-neumes in position
			line_number = ''
			note = ''
	
		glyph_kind = sep_c[0]
		actual_glyph = sep_c[1]	
		glyph_char = sep_c[2:]
		glyph_list.append([staff_number, c.offset_x, c.offset_y, note, line_number, glyph_kind, actual_glyph, glyph_char, uod, c.ncols, c.nrows])

glyph_list.sort()
#print glyph_list


clef_dif = 0
for i, gc in enumerate(glyph_list):
	#print 'antes', glyph_list[i]

	if glyph_list[i][5] == 'clef' and glyph_list[i][6] == 'c':
		clef_dif = glyph_list[i][4] + 0
		print 'clef c', clef_dif
	elif glyph_list[i][5] == 'clef' and glyph_list[i][6] == 'f':
		clef_dif = glyph_list[i][4] - 3
		print 'clef f', clef_dif
	elif glyph_list[i][5] == 'neume' and glyph_list[i][0] != '':
		#print 'neume', i, glyph_list[i]
		glyph_list[i][3] = notes[glyph_list[i][4] + clef_dif]
	
	#print 'despues', glyph_list[i]
	print 'neume', i, glyph_list[i]
	
print 'There are', len(class_im), 'recognized glyphs,', neume_count, 'neumes, and ', er, 'errors'


	

