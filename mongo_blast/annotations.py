# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai
import sys
import os.path
import argparse
import functions
import ptmAnnotation
		
def get_ids():
    ids = []
    table = functions.connectMongoDB('uniprot','table')
    cursor = table.find()
    for doc in cursor:
        ids.append(doc['_id'])
    return ids

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-ptms', nargs='+', help="ptm", required=True)
	parser.add_argument('-out',default='data', help="output folder name")
	args = parser.parse_args()
	# ptms = ['Phosphoserine','N6-methyllysine','Phosphothreonine','Phosphotyrosine',
	# 'N6-acetyllysine','Omega-N-methylarginine','N6,N6-dimethyllysine','N6,N6,N6-trimethyllysine','N-linked(GlcNAc)asparagine',
	# 'S-palmitoylcysteine','Pyrrolidonecarboxylicacid','Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)']
	ids = get_ids()
	ptms = args.ptms
	
	folder_path = args.out
	
	ptmAnnotation.MongotoPTMannotation(ids,ptms,folder_path)
  
if __name__== "__main__":
	main()



