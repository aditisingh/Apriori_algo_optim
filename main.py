import pygtrie as trie
import itertools
import string
import numpy as np

filename='transactionDB2.txt'

f=open(filename,'r')
transaction_DB=[line.split(' ') for line in f.readlines()]

for i in range(len(transaction_DB)):
	transaction_DB[i][-1]=string.replace(transaction_DB[i][-1],'\n','')

num_transactions=len(transaction_DB)

minsup_count=5
k=7

if(k>len(max(transaction_DB,key=len))):
	print('Value of k cannot be larger than longest transaction')

words=open(filename).read().split()

t=trie.StringTrie(enable=True)

#Create a trie with it
itemset_1=[]
idx1=0
for x in words:
	if x not in itemset_1:
		itemset_1.append(x)
		t[x]=idx1
		idx1=idx1+1


#for every transaction find subsets of size 1
sz=1
support_vals=np.zeros((len(t.keys()),1))

for i in range(len(transaction_DB)):
	curr=list(itertools.combinations(transaction_DB[i],sz))
	for j in range(len(curr)):
		subset=curr[j]
		if sz==1:
			print(t[subset[0]])
			support_vals[t[subset[0]]]=support_vals[t[subset[0]]]+1
		else:
			print(t[subset[0:len(subset)-1]])
			support_vals[t[subset[0:len(subset)-1]]]=support_vals[t[subset[0:len(subset)-1]]]+1

for k in range(len(itemset_1)):
	word=itemset_1[k]
	if(support_vals[t[word]]<minsup_count):
		del t[word]

#sort the previous itemset
itemset_1.sort()

i=0

while(i<len(t.keys())):
	element=t.keys()[i]
	idx=itemset_1.index(element)
	gr_idx=itemset_1[idx+1:]
	for j in range(len(gr_idx)):
		element_2=str(element)+'/'+str(gr_idx[j])
		t[element_2]=idx1+1
		idx1=idx1+1
	i=i+len(gr_idx)+1

#for every transaction find subsets of size 2
sz=2
support_vals=np.zeros(max(t.values()),1))

for i in range(len(transaction_DB)):
	curr=list(itertools.combinations(transaction_DB[i],sz))
	curr.sort()
	for j in range(len(curr)):
		subset=curr[j]
		if sz==1:
			print(t[subset[j]])
			support_vals[t[subset[j]]]=support_vals[t[subset[j]]]+1
		else:
			word=subset[0]
			for k in range(1,len(subset)):
				word=word+'/'+subset[k]
			print(t[word])
			support_vals[t.__getitem__(word)]=support_vals[t.__getitem__(word)]+1 

for k in range(len(itemset_1)):
	word=itemset_1[k]
	if(support_vals[t[word]]<minsup_count):
		del t[word]