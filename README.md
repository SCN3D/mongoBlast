# mongoBlast
OS: Ubuntu, 18.04.1 LTS  
Python: Python 2.7.15  
Mongodb: v3.2.21  

Install MongoDB and Blast:  
1.sudo apt install mongodb-server-core  
2.cd /  
3.sudo mkdir -p data/db  
4.sudo chmod 777 /data/db  
5.sudo apt install blast2=2.6.0+  
or download from https://launchpad.net/ubuntu/+source/ncbi-blast+/2.6.0-1  
gunzip xxx.gz  
tar -xvf xxx.tar  
cd c++  
./configure  
cd ReleaseMT/build  
make all_r  
  

Crontab:  
1.pip uninstall crontab  
2.pip install python-crontab  

Run:  
1.mongod  
2.(First time setup)Run: python tableGenerator.py -update 1 && python DBtoF.py && Generate annotations(data/*.fasta): python annotations.py  
3.When user query:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1)formatdb -i background_seqs.fasta -p T  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2)blastall -p blastp -i query_seqs.fasta -d background_seqs.fasta -e 1e-5 -v 20 -b 20 -m 2 -o format2.txt  
4.Functions:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3)Generate display(data/blast_output.txt): python blast_parse.py  -l 'blastoutputpath' -ptms ptm1 ptm2 -o 'output folder name'
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;----output1: data/blast_out.txt (disaplay sequences)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;----output2: data/*.txt (ptm positions)  


