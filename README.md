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
2.(First time setup)Run: python setup.py -update 1  
3.When user query: python user_query.py -ptms ptm ptm ptm  
4.Outputs:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;----output1: display/blast_out.txt (disaplay sequences)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;----output2: display/*.txt (ptm positions)  


