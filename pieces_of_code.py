_27__only_staves = load_image(r"/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Pitch_Recognition/127__only_staves.tiff")
musicstaves0 = musicstaves.MusicStaves_rl_fujinaga(_27__only_staves, 0, 0)
musicstaves0.remove_staves(u'all', 4)


# To retrieve the page position and dimensions of each one of the staves in a page
# using a MusicStaves object (actually removing the staves)
for i in range(1, len(musicstaves0.get_staffpos(x=0))):
	print "Staff no.", i
	musicstaves0.get_staffpos(x=0)[i].staffrect # staff position and dimension
	musicstaves0.get_staffpos(x=0)[i].yposlist	# each line position	


# To retrieve the page position and dimensions of each one of the staves in a page
# using a StaffFinder object (without removing the staves)
from gamera.core import *
import gamera.toolkits.musicstaves 

init_gamera()

image = load_image(r"/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Pitch_Recognition/127__only_staves.tiff")
image = image.to_onebit()

sf = stafffinder_miyao.StaffFinder_miyao(image)
sf.find_staves()

staves = sf.get_average()
for i, staff in enumerate(staves):
  print "Staff %d has %d staves:" % (i+1, len(staff))
  for j, line in enumerate(staff):
    print "    %d. line at y-position:" % (j+1), line.average_y






# knn.glyphs_by_category
def glyphs_by_category(glyphs):
   klasses = {}
   for x in glyphs:
      id = x.get_main_id()
      if not klasses.has_key(id):
         klasses[id] = []
      klasses[id].append(x)
   return klasses