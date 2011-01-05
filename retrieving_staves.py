from gamera.core import *
from gamera.toolkits.musicstaves import stafffinder_miyao

init_gamera()

image = load_image(r"/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Pitch_Recognition/127__only_staves.tiff")
image = image.to_onebit()
print str(image.ncols) + ' * ' + str(image.nrows)
#print image.nrows


sf = stafffinder_miyao.StaffFinder_miyao(image)
sf.find_staves()

staves = sf.get_average()
#polygon = sf.get_polygon()

for i, staff in enumerate(staves):
	print "Staff %d has %d staves:" % (i+1, len(staff))
	
	for j, line in enumerate(staff):
		print "    %d. line at y-position:" % (j+1), line.average_y
#		print "Its positions is " + str(polygon[i][j].vertices) 
	

for g in line.glyphs:
	classname = g.get_main_id()
	g.classify_automatic(classname)
	