#!/usr/bin/env python

import itertools
import string
import numpy as np
import sys
import time
import os

#To get the support values for all the candidates generated of size sz
def get_support_vals(dict2, x, node, sz):
	support_vals=np.zeros((1,node))	
	for transaction in x: #for every transaction in transaction database
		for curr in itertools.combinations(transaction,sz): #find combinations of size sz
			key='/'.join(str(x) for x in (curr))#constructed key using transaction combination
			if(dict2.get(key)):	#if the key is in dictionary
				node_val=dict2[str(key)] #find unique index for the key
				support_vals[0][node_val]=support_vals[0][node_val]+1 #increment support value
	for key,value in dict2.iteritems():
		if(key.count('/')==sz-1): #for the sz sized keys
			idx=dict2[key] #get unique index for key
			dict2[key]=support_vals[0][idx] #update the value as the support value
	return dict2;

total=len(sys.argv)
start=time.clock()

#Check the number of commandline arguments
if(total!=5):
	print('Invalid number of arguments, try again. Expected: prog_exe min_sup k input_transaction_file_path output_file_path')
	sys.exit()

minsup_count=int(sys.argv[1]) #The minimum support count
k=int(sys.argv[2])	#k value, k+ sized itemsets will be printed

filename=str(sys.argv[3]) #input file
out=str(sys.argv[4]) #output file
#Fixing the format of the output file
out=out.split('/')
out[-1]='out_s='+str(minsup_count)+'_k='+str(k)+'+.txt'
out='/'.join(out)

os.mknod(out) #creating the output file

f=open(filename,'r')
transaction_DB=[line.split(' ') for line in f.readlines()] #Storing the database

#Removing the newline character from the database
for i in range(len(transaction_DB)):
	transaction_DB[i][-1]=string.replace(transaction_DB[i][-1],'\n','')

if(k>len(max(transaction_DB,key=len))):
	print('Value of k cannot be larger than longest transaction')
	sys.exit()

words=np.unique(open(filename).read().split())	#contains all words unique
words.sort() #Sorting the words, and saving to list
words=words.tolist()
word_index=range(len(words)) #conversion of words to int

#Converting the database from string to int
for i in range(len(transaction_DB)):
	for j in range(len(transaction_DB[i])):
		transaction_DB[i][j]=word_index[words.index(transaction_DB[i][j])]
	transaction_DB[i].sort() #sorting every transaction_DB

#Candidate generation for size 1 itemset, with unique value for each key
sz=1
dict2={}
count=0

for i in word_index:
	dict2[str(i)]=count+1
	count=count+1

f_o=open(out,'r+')

#Discard the database which is of size<sz, it won't be of help to calculate support values
#This will help in faster computation, will be helpful with large sizes sz
transaction_DB=[transaction for transaction in transaction_DB if len(transaction)>=sz]
#SUPPORT VALUE CALCULATION
#Find support values for all keys of size=sz and replacing their value with the support values
dict2=get_support_vals(dict2,transaction_DB,count+1,sz) 

#FREQUENT ITEMSET DETECTION
#pruning, since dictionary size can't be changed while iterating over it, we declare a new dictionary, and copy the frequent itemsets
dict1={}
for key in dict2:
		if dict2[key]>=minsup_count:
			dict1[key]=dict2[key]
#Copying back
dict2=dict1

#Discard the transactions which don't have a single frequent itemset of size sz 
#these transactions won't be used to find support values for any sz+ itemsets
for transaction in transaction_DB:
	cnt=0
	for key, value in dict2.iteritems():
		if(int(key) in transaction):
			cnt=cnt+1
			break
	if(cnt==0):
		transaction_DB.remove(transaction)

#PRINTING 
#Only print itemsets of size >=k
if(k<=sz):
	l=list(dict2)
	l1=[ll for ll in l if ll.count('/')==sz-1]
	for key in l1:
		value=dict2[key]
		list_element=key.split('/')
		list_element.sort(key=int)
		for element in list_element:
			f_o.write(str(words[int(element)])+' ')
		f_o.write('\t ('+str(int(value))+') \n')

#Maximum size of a candidate possible
max_itemset_size=1+len(max(transaction_DB,key=len))

for sz in range(2,max_itemset_size):
	add1=0 #stores number of candidates generated of size sz

	l=list(dict2)
	l1=[ll for ll in l if ll.count('/')==0] #getting 1 size itemsets
	l2=[ll for ll in l if ll.count('/')==sz-2] #getting sz-1 sized itemsets
	#if no itemsets of size sz-1, terminate 
	if(len(l2)==0):
		break
	#CANDIDATE GENERATION
	#join sz-1 sized with size 1 itemset to generate possible candidates
	for c in itertools.product(l1,l2):
		element='/'.join(c) #join them 
		ll=element.split('/') #get all elements
		ll=list(set(ll))
		ll.sort(key=int) #sort
		if(element.count('/')==sz-1 and len(ll)==sz):
			element='/'.join(ll)
			#join to a make a itemset
			result = list(( ll.count(i)) for i in ll)
			if(sum(result)-len(result)==0): #only unique values find
				dict2[element]=count+1
				add1=add1+1
				count=count+1
	#No new candidates generated
	if(add1==0):
		break
	#discard the transactions with size smaller than sz
	transaction_DB=[transaction for transaction in transaction_DB if len(transaction)>=sz]

	#getting the support values for sz sized itemsets
	dict2=get_support_vals(dict2,transaction_DB,count+1,sz) 
	#prune the dictionary
	dict1={}
	for key in dict2:
			if dict2[key]>=minsup_count:
				dict1[key]=dict2[key]
	dict2=dict1
	#printing out
	if(k<=sz):
		l=list(dict2)
		l1=[ll for ll in l if ll.count('/')==sz-1]
		for key in l1:
			value=dict2[key]
			list_element=key.split('/')
			list_element.sort(key=int)
			for element in list_element:
				f_o.write(str(words[int(element)])+' ')
			f_o.write('\t ('+str(int(value))+') \n')
	#remove those transactions, with no sz sized frequent itemsets
	for transaction in transaction_DB:
		cnt=0
		for key, value in dict2.iteritems():
			if(key.count('/')==sz-1):
				elements=key.split('/')
				cnt=cnt+min(transaction.count(int(e)) for e in elements)
		if(cnt==0):
			transaction_DB.remove(transaction)
	
f_o.close()

#print ('Total execution time: ' + str(time.clock() - start)+ ' seconds')