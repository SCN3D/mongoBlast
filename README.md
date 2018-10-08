# mongoBlast
OS: Ubuntu, 18.04.1 LTS
Python: Python 2.7.15rc1
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
1.(First time setup)Run: python getuniprottxt.py && uniprotCreateDB.py -update 1 && python DBtoF.py && python tableGenerator.py  
2.When user query:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1)formatdb -i background_seqs.fasta -p T  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2)blastall -p blastp -i query_seqs.fasta -d background_seqs.fasta -e 1e-5 -v 100000 -b 100000 -m 8 -o format8.txt  
3.Functions:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3)Generate display(data/input1.txt): python blastoutput.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4)Generate ptm position(data/input2.txt): python ptmPosition.py -ptm Phosphoserine  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5)Generate annotations(data/*.fasta): python ptmAnnotation.py -ptms Phosphoserine....   




