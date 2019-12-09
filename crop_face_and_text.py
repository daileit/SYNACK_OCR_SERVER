from Read_text import *
def crop_face_and_text_line(img):
	rs = crop_image_from_background(img,'front')
	top_end_text,minx,maxx,miny,maxy = detect_cmnd(rs)
	top_end_text = cv2.resize(top_end_text,(994,908))
	face = rs[int((maxy-miny)*5/12):maxy,:minx]
	return face,top_end_text