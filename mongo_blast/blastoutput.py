import sys
import os.path
import argparse
import functions

def get_query_seq(id):
    seq = ""
    seq_flag = 0
    with open("query_seqs.fasta") as fp:
        for line in fp:
            parse = line.split(" ")

            if len(parse) > 1 and id == parse[1].rstrip():
                seq_flag = 1
            elif len(parse) == 1 and seq_flag == 1:
                seq += parse[0]
            elif seq_flag == 1 and parse[0] == ">":
                return seq.rstrip()
    return seq.rstrip()
            
def fillup(num,seq):
    out = ""
    for i in range(num):
        out += " "
    out += seq
    return out

def	blast_output(output_prefix):
    table = functions.connectMongoDB('uniprot','table')
    if not os.path.exists(output_prefix):
	    os.makedirs(output_prefix)
    out_file = open(output_prefix+'/input1.txt','w')
    current = " "
    with open("format8.txt") as fp:
        for line in fp:
            collapse = ' '.join(line.split())
            parse = collapse.split(" ")
            if current != parse[0]:
                current = parse[0]
                seq = get_query_seq(current)
                q_id = '{:14}'.format(current)
                out_file.write(q_id + seq + "\n")
            pid = '{:14}'.format(parse[1]) 
            p_doc = table.find_one({'_id': parse[1]})
            p_seq = p_doc["sequence"]
            start = int(parse[8])-1 
            end = int(parse[9])
            p_seq = p_seq[start:end]
            p_seq = fillup(int(parse[6])-1,p_seq)
            out_file.write(pid + p_seq + "\n")
    out_file.close()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-out',default='data', help="output folder name")
	args = parser.parse_args()
	
	folder_path = args.out
	
	blast_output(folder_path)
  
if __name__== "__main__":
	main()