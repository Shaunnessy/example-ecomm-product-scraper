# Importing library
import cv2
from pyzbar.pyzbar import decode
import requests
import shutil
import wget

'''
required to run:

host needs zbar library
python3 - third party modules:
	pyzbar
	opencv-python
	wget

'''

# Make one method to decode the barcode
def BarcodeReader(image):
	
	# read the image in numpy array using cv2
	img = cv2.imread(image)
	
	# Decode the barcode image
	detectedBarcodes = decode(img)
	
	# If not detected then print the message
	if not detectedBarcodes:
		print("Barcode Not Detected or your barcode is blank/corrupted!")
		return

	else:
	
		# Traverse through all the detected barcodes in image
		for barcode in detectedBarcodes:
		
			# Locate the barcode position in image
			(x, y, w, h) = barcode.rect
			
			# Put the rectangle in image using
			# cv2 to highlight the barcode
			cv2.rectangle(img, (x-10, y-10),
						(x + w+10, y + h+10),
						(255, 0, 0), 2)
			
			if barcode.data!="":
				# print(barcode.data)
				cv2.imshow("Image", img)
				# cv2.waitKey(0)
				cv2.destroyAllWindows()
			# Print the barcode data
				return barcode
				#print(barcode.data)
				#print(barcode.type)

				
				
	#Display the image
	


if __name__ == "__main__":
# Take the image from user
	image= wget.download("https://m.media-amazon.com/images/I/71j7ydPO8wL._SL1500_.jpg")

	#print(image)
	#input()
	#exit()
	BarcodeReader(image)
