glyph_name = 'neume.torculus.4.2'
for l, letter in enumerate(glyph_name[6:]):
	if letter == '.':
		actual_glyph_name = glyph_name[6:6+l]
		break
