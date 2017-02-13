#!/usr/bin/env python

import pygtrie as trie
import itertools
import string
import numpy as np
import sys
import time

def get_support_vals(t, x, node):
	support_vals=np.zeros((1,node))
	for sz in range(1, len(max(x,key=len))+1):
		for transaction in x: #for every transaction
			curr=list(itertools.combinations(transaction,sz))
			for i in range(len(curr)):
				key=str(curr[i][0])
				for j in range(1,len(curr[i])):
					key=key+'/'+str(curr[i][j])
				#constructed key
				if(t.has_key(key)):	#add it
					node_val=t.__getitem__(key)
					support_vals[0][node_val]=support_vals[0][node_val]+1
	for key in t.keys():
		idx=t[key]
		t[key]=support_vals[0][idx]
	return t;

def pruning_trie(t,minsup_count):
	for word in list(t):
		if t[word]<minsup_count:
			del t[word]
	return t;

start = time.clock()

total=len(sys.argv)

#Check the number of commandline arguments
if(total!=5):
	print('Invalid number of arguments, try again. Expected: prog_exe min_sup k input_transaction_file_path output_file_path')
	sys.exit()

minsup_count=int(sys.argv[1])
k=int(sys.argv[2])

filename=str(sys.argv[3])#'transactionDB2.txt'
out=str(sys.argv[4]) # output file

f=open(filename,'r')
transaction_DB=[line.split(' ') for line in f.readlines()]

for i in range(len(transaction_DB)):
	transaction_DB[i][-1]=string.replace(transaction_DB[i][-1],'\n','')

num_transactions=len(transaction_DB)

if(k>len(max(transaction_DB,key=len))):
	print('Value of k cannot be larger than longest transaction')
	sys.exit()

words=np.unique(open(filename).read().split())	#contains all words unique
words.sort()
words=words.tolist()

t=trie.StringTrie()

#Create first trie 
count=0
for x in words:
	t[x]=count
	count=count+1

#Candidate generation
i=0
while(i<len(t.keys())):
	element=t.keys()[i].split('/')
	idx=words.index(element[-1])
	gr_idx=words[idx+1:]
	for n in range(len(gr_idx)):
		element_2=str(t.keys()[i])+'/'+str(gr_idx[n])
		if(~t.has_key(element_2)):
			t[element_2]=count+1
		count=count+1
	i=i+1

# all candidates ready

#Next, we get all the support count for each candidate
t=get_support_vals(t,transaction_DB,1+max(t.values()))

#pruning operation
t=pruning_trie(t,minsup_count)

print(t)
print ('Total execution time: ' + str(time.clock() - start)+ ' seconds')