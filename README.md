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
5.sudo apt install blast2

Crontab:
1.pip uninstall crontab
2.pip install python-crontab

Run:
1 mongod

2 (First time setup)Run: python uniprotCreateDB.py -update 1 && python DBtoF.py && python tableGenerator.py

3 When user query:(blast+)
      
      1)formatdb -i background_seqs.fasta -p T
      
      2)blastall -p blastp -i query_seqs.fasta -d background_seqs.fasta -e 1e-5 -v 100000 -b 100000 -m 8 -o format8.txt
      blastall -p blastp -i query_seqs.fasta -d background_seqs.fasta -e 1e-5 -v 100000 -b 100000 -m 11 -o format11.txt -J T
      
      blastp -task blastp -query query_seqs.fasta -db background_seqs.fasta -evalue 1e-5 -num_descriptions 100000 -num_alignments 100000 -outfmt 2 -out format2.txt
4 Functions:
      
      3)Generate display(data/blast_output.txt): python blastoutput.py
      
      4)Generate ptm position(data/.txt): python ptmPosition.py -ptm Phosphoserine
      
      5)Generate annotations(data/.fasta): python annotations.py -ptms Phosphoserine....
