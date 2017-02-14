#!/usr/bin/env python

import pygtrie as trie
import itertools
import string
import numpy as np
import sys
import time

def get_support_vals(t, x, node, sz): #not working for >=2 number of itemsets
	support_vals=np.zeros((1,node))	
	for transaction in x: #for every transaction
		curr=list(itertools.combinations(transaction,sz))
		for i in range(len(curr)):
			key=str(word_index[curr[i][0]])
			for j in range(1,len(curr[i])):
				key=key+'/'+str(word_index[curr[i][j]])
			#constructed key
			print(t)
			print(key)
			print('\n')
			if(t.has_key(key)):	#add it
				node_val=t.__getitem__(key)
				support_vals[0][node_val]=support_vals[0][node_val]+1
	for key in t.keys():
			idx=t[key]
			t[key]=support_vals[0][idx]
	return t;

def pruning_trie(t,minsup_count,sz):
	for word in list(t):
		if word.count('/')==(sz-1):
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
word_index=range(len(words)) #conversion of words to int

for i in range(len(transaction_DB)):
	for j in range(len(transaction_DB[i])):
		transaction_DB[i][j]=word_index[words.index(transaction_DB[i][j])]
	transaction_DB[i].sort() #sorting every transaction_DB

print ('Argument reading time: ' + str(time.clock() - start)+ ' seconds')
pt_1= time.clock()

t=trie.StringTrie()

count=0

for x in word_index:
	t[str(x)]=count
	count=count+1

f_o=open(out,'r+')
for sz in range(1, len(max(transaction_DB,key=len))):
	t=get_support_vals(t,transaction_DB,1+max(t.values()),sz)
	t=pruning_trie(t,minsup_count,sz)
	if(k<=sz):
		for i in range(len(t.keys())):
			key=t.keys()[i]
			value=int(t.__getitem__(key))
			f_o.write(str(words[int(key)])+'\t ('+str(value)+') \n')
	j=0
	while(j<len(t.keys())):
		element=t.keys()[j].split('/')
		idx=word_index.index(int(element[-1]))
		gr_idx=word_index[idx+1:]
		add=0
		for n in range(len(gr_idx)):
			element_2=str(t.keys()[j])+'/'+str(gr_idx[n])
			if(~t.has_key(element_2)):
				t[element_2]=count+1
				count=count+1
				add=add+1
		j=j+1+add
f_o.close()

for i in range(len(t.keys())):
	key=t.keys()[i]
	value=int(t.__getitem__(key))
	f_o.write(str(words[int(key)])+'\t ('+str(value)+')')




#Candidate generation
i=0
while(i<len(t.keys())):
	element=t.keys()[i].split('/')
	idx=word_index.index(int(element[-1]))
	gr_idx=word_index[idx+1:]
	for n in range(len(gr_idx)):
		element_2=str(t.keys()[i])+'/'+str(gr_idx[n])
		if(~t.has_key(element_2)):
			t[element_2]=count+1
		count=count+1
	i=i+1

print ('Candidate generation time: ' + str(time.clock() - pt_1)+ ' seconds')
pt_2= time.clock() 

# all candidates ready

#Next, we get all the support count for each candidate
t=get_support_vals(t,transaction_DB,1+max(t.values()),k,1)

print ('Support value calculation time: ' + str(time.clock() - pt_2)+ ' seconds')
pt_3= time.clock()

#pruning operation
t=pruning_trie(t,minsup_count)

print ('Pruning operation time: ' + str(time.clock() - pt_3)+ ' seconds')

print(t)
print ('Total execution time: ' + str(time.clock() - start)+ ' seconds')