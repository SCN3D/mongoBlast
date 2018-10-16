# mongoBlast
OS: Ubuntu, 18.04.1 LTS  
Python: Python 2.7.15  
Mongodb: v3.2.21  

Install MongoDB and Blast:  
1.sudo apt install mongodb-server-core  
2.cd /  
3.sudo mkdir -p data/db  
4.sudo chmod 777 /data/db  
5.sudo apt install blast2  

Crontab:  
1.pip uninstall crontab  
2.pip install python-crontab  

Run:  
1. mongod
2.(First time setup)Run: python uniprotCreateDB.py -update 1 && python DBtoF.py && python tableGenerator.py  
3.When user query:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1)formatdb -i background_seqs.fasta -p T  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2)blastall -p blastp -i query_seqs.fasta -d background_seqs.fasta -e 1e-5 -v 100000 -b 100000 -m 8 -o format8.txt  
4.Functions:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3)Generate display(data/blast_output.txt): python blastoutput.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4)Generate ptm position(data/*.txt): python ptmPosition.py -ptm Phosphoserine  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5)Generate annotations(data/*.fasta): python annotations.py -ptms Phosphoserine....  




