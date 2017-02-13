#!/usr/bin/env python

import pygtrie as trie
import itertools
import string
import numpy as np
import sys

def get_support_vals(t, x, node):
	support_vals=np.zeros((1,node))
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
	return support_vals;

def pruning_trie(t,minsup_count):
	for word in list(t):
		if t[word]<minsup_count:
			del t[word]
	return t;


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

# #Get support values
# sz=1
# support_vals=get_support_vals(t,transaction_DB,sz,1+max(t.values()))
# i=0

# for word in t.keys():
# 	t[word]=support_vals[0][i]
# 	i=i+1

# #pruning operation
# t=pruning_trie(t,minsup_count)

# count_item=1
# longest_transaction=len(words)

# i=0

i=0
while(i<len(t.keys())):
	element=t.keys()[i]
	idx=words.index(element[-1])
	gr_idx=words[idx+1:]
	for n in range(len(gr_idx)):
		element_2=str(element)+'/'+str(gr_idx[n])
		if(~t.has_key(element_2)):
			t[element_2]=count+1
		count=count+1
	i=i+1

# all candidates ready

#Next, we get all the support count for each candidate
support_vals=get_support_vals(t,transaction_DB,1+max(t.values()))


# #sort the previous itemset
# itemset_1.sort()

# i=0

# while(i<len(t.keys())):
# 	element=t.keys()[i]
# 	idx=itemset_1.index(element)
# 	gr_idx=itemset_1[idx+1:]
# 	for j in range(len(gr_idx)):
# 		element_2=str(element)+'/'+str(gr_idx[j])
# 		t[element_2]=idx1+1
# 		idx1=idx1+1
# 	i=i+len(gr_idx)+1

# #for every transaction find subsets of size 2
# sz=2
# support_vals=np.zeros(max(t.values()),1))

# for i in range(len(transaction_DB)):
# 	curr=list(itertools.combinations(transaction_DB[i],sz))
# 	curr.sort()
# 	for j in range(len(curr)):
# 		subset=curr[j]
# 		if sz==1:
# 			print(t[subset[j]])
# 			support_vals[t[subset[j]]]=support_vals[t[subset[j]]]+1
# 		else:
# 			word=subset[0]
# 			for k in range(1,len(subset)):
# 				word=word+'/'+subset[k]
# 			print(t[word])
# 			support_vals[t.__getitem__(word)]=support_vals[t.__getitem__(word)]+1 

# for k in range(len(itemset_1)):
# 	word=itemset_1[k]
# 	if(support_vals[t[word]]<minsup_count):
# 		del t[word]