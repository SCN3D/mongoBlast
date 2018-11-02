# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai
import time
import argparse
import functions
		
def get_ids(sp):
    ids = []
    table = functions.connectMongoDB('uniprot','table')
    cursor = table.find()
    for doc in cursor:
        if doc['species'] and sp in doc['species']:
            ids.append(doc['_id'])
    return ids

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-out',default='data_'+ "_".join(time.asctime().split(" ")), help="output folder name")
    args = parser.parse_args()

    ptms = ['Phosphoserine_Phosphothreonine','Phosphotyrosine','N-linked(GlcNAc)asparagine','N6-acetyllysine','N6-methyllysine_N6,N6-dimethyllysine_N6,N6,N6-trimethyllysine','Omega-N-methylarginine',
    'S-palmitoylcysteine','Pyrrolidonecarboxylicacid','Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)']
    ids = get_ids("Metazoa")
    
    folder_path = args.out
    
    functions.MongotoPTMannotation(ids,ptms,folder_path)
  
if __name__== "__main__":
	main()



