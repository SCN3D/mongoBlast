# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai
import sys
import os.path
import argparse
import re
import itertools
#import functions
#def preprocess(converter,):
class deletion_data:
    def __init__(self, pos, seq):
        self.pos = pos
        self.seq = seq

def get_ptms(ptms,table,id,s_p,e_p,insertions,deletions):
	ab_ptms = dict()
	data = table.find_one({'_id': id})
	pad = re.match(r"^\.+",data["sequence"])
	if pad == None:
		pad = 0
	else:
		pad = len(pad)

	for ptm in ptms:
		ab_ptms[ptm] = []
		if data[ptm]:
			for i in data[ptm]:
				if i in range(s_p,e_p+1):
					temp_ptm = i - s_p + pad + 14
					for j in insertions[id]:
						if temp_ptm > j[0]:
							temp_ptm = temp_ptm + j[1] - j[0]
						else:
							break
					delete = False
					for k in deletions[id]:
						if temp_ptm in range(k.pos,k.pos+len(k.seq)):
							delete = True
							break
					if delete == True:
						ab_ptms[ptm].append(temp_ptm)
	return ab_ptms
	
def get_deletions(fp,seq_start,seq_index):
	deletions = []

	line = fp.readline()
	indexes = [(m.start() - 14 + seq_index - int(seq_start)) for m in re.finditer(r"\|+", line)]
	#print(line)
	#indexes = [m.sapn()  for m in re.finditer('\\+', line)]
	line = fp.readline()
	collapsed = ' '.join(line.split())
	data = collapsed.split(" ")
	for counter, i in enumerate(indexes):
		deletions.append(deletion_data(i,data[counter]))
	return deletions

def get_ids(fp):
	fp.readline()
	fp.readline()
	fp.readline()
	fp.readline()
	fp.readline() # skip redundent info
	ids = []
	line = fp.readline()

	while line != "\n":
		collapsed = ' '.join(line.split())
		data = collapsed.split(" ")
		ids.append(data[0])
		line = fp.readline()
	return ids

def blast_get_inserts(pattern,string):
	inserts = [m.span() for m in re.finditer(pattern, string)]
	for counter, i in enumerate(inserts):
		# print(i)
		inserts[counter] = [x+14 for x in i]
	return inserts
	
def display_output(q_id,q_seq,output,ids,fp):
	q_id = '{:14}'.format(q_id)
	fp.write(q_id + q_seq + "\n")
	for i in ids:
		fp.write('{:14}'.format(i) + output[i] +  "\n")

#def display_ptm(output,insertions,deletions,out_fp):
#	inserts = blast_get_inserts("-+",output[i])

	
def blast_output(filepath,ptms):
	#table = functions.connectMongoDB('uniprot','table')
	out_file = open('blast_output.txt','w')

	seqs_start_position = 0
	seqs_end_position = 0
	output = dict()
	q_name = "query name"
	ids = []
	acs = []
	ac_deletions = dict()

	fp = open(filepath)
	line = fp.readline()


	while line:
		collapsed = ' '.join(line.split())
		data = collapsed.split(" ")
		tag = data[0]
		#print("tag: "+tag)
		if tag == "Query=":
			q_name = data[1]

			ids = get_ids(fp)
		elif tag.lower() == q_name.lower():

			# q_start = int(data[1])
			temp_q_end = int(data[3])
			q_seq = data[2]
			seqs_start_position = line.find(data[2]) # start position in txt
			seqs_end_position = line.find(data[3]) - 2 # end position in txt
			seqs_end_index = dict() 
			seqs_start_index = dict()
			# print("start: "+str(seqs_start_position)+"--->end: "+str(seqs_end_position))

			line = fp.readline()
			collapsed = ' '.join(line.split())
			data = collapsed.split(" ")
			
			prev_ac = ""
			prev_start = 0

			while line and data[0] != "Lambda":
				if data[0].lower() == q_name.lower(): # if its query
					seqs_start_position = line.find(data[2])
					seqs_end_position = line.find(data[3]) - 2
					# print("start: "+str(seqs_start_position)+"--->end: "+str(seqs_end_position))
					if temp_q_end == int(data[1])-1:
						temp_q_end = int(data[3])
						q_seq += data[2]
					else:
						print("special case!")
				elif len(data) == 4 and int(data[1]) and int(data[3]): # if its subjects
					if data[0] in output: # if its not head
						prev_ac = data[0]
						prev_start = int(data[1])
						seqs_end_index[data[0]] = data[3]
						output[data[0]] += line[seqs_start_position:seqs_end_position]
					else: # if its head
						prev_ac = data[0]
						prev_start = int(data[1])
						seqs_start_index[data[0]] = data[1]
						output[data[0]] = line[seqs_start_position:seqs_end_position]
						acs.append(data[0])
				elif data[0] == "\\":
					if prev_ac in ac_deletions:
						delete = get_deletions(fp,seqs_start_index[prev_ac],prev_start)
						ac_deletions[prev_ac] += delete
					else:
						delete = get_deletions(fp,seqs_start_index[prev_ac],prev_start)
						ac_deletions[prev_ac] = delete
				line = fp.readline()
				
				collapsed = ' '.join(line.split())
				data = collapsed.split(" ")	

			# preprocess data
			converter = dict(zip(acs,ids))
			for ncbi in converter:
				output[converter[ncbi]] = output.pop(ncbi)
				output[converter[ncbi]] = output[converter[ncbi]].ljust(len(q_seq))
				output[converter[ncbi]] = output[converter[ncbi]].replace(" ",".")
				seqs_start_index[converter[ncbi]] = seqs_start_index.pop(ncbi)
				seqs_end_index[converter[ncbi]] = seqs_end_index.pop(ncbi)
				### working area
				



			display_output(q_name,q_seq,output,ids,out_file)
		line = fp.readline()
	
	for i in ac_deletions:
		for j in ac_deletions[i]:
			print("ac: "+i+"\tpos: "+str(j.pos)+"\tseq: "+str(j.seq))
	out_file.close()
	fp.close()
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', default='format2.txt',help="local filepath")
	parser.add_argument('-ptms', nargs='+', default='Phosphoserine', help="ptms ptm1 ptm2")
	args = parser.parse_args()
	filepath = args.l
	ptms = args.ptms
	
	if os.path.exists(filepath):
		blast_output(filepath,ptms)
			
	else:
		print("File does not exist\n")
		sys.exit()
  
if __name__== "__main__":
	main()
