# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai
import sys
import os.path
import argparse
import re
import itertools
import functions

# for debug
log_file = open("ptm_log.txt","w")

class deletion_data:
    def __init__(self, pos, seq):
        self.pos = pos
        self.seq = seq

def reposition_seq(str,pad):
	len_str = len(str) + pad * 60
	return str.rjust(len_str)


def is_int(str):
	try:
		int(str)
	except ValueError:
		return False
	else:
		return True

def prepare(id,relative_positions):
	out_data = id
	for i in relative_positions:
		out_data += ' '+str(i)
	return out_data + '\n'

def get_ptms(ptm,table,ids,s_p,e_p,insertions,deletions,seqs):
	ab_ptms = dict()

	for id in ids:
		ab_ptms[id] = []
		data = table.find_one({'_id': id})
		pad = re.match(r"^\.+",seqs[id])

		if pad == None:
			pad = 0
		else:
			pad = len(pad.group(0))

		if ptm in data:
			for i in data[ptm]:
				if int(i) >= s_p[id] and int(i) <= e_p[id]:

					out_ptm = int(i) - s_p[id] + pad + 1

					temp_ptm = out_ptm
					# first calc insertions
					if id in insertions:
						for j in insertions[id]:
							if out_ptm > j[0]:
								out_ptm = out_ptm + j[1] - j[0]
							else:
								break
					delete = False
					# then deal with deletions
					if id in deletions:
						for k in deletions[id]:
							if temp_ptm > k.pos: 
								if temp_ptm <= k.pos+len(k.seq):
									delete = True
									break
								else:
									temp_ptm += len(k.seq)
					if delete == False:
						#log
						log_file.write("id: "+id+"\tptm: "+ptm +"\tDB_position: "+str(i)+"\tseq_start: "+str(s_p[id])+"\tseq_end: "+str(e_p[id])+" ADDED!\n")
						
						ab_ptms[id].append(out_ptm)
					else:
						#log
						log_file.write("id: "+id+"\tptm: "+ptm +"\tab_position: "+str(out_ptm)+" DELETED!\n")
				else:
					#log
					log_file.write("id: "+id+"\tptm: "+ptm +"\tDB_index: "+str(i)+"\tseq_start: "+str(s_p[id])+"\tseq_end: "+str(e_p[id])+" OUT OF RANGE!\n")
	return ab_ptms
	
def get_deletions(fp,seq_start,seq_index):
	deletions = []
	line = fp.readline()
	indexes = [(m.start() + seq_index - int(seq_start)) for m in re.finditer(r"\|+", line)]

	line = fp.readline()
	line = re.sub("|","",line)
	collapsed = ' '.join(line.split())
	data = collapsed.split(" ")
	
	deletion_strs = []

	while len(deletion_strs) < len(indexes):
		if not data:
			line = fp.readline()
			line = re.sub("|","",line)
			collapsed = ' '.join(line.split())
			data = collapsed.split(" ")
		else:
			for d in data:
				deletion_strs.append(d)

	for counter, i in enumerate(indexes):
		deletions.append(deletion_data(i,deletion_strs[counter]))

	return deletions

def get_ids(fp):
	tag = "tag!"
	while tag != "Sequences":
		collapsed = ' '.join(fp.readline().split())
		data = collapsed.split(" ")
		tag = data[0]
	fp.readline()# skip redundent info
	ids = []
	line = fp.readline()

	while line != "\n":
		collapsed = ' '.join(line.split())
		data = collapsed.split(" ")
		ids.append(data[0])
		line = fp.readline()
	return ids

def get_inserts(string):
	inserts = [m.span() for m in re.finditer("-+", string)]
	for counter, i in enumerate(inserts):
		inserts[counter] = [x for x in i]
		#print(inserts[counter])
	return inserts # m.start() => inserts[0]; m.end() => inserts[1] 

def display_output(q_id,q_seq,output,ids,identities,fp):
	q_id = '{:14}'.format(q_id)
	fp.write(q_id + q_seq + "\n")
	for id in ids:
		fp.write('{:14}'.format(id) + '{:8}'.format(identities[id]) + output[id] +  "\n")

def display_ptm(ptm,ptm_fp,ids):
	for id in ids:
		out = prepare(id,ptm[id])
		#if len(ptm[id]) > 0:
		#	print(ptm_fp.name+": "+out)
		ptm_fp.write(out)

def get_identities():
	out = dict()
	file_name = 'format8.txt'
	fp = open(file_name)
	line = fp.readline()
	while line:
		collapsed = ' '.join(line.split())
		data = collapsed.split(" ")
		id = data[1]
		identity = data[2]
		out[id] = identity
		line = fp.readline()
	return out
	
	
def blast_output(filepath,ptms,out_folder):
	file = []
	
	for ptm in ptms:
		file.append(open(out_folder+'/'+ptm+'.txt','w'))

	table = functions.connectMongoDB('uniprot','table')
	out_file = open(out_folder+'/blast_output.txt','w')

	seqs_start_position = 0
	seqs_end_position = 0
	output = dict()
	q_name = "query name"
	ids = []
	acs = []
	ac_deletions = dict()
	insertions = dict()
	ab_ptms = dict()

	fp = open(filepath)
	line = fp.readline()

	sequence_pad = -1


	while line:
		collapsed = ' '.join(line.split())
		data = collapsed.split(" ")
		tag = data[0]
		#print("tag: "+tag)
		if tag == "Query=":
			q_name = "Query_1"

			ids = get_ids(fp)
		elif tag.lower() == q_name.lower():
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
					sequence_pad += 1
					seqs_start_position = line.find(data[2])
					seqs_end_position = line.find(data[3]) - 2
					# print("start: "+str(seqs_start_position)+"--->end: "+str(seqs_end_position))
					if temp_q_end == int(data[1])-1:
						temp_q_end = int(data[3])
						q_seq += data[2]
					else:
						print("special case!")
				elif len(data) == 4 and is_int(data[1]) and is_int(data[3]): # if its subjects
					if data[0] in output: # if its not head
						prev_ac = data[0]
						prev_start = int(data[1])
						seqs_end_index[data[0]] = int(data[3])
						output[data[0]] += line[seqs_start_position:seqs_end_position]
					else: # if its head
						prev_ac = data[0]
						prev_start = int(data[1])
						seqs_start_index[data[0]] = int(data[1])
						seqs_end_index[data[0]] = int(data[3])
						output[data[0]] = reposition_seq(line[seqs_start_position:seqs_end_position],sequence_pad)
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
			
			##########check ptms
			#for id in ids:
			#	temp = table.find_one({"_id": id})
			#	for ptm in ptms:
			#		if ptm in temp:
			#			print(temp[ptm])
			##################
		
			# preprocess data
			converter = dict(zip(acs,ids))
			for ncbi in converter:
				output[converter[ncbi]] = output.pop(ncbi)
				output[converter[ncbi]] = output[converter[ncbi]].ljust(len(q_seq))
				output[converter[ncbi]] = output[converter[ncbi]].replace(" ",".")
				seqs_start_index[converter[ncbi]] = seqs_start_index.pop(ncbi)
				seqs_end_index[converter[ncbi]] = seqs_end_index.pop(ncbi)
				if ncbi in ac_deletions:
					ac_deletions[converter[ncbi]] = ac_deletions.pop(ncbi)
				
				insertions[converter[ncbi]] = get_inserts(output[converter[ncbi]])

			#############check deletions
			#for i in ac_deletions:
			#	for j in ac_deletions[i]:
			#		print("id: "+i+"\tpos: "+str(j.pos)+"\tseq: "+j.seq)
			#####################

			# ptm position is relative to the line in the file not sequence now
			for counter, ptm in enumerate(ptms):
				ab_ptms = get_ptms(ptm,table,ids,seqs_start_index,seqs_end_index,insertions,ac_deletions,output)
				display_ptm(ab_ptms,file[counter],ids)
			identities = get_identities()
			display_output(q_name,q_seq,output,ids,identities,out_file)

		line = fp.readline()
	
	
	out_file.close()
	fp.close()
	for index, ptm in enumerate(ptms):
		file[index].close()
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', default='format2.txt',help="local filepath")
	parser.add_argument('-ptms', nargs='*', default=['Phosphotyrosine'], help="ptms ptm1 ptm2")
	parser.add_argument('-o', default='display',help="output folder name")
	args = parser.parse_args()
	filepath = args.l
	ptms = args.ptms
	out_folder = args.o

	if not os.path.exists(out_folder):
		os.makedirs(out_folder)

	if os.path.exists(filepath):
		blast_output(filepath,ptms,out_folder)	
	else:
		print("File does not exist\n")
		sys.exit()
  
if __name__== "__main__":
	main()
log_file.close()