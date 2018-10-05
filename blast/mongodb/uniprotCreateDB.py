#!/usr/bin/python
#vm: amazon linux 2 AMI
#python 2.7.5
#mongodb 3.6.3
import functions
import sys
import os.path
import argparse 
from datetime import datetime as dt

# usage: uniprotDB.py [-h] -l L -db DB -col COL -f F [F ...] [-update [UPDATE]]
#
# optional arguments:
#  -h, --help        show this help message and exit
#  -l L              local filepath
#  -db DB            database name
#  -col COL          collection name
#  -update [UPDATE]  update option[1,2,3,4,5], default to manual 0
#  -train            set to 1 for out put updated id list,default 0
# example: uniprotCreateDB.py -l 'uniprot.txt' -dbname 'uniprot' -colname 'entry' -f 'go interpro pfam prosite smart supfam' -update 1
		
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-update', type=int, default=0, help="update options [#](every # months) , default to manual(0)")

	args = parser.parse_args()
	
	filepath = 'uniprotData/uniprot.txt'
	dbname = 'uniprot'
	colname = 'entry'
	
	if os.path.exists(filepath):
		functions.updateMongoDB(filepath,dbname,colname,"1/1/1111")
		functions.Config_edit(dt.now().date())
		
		if args.update > 0:
			#train arg set to 1, so for output updated id list
			functions.setAutoUpdate(dbname, colname, 0, args.update)
			print("Check for update every %s months!" % (args.update))
	else:
		print("File does not exist\n")
		sys.exit()
	
  
if __name__== "__main__":
	main()



