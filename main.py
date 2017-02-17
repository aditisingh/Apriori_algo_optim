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
			# print(t)
			# print(key)
			# print('\n')
			if(t.has_key(key)):	#add it
				node_val=t.__getitem__(key)
				support_vals[0][node_val]=support_vals[0][node_val]+1
	for key in t.keys():
		if(key.count('/')==sz-1):
			idx=t[key]
			t[key]=support_vals[0][idx]
			# print(t[key])
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

sz=1
print('Size: '+str(sz))
t=trie.StringTrie()

count=0

for x in word_index:
	t[str(x)]=count
	count=count+1

print('Candidate generation done in '+ str(time.clock() - pt_1)+ ' seconds')
f_o=open(out,'r+')
pt_2= time.clock()
t=get_support_vals(t,transaction_DB,1+max(t.values()),sz) 
print('Support values generation done in '+ str(time.clock() - pt_2)+ ' seconds')
pt_3=time.clock()
t=pruning_trie(t,minsup_count,sz)
print('Pruning done in '+ str(time.clock() - pt_3)+ ' seconds')
pt_4=time.clock()
if(k<=sz):
	l=list(t)
	l1=[ll for ll in l if ll.count('/')==sz-1]
	for key in l1:
		value=int(t.__getitem__(key))
		list_element=key.split('/')
		list_element.sort(key=int)
		for element in list_element:
			f_o.write(str(words[int(element)])+' ')
		f_o.write('\t ('+str(value)+') \n')
print('Writing done in '+ str(time.clock() - pt_4)+ ' seconds')
print('\n')

for sz in range(2, 1+len(max(transaction_DB,key=len))):
	print('Size: '+str(sz))
	pt_5=time.clock()
	add1=0
	l=list(t)
	l1=[ll for ll in l if ll.count('/')==0]
	l2=[ll for ll in l if ll.count('/')==sz-2]
	if(len(l2)==0):
		break
	# l=l1+l2
	candidates=list(itertools.product(l1,l2))
	for c in candidates:
		element='/'.join(c)
		if(element.count('/')==sz-1):
			ll=element.split('/')
			ll.sort(key=int)
			element='/'.join(ll)
			result = list(( ll.count(i)) for i in ll)
			if(sum(result)-len(result)==0):
				t[element]=count+1
				add1=add1+1
				count=count+1
	# print(t)
	#No new candidates generated
	if(add1==0):
		break
	# print('\n')
	print('Candidate generation done '+ str(time.clock() - pt_5)+ ' seconds')
	pt_2= time.clock()
	t=get_support_vals(t,transaction_DB,1+max(t.values()),sz) # prune outside
	print('Support values generation done in '+ str(time.clock() - pt_2)+ ' seconds')
	# print(t)
	pt_3=time.clock()
	t=pruning_trie(t,minsup_count,sz)
	print('Pruning done in '+ str(time.clock() - pt_3)+ ' seconds')
	# print(t)
	pt_4=time.clock()
	if(k<=sz):
		l=list(t)
		l1=[ll for ll in l if ll.count('/')==sz-1]
		for key in l1:
			value=int(t.__getitem__(key))
			list_element=key.split('/')
			list_element.sort(key=int)
			for element in list_element:
				f_o.write(str(words[int(element)])+' ')
			f_o.write('\t ('+str(value)+') \n')
		print('Writing done in '+ str(time.clock() - pt_4)+ ' seconds')
	print('\n')
	# j=0
	
f_o.close()

print ('Total execution time: ' + str(time.clock() - start)+ ' seconds')