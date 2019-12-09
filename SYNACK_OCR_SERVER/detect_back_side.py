from Read_text import *
def crop_fingerprint(img):
  x_start, y_start = img.shape[1] /8, img.shape[0] /4
  x_end, y_end =img.shape[1]/3, img.shape[0] / 2
  fingerprint = img[int(y_start) : int(y_end),int(x_start) : int(x_end)]
  return fingerprint
def detect_back_side_ID(img):
	kq = crop_image_from_background(img,'back')
	kq = crop_fingerprint(kq)
	return kq
