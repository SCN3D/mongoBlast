#
#!/usr/bin/python
#vm: amazon linux 2 AMI
#python 2.7.5
#mongodb 3.6.3
import pymongo
from pymongo import MongoClient
import sys
import os.path
import argparse
import re
import itertools
import functions
	
	
#if there is ft add 1 after id, format: fasta
def prepareData(id,seq):
	out_data = '>'+id+'|\n'+seq
	return out_data


#output_type 1: duolin 0:chunhui 
def	db_to_fasta(output_prefix):
	entry = functions.connectMongoDB('uniprot','entry')
	out_data = ''
	out_file = open(output_prefix+'.fasta','w')
	entrys = entry.find({})
	print('1')
	print(entrys)
	for doc in entrys:			
		out_data = prepareData(doc['_id'],doc['sequence'])
		out_file.write(out_data)
		print('2')

	out_file.close()
		
#requirement: 1. uniprotCreateDB.py 
#example DBtoF.py -l 'background_seqs'
#output file: background_seqs.fasta
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-out', help="output file name", required=True)
	args = parser.parse_args()
	
	file_name = args.out
	
	db_to_fasta(file_name)
	print('Done!')
  
if __name__== "__main__":
	main()


