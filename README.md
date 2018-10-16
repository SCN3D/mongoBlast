# mongoBlast
OS: Ubuntu 14.04
Python: Python 2.7.15rc1
Mongodb: v3.2.21 

Install MongoDB and Blast:  
1. install mongoDB：
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install mongodb-org
refer to
https://stackoverflow.com/questions/28945921/e-unable-to-locate-package-mongodb-org
2.cd /  
3.sudo mkdir -p data/db  
4.sudo chmod 777 /data/db  
5.pip install pymongo
6.pip install feedparser
7.pip install crontab
8.pip install configparser

Run:  
1.mongod
2.(First time setup)Run: python getuniprottxt.py && uniprotCreateDB.py -update 1 && python DBtoF.py && python tableGenerator.py  
2.When user query:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1)formatdb -i background_seqs.fasta -p T  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2)blastp -task blastp -query ../../mongoBlast/mongo_blast/query_seqs.fasta -db ../../mongoBlast/mongo_blast/background_seqs.fasta -evalue 1e-5 -num_descriptions 100000 -num_alignments 100000 -out format8.txt

3.Functions:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3)Generate display(data/input1.txt): python blastoutput.py  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4)Generate ptm position(data/input2.txt): python ptmPosition.py -ptm Phosphoserine  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5)Generate annotations(data/*.fasta): python ptmAnnotation.py -ptms Phosphoserine....   




