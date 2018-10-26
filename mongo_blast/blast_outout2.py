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
 
def save_to_file(q_id,q_seq,output,fp):
	q_id = '{:14}'.format(q_id)
	fp.write(q_id + q_seq + "\n")
	for i in output:
		fp.write('{:14}'.format(i) + output[i] + "\n")
	
def blast_output(filepath):
	#table = functions.connectMongoDB('uniprot','table')
	out_file = open('blast_output.txt','w')

	seqs_start_position = 0
	seqs_end_position = 0
	output = dict()
	q_name = "query name"

	fp = open(filepath)
	line = fp.readline()

	while line:
		collapsed = ' '.join(line.split())
		data = collapsed.split(" ")
		tag = data[0]
		#print("tag: "+tag)
		if tag == "Query=":
			q_name = data[1]
		elif tag.lower() == q_name.lower():

			#q_start = int(data[1])
			temp_q_end = int(data[3])
			q_seq = data[2]
			seqs_start_position = line.find(data[2])
			seqs_end_position = line.find(data[3]) - 2
			print("start: "+str(seqs_start_position)+"--->end: "+str(seqs_end_position))

			line = fp.readline()
			collapsed = ' '.join(line.split())
			data = collapsed.split(" ")

			while line and data[0] != "Lambda":
				if data[0].lower() == q_name.lower():
					seqs_start_position = line.find(data[2])
					seqs_end_position = line.find(data[3]) - 2
					print("start: "+str(seqs_start_position)+"--->end: "+str(seqs_end_position))
					if temp_q_end == int(data[1])-1:
						temp_q_end = int(data[3])
						q_seq += data[2]
					else:
						print("special case!")
				elif len(data) == 4 and int(data[1]) and int(data[3]):
					if data[0] in output:
						output[data[0]] += line[seqs_start_position:seqs_end_position]
					else:
						output[data[0]] = line[seqs_start_position:seqs_end_position] 
				elif len(data) == 0:
					print("new lines")
				line = fp.readline()
				collapsed = ' '.join(line.split())
				data = collapsed.split(" ")	
			#print("query: "+q_seq)
			save_to_file(q_name,q_seq,output,out_file)
		line = fp.readline()
	print("done!")
	out_file.close()
	fp.close()
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', default='format2.txt',help="local filepath")
	args = parser.parse_args()
	filepath = args.l
	
	filepath = args.l
	
	if os.path.exists(filepath):
		blast_output(filepath)
			
	else:
		print("File does not exist\n")
		sys.exit()
  
if __name__== "__main__":
	main()



