from google_images_download import google_images_download   #importing the library

response = google_images_download.googleimagesdownload()   #class instantiation
'''
arguments = []
arguments.append({"keywords":"Allergy Relief, Allergy Medicine, allergy drug, Asthma and Sinus Medicine, Sunmark allergy medicine,  Premier Value allergy,  Zyrtec allergy,  Claritin allergy","limit":100, "output_directory":"allergyRelief", "size":"large"}) 
#arguments = {"keywords":"Vitamin b supplement, B complex supplement, Vitamin c supplement ","limit":100,}   #creating list of arguments
#arguments = {"keywords":"Vitamin E supplement, Natures Bounty supplement","limit":100,}   #creating list of arguments
#arguments = {"keywords":"Natures Truth supplement, Nature made supplement, Premier Value supplement, Sundance supplement, Sundown Naturals supplement, Centrum supplement","limit":100,}

arguments.append({"keywords":"headache medicine, pain relief drug, pain relief medicine, pain killer drug, Advil pain relief, Aleve pain relief,  Hylands pain relief, Icy Hot pain relief, Premier Value pain relief, Sunmark pain relief, Boiron pain relief", "limit":100, "output_directory":"painRelief", "size":"large"}) 

for ar in arguments:
	paths = response.download(ar)   #passing the arguments to the function
#print(paths)   #printing absolute paths of the downloaded images
'''
arguments = {"keywords":"drug","limit":50,"output_directory":"image_crawl", "size":"large"}   #creating list of arguments
with open('drug_name.txt', 'r') as names:
	for line in names:
		key = line[:-1] + ' product package'
		arguments['keywords'] = key
		print("processing " + key)
		paths = response.download(arguments)
		
	 
