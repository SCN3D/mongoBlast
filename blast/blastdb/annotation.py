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
	
#insert # after ptm position in seq, format: fasta
def duolin(id,ft):
	out_data = id+'\t'
	for i in ft:
		out_data += i+' '
	return out_data



def	MongotoPTMannotation(proteinIDs,Tag_FTs,output_prefix):
	table = functions.connectMongoDB('uniprot','table')
	file = []
	out_data = ''
	
	if not os.path.exists(output_prefix):
		os.makedirs(output_prefix)
	
	for index, tag in enumerate(Tag_FTs):
		file.append(open(output_prefix+'/'+tag+'.fasta','w'))
		
	
	for id in proteinIDs:
		ptm = table.find_one({'_id': id})
		ft_index = []
		for index, ft in enumerate(Tag_FTs):
			if ft in ptm:
				ft_index.extend(ptm[ft]) 
					
			if len(ft_index) >= 1:
				out_data = duolin(ptm['_id'],ft_index)
				file[index].write(out_data)
					
	for index, tag in enumerate(Tag_FTs):
		file[index].close()
		
#requirement: 1. uniprotCreateDB.py   2. tableGenerator.py 
#example annotaion.py -l 'uniprot '
def main():
	parser = argparse.ArgumentParser()
	#parser.add_argument('-fts', nargs='+', help="feature keys", required=True)
	parser.add_argument('-ids', nargs='+', help="id list", required=True)
	parser.add_argument('-out', help="output folder name", required=True)
	args = parser.parse_args()
	fts = ['Phosphoserine','N6-methyllysine','Phosphothreonine','Phosphotyrosine',
	'N6-acetyllysine','Omega-N-methylarginine','N6,N6-dimethyllysine','N6,N6,N6-trimethyllysine','N-linked(GlcNAc)asparagine',
	'S-palmitoylcysteine','Pyrrolidonecarboxylicacid','Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)']
	ids = args.ids
	
	# print(fts)
	
	folder_path = args.out
	
	MongotoPTMannotation(ids,fts,folder_path)
  
if __name__== "__main__":
	main()



