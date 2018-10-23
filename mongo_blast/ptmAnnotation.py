# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai
import sys
import os.path
import argparse
import functions
	
#insert # after ptm position in seq, format: fasta
def prepare(id,ft,seq):
	seq_list = list(seq)
	for c,i in enumerate(ft):
		seq_list.insert(i+c,'#')
	
	sequence = ''.join(seq_list)
	out_data = '>sp|'+id+'\n'+sequence+'\n'
	return out_data


def MongotoPTMannotation(proteinIDs,Tag_FTs,output_prefix):
	table = functions.connectMongoDB('uniprot','table')

	file = []
	out_data = ''
	
	if not os.path.exists(output_prefix):
		os.makedirs(output_prefix)
	
	for index, tag in enumerate(Tag_FTs):
		file.append(open(output_prefix+'/'+tag+'.fasta','w'))
		
	
	for id in proteinIDs:
		ptm = table.find_one({'_id': id})
		
	
		for index, ft in enumerate(Tag_FTs):
			ft_index = []
			unfold_ft = ft.split("_")
			
			for new_ft in unfold_ft:
				if new_ft in ptm:
					ft_index.extend(ptm[new_ft]) 
			ft_index = map(int,ft_index)
			ft_index.sort()
			if len(ft_index) >= 1:
				sequence = ptm['sequence']
				
				out_data = prepare(ptm['ac'][0]+"|"+ptm['_id'],ft_index,sequence)
				
				file[index].write(out_data)
					
	for index, tag in enumerate(Tag_FTs):
		file[index].close()
		
def get_q_ids():
	ids = []
	with open("format8.txt") as fp:
		for line in fp:
			collapse = ' '.join(line.split())
			parse = collapse.split(" ")
			ids.append(parse[1])
	return ids

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-ptms', nargs='+', help="ptm", required=True)
	parser.add_argument('-out',default='data', help="output folder name")
	args = parser.parse_args()
	# ptms = ['Phosphoserine','N6-methyllysine','Phosphothreonine','Phosphotyrosine',
	# 'N6-acetyllysine','Omega-N-methylarginine','N6,N6-dimethyllysine','N6,N6,N6-trimethyllysine','N-linked(GlcNAc)asparagine',
	# 'S-palmitoylcysteine','Pyrrolidonecarboxylicacid','Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)']
	ids = get_q_ids()
	ptms = args.ptms
		
	folder_path = args.out
	
	MongotoPTMannotation(ids,ptms,folder_path)
  
if __name__== "__main__":
	main()



