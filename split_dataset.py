import os
import glob

drebin = ["drebin-4"]
for files in drebin:
	os.chdir("objects/"+files)
	objects = glob.glob("*")
	for i in objects:
			if (os.path.getsize(i) < 100000): # less or equal than 100 KB
				os.rename(i,"/home/sentinel/PGRCyberintelligence/Centinela/objects/100KB/"+i)
			elif (100000 <= os.path.getsize(i) < 500000): # between 100-500 KB
				os.rename(i,"/home/sentinel/PGRCyberintelligence/Centinela/objects/500KB/"+i)
			elif (500000 <= os.path.getsize(i) < 1000000): # between 500 KB - 1 MB
				os.rename(i,"/home/sentinel/PGRCyberintelligence/Centinela/objects/1MB/"+i)
			elif (1000000 <= os.path.getsize(i) < 5000000): # between 1-5 MB
				os.rename(i,"/home/sentinel/PGRCyberintelligence/Centinela/objects/5MB/"+i)
			elif (os.path.getsize(i) >= 5000000) : # greater or equal than 5 MB
				os.rename(i,"/home/sentinel/PGRCyberintelligence/Centinela/objects/5MB+/"+i)
