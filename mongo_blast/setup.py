# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai

import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-update', type=int, default=0, help="update options: check every # months, default to manual(0)")
  
    args = parser.parse_args()
    step_1 = 'codes/tableGenerator.py'
    step_2 = 'codes/DBtoF.py'
    step_3 = 'codes/annotations.py'
    step_4 = 'makeblastdb -in background_seqs.fasta -dbtype prot -out mydb -parse_seqids'
    subprocess.call(['python',step_1,'-update',str(args.update)])
    subprocess.call(['python',step_2])
    subprocess.call(['python',step_3])
    subprocess.call([step_4],shell=True)
    print("Setup Finished")

  
if __name__== "__main__":
	main()
