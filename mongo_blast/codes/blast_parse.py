# OS: Ubuntu, 18.04.1 LTS
# Python: Python 2.7.15
# Mongodb: v3.2.21 
# Siteng Cai
import sys
import os.path
import argparse
import re
import itertools
import functions

# for debug
log_file = open("ptm_log.txt","w")

# a data structure to hold deletion info
class deletion_data:
    def __init__(self, pos, seq):
        self.pos = pos
        self.seq = seq


def reposition_seq(str,pad): #for output alignment
	len_str = len(str) + pad * 60
	return str.rjust(len_str)


def is_int(str):
	try:
		int(str)
	except ValueError:
		return False
	else:
		return True

#formating string for display
def prepare(id,relative_positions):
	out_data = id
	for i in relative_positions:
		out_data += ' '+str(i)
	return out_data + '\n'

def get_ptms(ptm,table,s_p,e_p,insertions,deletions,seqs):
    """
    calculate ptm indexes

    parameters:
    ptm: a list contains ptms
    table: the table in mongodb
    s_p: a list contains sequence start index for each id
    e_p: a list contains sequence end index for each id
    inserions: a list contains insertion indexes for each sequence
    deletions: a list contains deletion indexes for each sequence
    seqs: print ready sequences

    output: 
    ab_ptms: a list of print ready ptms 
    """
    ab_ptms = dict()
    for id in seqs:
        ab_ptms[id] = []
        data = table.find_one({'_id': id})
        pad = re.match(r"^\.+",seqs[id])
        if pad == None:
            pad = 0
        else:
            pad = len(pad.group(0))
        
        if ptm in data:
            print("ID: "+ id + " PTM: "+ptm)
            for i in data[ptm]:
                if id == 'KKCC2_RAT':
                    print("KKCC2_RAT start: "+ str(s_p[id]) + " end:" + str(e_p[id]))
                if int(i) >= s_p[id] and int(i) <= e_p[id]:
                    
                    out_ptm = int(i) - s_p[id] + pad + 1
                    if id == 'KKCC2_RAT':
                        print("id: "+str(id)+"   outptm before: "+str(out_ptm))

                    delete = False
                    
                    #if has both insert and delete
                    if id in insertions and id in deletions:
                        insert_pop = True
                        delete_pop = True

                        insert_ptr = 0
                        delete_ptr = 0
                        insert_len = len(insertions[id])
                        delete_len = len(deletions[id])
                        while insert_ptr <= insert_len or delete_ptr <= delete_len:
                            if insert_pop == True:
                                if insert_ptr < insert_len:
                                    j = insertions[id][insert_ptr]
                                    insert_ptr += 1 
                                else:
                                    j = [e_p[id],e_p[id]+1]   
                            if delete_pop == True:
                                if delete_ptr < delete_len:
                                    k = deletions[id][delete_ptr]
                                    delete_ptr += 1
                                else:
                                    k = deletion_data(e_p[id]+2,'THIS_MEANS_NO_DELETE')
                            #if meet insetions 
                            insert_pop = True
                            delete_pop = True
                            if j[0] < k.pos:
                                if out_ptm > j[0]:
                                    out_ptm = out_ptm + j[1] - j[0]
                                    if id == 'KKCC2_RAT':
                                        print("outptm now: "+str(out_ptm)+"  j[0]: "+str(j[0])+"  j[1]: "+str(j[1]))
                                    delete_pop = False
                                    insert_pop = True
                                else:
                                    None
                                    if id == 'KKCC2_RAT':
                                        print("outptm now2:"+str(out_ptm)+"  j[0]: "+str(j[0])+"  j[1]: "+str(j[1]))
                            #if meet deletions 
                            elif k.pos < j[0]:
                                if out_ptm > k.pos: 
                                    if out_ptm <= k.pos+len(k.seq):
                                        if id == 'KKCC2_RAT':
                                            print("outptm now:"+str(out_ptm)+" delet start postion: "+str(k.pos)+ " delete string: "+str(k.seq))
                                        delete = True
                                        break
                                    else:  
                                        out_ptm -= len(k.seq)
                                        delete_pop = True
                                        insert_pop = False
                                        if id == 'KKCC2_RAT':
                                            print("insert index: "+str(insert_ptr))
                                            print("delete length: "+ str(len(k.seq)) + " string: "+str(k.seq))
                                            print("outptm now:"+str(out_ptm)+" position: "+str(k.pos)) 
                            else:
                                print("if see it, means something wrong when both insert and delete exist") 

                            #if ptm is less than both insertion and deletion indexes  
                            if delete_pop == True and insert_pop == True:
                                break
                    #if only have insert
                    elif id in insertions :
                        for j in insertions[id]:
                            if out_ptm > j[0]:
                                out_ptm = out_ptm + j[1] - j[0]
                            else:
                                break
                    # if only have delete
                    elif id in deletions:
                        for k in deletions[id]:
                            if out_ptm > k.pos: 
                                if out_ptm <= k.pos+len(k.seq):
                                    delete = True
                                    break
                                else:
                                    out_ptm -= len(k.seq)
             
                    if delete == False:
                        if id == 'KKCC2_RAT':
                            print("outptm now:"+str(out_ptm))
                        #log
                        log_file.write("id: "+id+"\tptm: "+ptm +"\tDB_position: "+str(i)+"\tseq_start: "+str(s_p[id])+"\tseq_end: "+str(e_p[id])+" ADDED!\n")
                        
                        ab_ptms[id].append(out_ptm)
                    else:
                        #log
                        log_file.write("id: "+id+"\tptm: "+ptm +"\tab_position: "+str(out_ptm)+" DELETED!\n")
                else:
                    #log
                    log_file.write("id: "+id+"\tptm: "+ptm +"\tDB_index: "+str(i)+"\tseq_start: "+str(s_p[id])+"\tseq_end: "+str(e_p[id])+" OUT OF RANGE!\n")
    return ab_ptms
  

def get_deletions(fp,pad):
    """
    calculate deletions index

    parameters:
    fp: the file pointer
    pad: an int for number of previous lines 

    output: 
    deletions: a deletion_data type list
    """
    deletions = []
    line = fp.readline()
    indexes = [(m.start() + pad * 60 - 14) for m in re.finditer(r"\|+", line)]# each line has 60 length, 14 is default indents in the output
    
    line = fp.readline()
    line = re.sub("|","",line)
    collapsed = ' '.join(line.split())
    data = collapsed.split(" ")
    
    deletion_strs = []
    
    while len(deletion_strs) < len(indexes):
        if not data:
            line = fp.readline()
            line = re.sub("|","",line)
            collapsed = ' '.join(line.split())
            data = collapsed.split(" ")
        else:
            for d in data:
                deletion_strs.append(d)
    
    for counter, i in enumerate(indexes):
        deletions.append(deletion_data(i,deletion_strs[counter]))
    
    return deletions

#dont need this function anymore
def get_ids(fp):
    """
    get all ids into a list, later can translate to ncbi ac 
    """
    tag = "tag!"
    while tag != "Sequences":
        collapsed = ' '.join(fp.readline().split())
        data = collapsed.split(" ")
        tag = data[0]
    fp.readline()# skip redundent info
    ids = []
    line = fp.readline()
    
    while line != "\n":
        collapsed = ' '.join(line.split())
        data = collapsed.split(" ")
        ids.append(data[0])
        line = fp.readline()
    return ids

def get_inserts(string):
    """
    find all insertion indexes

    parameters:
    string: the whole sequence string after read through file without deletions
    """
    inserts = [m.span() for m in re.finditer("-+", string)]
    for counter, i in enumerate(inserts):
        inserts[counter] = [x for x in i]
        #print(inserts[counter])
    return inserts # m.start() => inserts[0]; m.end() => inserts[1] 
    
def display_output(q_seq,output,identities,fp):
    """
    write final display seq output to file

    parameters:

    q_seq: user query sequence
    output: a list of print ready sequences for each id
    identities: a list of identity for each id
    fp: output file pointer

    """
    q_id = '{:14}'.format("Query_1")
    fp.write(q_id + q_seq + "\n")
    for id in output:
        fp.write('{:14}'.format(id) + output[id] + '{:8}'.format(identities[id]) +  "\n")
    
def display_ptm(ptm,ptm_fp,output):
    """
    write print ready ptm positions to file

    parameters:
    ptm: a list contains ptm for each id
    ptm_fp: ptm position file pointer

    """
    for id in output:
        out = prepare(id,ptm[id])
        #if len(ptm[id]) > 0:
        #	print(ptm_fp.name+": "+out)
        ptm_fp.write(out)
    
def get_identities(input_folder):
    """
    get identities from format6 output

    """
    out = dict()
    file_name = input_folder+'/format6.txt'
    fp = open(file_name)
    line = fp.readline()
    while line:
        collapsed = ' '.join(line.split())
        data = collapsed.split(" ")
        id = data[1].split("|")[1]
        identity = data[2]
        out[id] = identity
        line = fp.readline()
    return out
    
    
def blast_output(filepath,ptms,out_folder):
    """
    main function to generate display from blast output
    and write to files
    """
    file = []
    
    for ptm in ptms:
        file.append(open(out_folder+'/'+ptm+'.txt','w'))
    
    table = functions.connectMongoDB('uniprot','table')
    out_file = open(out_folder+'/blast_output.txt','w')
    
    seqs_start_position = 0
    seqs_end_position = 0
    output = dict()
    ac_deletions = dict()
    insertions = dict()
    ab_ptms = dict()
    
    fp = open(filepath)
    line = fp.readline()
    
    sequence_pad = -1
    
    
    while line:
        collapsed = ' '.join(line.split())
        data = collapsed.split(" ")
        tag = data[0]
        # 1. read blast result sequences
        if tag == 'Query_1': #blast result start
            sequence_pad += 1
            temp_q_end = int(data[3])
            q_seq = data[2]
            seqs_start_position = line.find(data[2]) # start position in txt
            seqs_end_position = line.find(data[3]) - 2 # end position in txt     
            seqs_end_index = dict() # sequence end index
            seqs_start_index = dict() # sequence start index
    
            line = fp.readline()
            collapsed = ' '.join(line.split())
            data = collapsed.split(" ")
            
            prev_ac = ""

            while line and data[0] != "Lambda":
                if data[0] == 'Query_1': # if its query
                    sequence_pad += 1
                    seqs_start_position = line.find(data[2])
                    seqs_end_position = line.find(data[3]) - 2
                    if temp_q_end == int(data[1])-1:
                        temp_q_end = int(data[3])
                        q_seq += data[2]
                    else:
                        print("special case!")
                elif len(data) == 4 and is_int(data[1]) and is_int(data[3]): # if its subjects
                    if data[0] in output: # if its not head
                        prev_ac = data[0]
                        seqs_end_index[data[0]] = int(data[3])
                        output[data[0]] += line[seqs_start_position:seqs_end_position]
                    else: # if its head
                        prev_ac = data[0]
                        seqs_start_index[data[0]] = int(data[1])
                        seqs_end_index[data[0]] = int(data[3])
                        output[data[0]] = reposition_seq(line[seqs_start_position:seqs_end_position],sequence_pad)
                elif data[0] == '\\':
                    if prev_ac in ac_deletions:
                        delete = get_deletions(fp,sequence_pad)
                        ac_deletions[prev_ac] += delete
                    else:
                        delete = get_deletions(fp,sequence_pad)
    
                        ac_deletions[prev_ac] = delete
                line = fp.readline()
                
                collapsed = ' '.join(line.split())
                data = collapsed.split(" ")	
            
            ##########check ptms
            #for id in ids:
            #	temp = table.find_one({"_id": id})
            #	for ptm in ptms:
            #		if ptm in temp:
            #			print(temp[ptm])
            ##################
        
            # preprocess data

            for id in output:
                output[id] = output[id].ljust(len(q_seq))
                output[id] = output[id].replace(" ",".")
                insertions[id] = get_inserts(output[id])
                dict((k, v) for k, v in insertions.iteritems() if v)
    
            #############check deletions
            #for i in ac_deletions:
            #	for j in ac_deletions[i]:
            #		print("id: "+i+"\tpos: "+str(j.pos)+"\tseq: "+j.seq)
            #####################
    
            # ptm position is relative to the line in the file not sequence now
            for counter, ptm in enumerate(ptms):
                # generate the ptm position for display
                ab_ptms = get_ptms(ptm,table,seqs_start_index,seqs_end_index,insertions,ac_deletions,output) #TODO check if ids are right
                display_ptm(ab_ptms,file[counter],output) #TODO one more ids
            identities = get_identities(out_folder)
            display_output(q_seq,output,identities,out_file) #TODO ids here
    
        line = fp.readline()
    
    
    out_file.close()
    fp.close()
    for index, ptm in enumerate(ptms):
        file[index].close()
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', default='format2.txt',help="local filepath")
    parser.add_argument('-ptms', default='Phosphotyrosine', help="ptms ptm1_ptm2_ptm3...")
    parser.add_argument('-o', default='display',help="output folder name")
    args = parser.parse_args()
    filepath = args.l
    ptms = args.ptms.split('_')
    out_folder = args.o
    
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    
    if os.path.exists(filepath):
        blast_output(filepath,ptms,out_folder)	
    else:
        print("File does not exist\n")
        sys.exit()
    
if __name__== "__main__":
    main()
log_file.close()