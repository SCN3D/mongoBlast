# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai
import sys
import os.path
import argparse
import functions
	
#insert # after ptm position in seq, format: fasta
def prepare(id,relative_positions):
	out_data = id
	for i in relative_positions:
		out_data += ' '+str(i)
	return out_data + '\n'

def calc_psition(q_start,s_start,s_end,ptm_positions):
	if ptm_positions is None:
		return 0
	relative_positions = []
	for position in ptm_positions:
		position = int(position)
		if position >= s_start and position <= s_end:
			seq_rel_pos = position - s_start
			q_rel_pos = q_start + seq_rel_pos
			relative_positions.append(q_rel_pos)
	return relative_positions

def	ptmPosition(Tag_FTs):
	table = functions.connectMongoDB('uniprot','table')
	out_data = ''
	file = []
	if not os.path.exists("data"):
		os.makedirs("data")
	
	for index, tag in enumerate(Tag_FTs):
		file.append(open('data/'+tag+'.txt','w'))

	with open("format8.txt") as fp:
		for line in fp:
			collapse = ' '.join(line.split())
			parse = collapse.split(" ")
			id = parse[1]
			ptm = table.find_one({'_id': id})
			ptm_pos = []
			for index, ft in enumerate(Tag_FTs):
				if ft in ptm:
					ptm_pos.extend(ptm[ft])

				relative_positions = calc_psition(int(parse[6]),int(parse[8]),int(parse[9]),ptm_pos)

				out_data = prepare(ptm['_id'],relative_positions)
				file[index].write(out_data)		

	for index, tag in enumerate(Tag_FTs):
		file[index].close()
		
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-ptm', nargs='+', help="ptm list", required=True)
	args = parser.parse_args()
	# ptms = ['Phosphoserine','N6-methyllysine','Phosphothreonine','Phosphotyrosine',
	# 'N6-acetyllysine','Omega-N-methylarginine','N6,N6-dimethyllysine','N6,N6,N6-trimethyllysine','N-linked(GlcNAc)asparagine',
	# 'S-palmitoylcysteine','Pyrrolidonecarboxylicacid','Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)']

	ptm = args.ptm
	
	ptmPosition(ptm)
  
if __name__== "__main__":
	main()



