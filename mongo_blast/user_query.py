# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai

import os
import argparse
import subprocess

def main():
    path = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', default=path+'/format2.txt',help="local filepath")
    parser.add_argument('-ptms', nargs='*', default=['Phosphotyrosine'], help="ptms ptm1 ptm2")
    parser.add_argument('-o', default=path+'/display',help="output folder name")
    args = parser.parse_args()
    filepath = args.l
    ptms = ' '.join(args.ptms)
    out_folder = args.o

    step_1 = 'blastp -query query_seqs.fasta -db mydb -evalue 1e-5 -max_target_seqs 50 -outfmt 11 -out format11.asn'
    step_2 = 'blast_formatter -archive format11.asn -outfmt "6 qseqid sseqid pident" -out format6.txt'
    step_3 = 'blast_formatter -archive format11.asn -outfmt 2 -out format2.txt'
    step_4 = 'python codes/blast_parse.py -l '+filepath+' -ptms '+ptms+' -o '+out_folder
    

    subprocess.call([step_1],shell=True)
    subprocess.call([step_2],shell=True)
    subprocess.call([step_3],shell=True)
    subprocess.call([step_4],shell=True)
    print("User query Finished")

  
if __name__== "__main__":
	main()