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

Run:  
1.(first time)go to mongodb folder run: python getuniprottxt.py && python uniprotCreateDB.py && python tableGenerator.py  
2.go to blast folder(when user query):  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1)python DBtoF.py -out background_seqs(get fasta db from mongodb)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2)formatdb -i background_seqs.fasta -p T  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3)blastall -p blastp -i query_seqs.fasta -d background_seqs.fasta -e 1e-5 -v 100000 -b 100000 -m 0 -o out.txt  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4)blastall -p blastp -i query_seqs.fasta -d background_seqs.fasta -e 1e-5 -v 100000 -b 100000 -m 8 -o format8.txt  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5)python ptmPosition.py -ptms Phosphoserine (get ptm positions relative to query)----file require:format8.txt  




