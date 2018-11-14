# mongoBlast
OS: Centos
Python: Python 2.7.15rc1
Mongodb: v3.2.21 

Install MongoDB and Blast:  
1.sudo yum install mongodb-org
2.cd /  
3.sudo mkdir -p data/db  
4.sudo chmod 777 /data/db  
5.pip install pymongo
6.pip install feedparser
7.pip install crontab
8.pip install configparser

Run:  
1.mongod
2.(First time setup)Run: python getuniprottxt.py && python uniprotCreateDB.py -update 1 && python DBtoF.py && python tableGenerator.py  
2.When user query:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1)makeblastdb -in background_seqs.fasta -dbtype prot  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2) blastp -task blastp -query query_seqs.fasta -db background_seqs.fasta -evalue 1e-5 -num_descriptions 100000 -num_alignments 100000 -outfmt 2 -out format2.txt

3.Functions:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3)Generate display(data/input1.txt): python blastoutput.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4)Generate ptm position(data/input2.txt): python ptmPosition.py -ptm Phosphoserine  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5)Generate annotations(data/*.fasta): python ptmAnnotation.py -ptms Phosphoserine....   




