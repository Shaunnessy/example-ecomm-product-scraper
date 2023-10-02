import requests
import json
from bs4 import BeautifulSoup
import wget
import csv

'''
required to run:

host needs zbar library
python3 - third party modules:
	bs4
	wget
	csv
	wget

'''
#local modules
from barcodescanner import BarcodeReader


# helper functions:

def output_csv(data,headers,filename='file.csv',path=""): # dynamic csv file dump

    with open(f'{path}{filename}','w') as file:

        fieldnames = headers
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return

# Example scraper:

data = [] 
columns = []

# examples Url has a barcode picture in it's product page, while urTtwo does not

urlTwo ="https://www.walmart.com/ip/Equate-Sport-Broad-Spectrum-Sunscreen-Spray-SPF-50-Twin-Pack/963321253?athbdg=L1200&from=/search"
url = "https://www.walmart.com/ip/CeraVe-Hydrating-Facial-Cleanser-Face-Wash-for-Normal-to-Dry-Skin-12-fl-oz/491147048?adsRedirect=true"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

# initial polling of product page
res = requests.get(urlTwo,headers=headers)

# print(res.status_code)

if res.status_code == 200:
	
	soup = BeautifulSoup(res.content,'html.parser')
	# productRow = {}
	# params to sort out of the product page
	# walmart parameters : 'data-testid', 'script'

	imageContainer = soup.find_all('img')
	productContainer = json.loads( soup.find('script',attrs={"type":"application/ld+json"} ).text ) 

## scraping images for product - scanning for one with barcode and appending to product json if successful
	imageContainer = soup.find('section',attrs = {'data-testid':'vertical-hero-carousel'})
	srcImages = [image['src'] for image in imageContainer.find_all('img')]
	productContainer.update({'imageLinks' : srcImages})
	for src in srcImages:
		localImage = wget.download(src)
		isBarcode = BarcodeReader(localImage)
		if isBarcode is not None:
			productContainer.update({'barcode': isBarcode.data, 'barcodeType': isBarcode.type})
			break

	# setting up keys to append as columns
	productKeys = list(productContainer.keys())
	
	#for item in productContainer:
	#	print(item,': \n',productContainer[item])

	# create table 
	data.append(productContainer)
	columns.extend([ value for index,value in enumerate(productKeys) if value not in headers ])

	# print(columns)

output_csv(data, columns)
	
