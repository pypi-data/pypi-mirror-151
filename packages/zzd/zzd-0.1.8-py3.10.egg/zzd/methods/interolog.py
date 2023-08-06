"""
example
python interolog ppi seqs

#mechanism
protein A` is the homolog of protein A
protein B` is the homolog of protein B
if A`-B` have interation then we inference A-B also have interation.

#
1. protein sequences db in which protein also have ppi.
2. seach homolog of input protein pair
3. if any interaction of A`-B` then A-B interaction. vice versa.

"""


import sys
import os
import numpy as np
import pandas as pd
from Bio import SeqIO
import torch.nn as nn
#from zzd import scores


#1 load input ppi and interolog_ppi_db
def load_ppis(ppis_file):
	return  np.genfromtxt(ppis_file,str)


def load_ppis_and_blastdb(ppis_db_file=None,blastdb=None):
	#init download ppidb and blastdb
	os.system("mkdir -p $HOME/.local/interolog/")
	work_dir = os.environ['HOME'] + "/.local/interolog"

	if not blastdb:
		blastdb_file = work_dir+"/blastdb/blastdb.phr"
		if not os.path.exists(blastdb_file):
			os.system(f"wget https://github.com/miderxi/zzd_lib/raw/main/zzd/lib/blastdb.tar.gz\
					-O {work_dir}/blastdb.tar.gz")
			os.system(f"tar -xvf {work_dir}/blastdb.tar.gz -C {work_dir}")

	if not ppis_db_file:
		ppis_db_file = work_dir + "/ppis_db/ppis_db.txt"
		if not os.path.exists(ppis_db_file):
			os.system(f"wget https://github.com/miderxi/zzd_lib/raw/main/zzd/lib/ppis_db.tar.gz \
					 -O {work_dir}/ppis_db.tar.gz")
			os.system(f"tar -xvf {work_dir}/ppis_db.tar.gz -C {work_dir}")	
	ppis_db  = set([tuple(i) for i in  np.genfromtxt(ppis_db_file,str)])
	return ppis_db


#2 search homolog
def search_homolog(ppis, seqs_file,run_blast=True,	blastdb=None):
	work_dir = os.environ['HOME'] + "/.local/interolog"
	if not blastdb:
		blastdb = f"{work_dir}/blastdb/blastdb"
	
	ppis_ids = set([j for i in ppis[:,:2].reshape(-1,2) for j in i])
	seqs = {i.id : str(i.seq) 
		for file_name in seqs_file for i in SeqIO.parse(seqs_file,"fasta") if i.id in ppis_ids}
	
	if run_blast:
		#(1) write ppis fasta to disk	
		with open(f"{work_dir}/seqs.fasta","w") as f:
			for k,v in seqs.items():
				f.write(f">{k}\n{v}\n")
		
		#(2) blastp interolog_ppi_db 
		cmd = f"blastp -query {work_dir}/seqs.fasta \
				-db {blastdb} -out {work_dir}/seqs.blastp -evalue 1e-2 -outfmt 6 -num_threads 12"
		os.system(cmd)

	#(3) extract homolog
	homo = {}
	for line in pd.read_table(f"{work_dir}/seqs.blastp").to_numpy():
		if line[2] > 40:
			if line[0] not in homo.keys():
				homo[line[0]] = set([line[1]])
			else:
				homo[line[0]].add(line[1])
	return homo


#3. make prediction
def prediction(ppis, homo, ppis_db,):
	ppis_pred = []
	for a,b in ppis[:,:2].reshape(-1,2):
		pred = 0
		if a in homo.keys() and b in homo.keys():
			candicate = set([(i,j) for i in  homo[a] for j in homo[b]] +
					    [(j,i) for i in  homo[a] for j in homo[b]]) 
			if candicate & ppis_db:
				pred = 1
		ppis_pred.append(pred)
	return ppis_pred


#4.
def interolog(ppis_file, seqs_file,run_blast=True,blastdb=None,):
	ppis_db = load_ppis_and_blastdb()
	ppis =  load_ppis(ppis_file)	
	homo = search_homolog(ppis, seqs_file,run_blast)
	pred = prediction(ppis, homo, ppis_db)
	return pred 
	
if __name__ == "__main__":
	ppis_file = "../../../atppi/B2_train_and_test/p1n1_tenfolds/test_0.txt"
	seqs_file = "../../../atppi/B1_ppis_and_seqs/ara_and_eff.fasta"
	y_true = load_ppis(ppis_file)[:,2]
	y_pred = interolog(ppis_file, seqs_file,run_blast=False)
	
	scores(y_true,y_pred,show=True)




