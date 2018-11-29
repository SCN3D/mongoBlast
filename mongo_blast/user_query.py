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

    step_1 = 'blastall -p blastp -i query_seqs.fasta -d background_seqs.fasta -e 1e-5 -v 50 -b 50 -m 2 -o format2.txt'
    step_2 = 'codes/blast_parse.py'
    

    subprocess.call([step_1],shell=True)
    print('step 1 done')
    subprocess.call(['python',step_2,'-l',filepath,'-ptms',ptms,'-o',out_folder])
    print("User query Finished")

  
if __name__== "__main__":
	main()