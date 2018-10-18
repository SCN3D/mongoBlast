# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai
import functions
import argparse
import sys
import configparser
from datetime import datetime as dt
import os

# read rss feed from uniprot, update database if there is a new update

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-train', type=int, choices=[0,1],default=0, help="set to 1 for output updated id list,default 0")
	
	args = parser.parse_args()
	
	dbname = "uniprot"
	colname = "entry"
	train = args.train
	
			
	config = configparser.ConfigParser()
	config.read('config.ini')
	old_date = dt.strptime(config['DEFAULT']['date'],"%Y-%m-%d")
	
	new_date = functions.rssread()
	
	if new_date > old_date:
		if train == 0:
			functions.updateMongoDB('uniprotData/uniprot.txt',dbname,colname,"1/1/1111")
			functions.Config_edit(new_date)
		elif train == 1:
			functions.updateMongoDB('uniprotData/uniprot.txt',dbname,colname,new_date)
			functions.Config_edit(new_date)
		else:
			print("error")
		dir_path = os.path.dirname(os.path.realpath(__file__))
		os.system('python '+dir_path+'/DBtoF.py')
		os.system('python '+dir_path+'/tableGenerator.py')
	else:
		print("No new update!")
if __name__== "__main__":
	main()
