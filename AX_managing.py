from gamera.toolkits.aruspix.ax_file import AxFile
from gamera.toolkits.aruspix.ax_page import AxPage
from gamera.toolkits.aruspix.ax_staff import AxStaff

from gamera.toolkits.musicstaves import MusicStaves_linetracking as MusicStaves

image = load_image(r"/Users/gabriel/Documents/imgs/pdf_to_tiff_conversion/IMG_test/Pitch_Recognition/127__only_staves.tiff")
axpage = AxPage(image)
#axpage.remove_staves('bars', 4, 25)
axpage.image.display()
ms = image.MusicStaves_linetracking()
staves = ms.get_staffpos()

for s in staves:
	print s
	axstaff = AxStaff(s, 75, 150, 22, 3)
	axstaff.glyphs
	axstaff.output()

#staffline_height = 3
#staffspace_height = 22