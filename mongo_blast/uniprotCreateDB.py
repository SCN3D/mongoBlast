# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai
import functions
import sys
import os.path
import argparse 
from datetime import datetime as dt
		
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-update', type=int, default=0, help="update options [#](every # months) , default to manual(0)")

	args = parser.parse_args()
	
	filepath = 'uniprotData/uniprot.txt'
	dbname = 'uniprot'
	colname = 'entry'
	if not os.path.exists("uniprotData"):
		os.makedirs("uniprotData")
	functions.getUniprot()
	if os.path.exists(filepath):
		functions.updateMongoDB(filepath,dbname,colname,"1/1/1111")
		functions.Config_edit(dt.now().date())
		
		if args.update > 0:
			functions.setAutoUpdate(args.update)
			print("Check for update every %s months!" % (args.update))
	else:
		print("File does not exist\n")
		sys.exit()
	
  
if __name__== "__main__":
	main()



