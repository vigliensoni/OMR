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


################################
### RETRIEVING STAFF POSITION
### Gabriel Vigliensoni
### 2010.09.15
################################


init_gamera()

stavelines = []
glyph_list = []

notes = ['F','E','D','C','B','A','G','F','E','D','C','B','A'] ## ['C','D','E','F','G','A','B']
neume_down = ['punctum', 'virga', 'clivis', 'cephalicus', 'porrectus']
neume_up = ['podatus', 'epiphonus', 'scandicus', 'torculus', 'quilisma']

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
#		print staff[j].average_y, (staff[j].average_y + staff[j+1].average_y)/2, staff[j+1].average_y
#		print
		stavelines.append([i+1, (j+1)*2+1, staff[j].average_y])
		stavelines.append([i+1, (j+1)*2+2, (staff[j].average_y + staff[j+1].average_y)/2])
		#stavelines.append([i+1, (j+1)*2+2, staff[j+1].average_y])
	stavelines.append([i+1, 0, (staves[i][0].average_y)-3*st_space/2]) ### 0 ### EXTRA LINES AND SPACES
	stavelines.append([i+1, 1, (staves[i][0].average_y)-2*st_space/2]) ### 1
	stavelines.append([i+1, 2, (staves[i][0].average_y)-1*st_space/2]) ### 2
	stavelines.append([i+1, 9, (staves[i][3].average_y)])              ### 9
	stavelines.append([i+1,10, (staves[i][3].average_y)+1*st_space/2]) ### 10
	stavelines.append([i+1,11, (staves[i][3].average_y)+2*st_space/2]) ### 11
	stavelines.append([i+1,12, (staves[i][3].average_y)+3*st_space/2]) ### 12
	
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


print 'b'

cknn = knn.kNNInteractive([], ["area", "aspect_ratio", "black_area", "compactness", "moments", "ncols_feature", "nholes", "nholes_extended", "nrows_feature", "skeleton_features", "top_bottom", "volume", "volume16regions", "volume64regions", "zernike_moments"], 0)

cknn.from_xml_filename('/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Liber_Usualis/_classifier_training/132/classifier_glyphs.xml') #154
cknn.load_settings('/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Liber_Usualis/_classifier_training/132/classifier_settings.xml')
#image = load_image(r'/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Pitch_Recognition/127__no_staves.tiff') 



ccs = image_no_st.cc_analysis()

#cknn.classify_list_automatic(ccs)
#for co in ccs:
#	print co.get_main_id()

grouping_function = classify.ShapedGroupingFunction(12)
class_im = cknn.group_and_update_list_automatic(ccs, grouping_function, max_parts_per_group = 12)

print 'c'

#print class_im
#print ccs


for c in class_im:
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


		else:
			uod = ''
			staff_number = '' # Comment for have the non-neumes in position
			line_number = ''
			note = ''
	
		glyph_kind = sep_c[0]
		actual_glyph = sep_c[1]	
		glyph_char = sep_c[2]



		for i, stave in enumerate(stavelines):
			if uod == 'D':
				if 0 <= stave[2] - c.offset_y <= (st_space/2):						# was only smaller that ...
					staff_number = stave[0]
					line_number = stave[1]
					note = notes[stave[1]]
					break
			elif uod == 'U':
				if 0 <= stave[2] - (c.offset_y + c.nrows) <= (st_space/2):			# was only smaller that ...
					staff_number = stave[0]
					line_number = stave[1]-1
					note = notes[stave[1]-1]
					break


		glyph_list.append([staff_number, c.offset_x, c.offset_y, note, line_number, glyph_kind, actual_glyph, glyph_char, uod, c.ncols, c.nrows])
	

		

#	for i, line in enumerate(stavelines):
#		dif = (line[2] - c.offset_y)				### THIRD ELEMENT OF THE LIST IS LINE Y-POSITION
#		if 0 < dif < (st_space/3): 						### FIND THE OPTIMAL DIFFERENCE DEPENDING IN THE STAFFLINES HEIGHT
#			print 'Neume', c.label, (c.get_main_id()[6:]), 'in staff', line[0], 'line', line[1], 'note', notes[((line[1]-1)*2)], c
#			break
		#print
#	else:
#		print c.label, c.get_main_id(), c

glyph_list.sort()
for i, gc in enumerate(glyph_list):
	print glyph_list[i]
	
print 'There are', len(class_im), 'recognized glyphs,', neume_count, 'neumes, and ', er, 'errors'


	

