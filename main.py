#!/usr/bin/env python

import pygtrie as trie
import itertools
import string
import numpy as np
import sys
import time
import cProfile

def get_support_vals(dict, x, node, sz): #not working for >=2 number of itemsets
	support_vals=np.zeros((1,node))	
	p1=time.clock()
	for transaction in x: #for every transaction
		comb=list(itertools.combinations(transaction,sz))
		for curr in comb:
			key='/'.join(str(x) for x in (curr))
			#constructed key
			if(key in dict.keys()):	#add it
				node_val=dict[str(key)]
				support_vals[0][node_val]=support_vals[0][node_val]+1
	print('Part1 time: ' + str(time.clock() - p1)+ ' seconds')
	p2=time.clock()
	for key in dict:
		if(key.count('/')==sz-1):
			idx=dict[key] 
			dict[key]=support_vals[0][idx]
			# print(t[key])
	print('Part2 time: ' + str(time.clock() - p2)+ ' seconds')
	return dict;

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
dict={}
count=1
for i in word_index:   
	dict[str(i)]=count
	count=count+1

print('Candidate generation done in '+ str(time.clock() - pt_1)+ ' seconds')
f_o=open(out,'r+')
pt_2= time.clock()
# cProfile.run(get_support_vals(get_support_vals(dict,transaction_DB,count,sz))
dict=get_support_vals(dict,transaction_DB,count,sz) 
print('Support values generation done in '+ str(time.clock() - pt_2)+ ' seconds')
pt_3=time.clock()
# cProfile.run(dict,minsup_count,sz)

#pruning
dict1={}
for key in dict:
		if key.count('/')==(sz-1):
			if dict[key]>=minsup_count:
				dict1[key]=dict[key]
dict=dict1

print('Pruning done in '+ str(time.clock() - pt_3)+ ' seconds')
pt_4=time.clock()
if(k<=sz):
	l=list(dict)
	l1=[ll for ll in l if ll.count('/')==sz-1]
	for key in l1:
		value=dict[key]
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
	l=list(dict)
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
			ll=list(set(ll))
			ll.sort(key=int)
			element='/'.join(ll)
			result = list(( ll.count(i)) for i in ll)
			if(sum(result)-len(result)==0):
				dict[element]=count+1
				add1=add1+1
				count=count+1
	# print(t)
	#No new candidates generated
	if(add1==0):
		break
	# print('\n')
	print('Candidate generation done '+ str(time.clock() - pt_5)+ ' seconds')
	pt_2= time.clock()
	# cProfile.run(get_support_vals(get_support_vals(dict,transaction_DB,count,sz))
	dict=get_support_vals(dict,transaction_DB,count,sz) # prune outside
	
	print('Support values generation done in '+ str(time.clock() - pt_2)+ ' seconds')
	# print(t)
	pt_3=time.clock()
	# cProfile.run(d,minsup_count,sz)
	#pruning
	dict1={}
	for key in dict:
			if key.count('/')==(sz-1):
				if dict[key]>=minsup_count:
					dict1[key]=dict[key]
	dict=dict1
	print('Pruning done in '+ str(time.clock() - pt_3)+ ' seconds')
	# print(t)
	pt_4=time.clock()
	if(k<=sz):
		l=list(dict)
		l1=[ll for ll in l if ll.count('/')==sz-1]
		for key in l1:
			value=dict[key]
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