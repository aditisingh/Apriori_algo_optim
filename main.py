import pygtrie as trie
import itertools
import string
import numpy as np
import sys

def get_support_vals(trie.StringTrie t,list x, int sz, int node):
	support_vals=np.zeros((node,1))
	for transaction in x: #for every transaction
		curr=list(itertools.combinations(transaction,sz))
		for i in range(len(curr)):
			key=str(curr[i][0])
			for j in range(1,len(curr[i])):
				key=key+'/'+str(curr[i][j])
			#constructed key
			if(t.has_key(key)):	#add it
				node_val=t.__getitem__(key)
				support_vals[node_val]=support_vals[node_val]+1
	return support_vals


total=len(sys.argv)
#Check the number of commandline arguments
if(total!=3):
	print('Invalid number of arguments, try again.')
	sys.exit()

minsup_count=int(sys.argv[0])
k=int(sys.argv[1])

filename=str(sys.argv[2])#'transactionDB2.txt'

f=open(filename,'r')
transaction_DB=[line.split(' ') for line in f.readlines()]

for i in range(len(transaction_DB)):
	transaction_DB[i][-1]=string.replace(transaction_DB[i][-1],'\n','')

num_transactions=len(transaction_DB)

if(k>len(max(transaction_DB,key=len))):
	print('Value of k cannot be larger than longest transaction')
	sys.exit()

words=np.unique(open(filename).read().split())	#contains all words unique

t=trie.StringTrie()

#Create first trie 
count=0
for x in words:
	t[x]=count
	count=count+1

#Get support values
support_vals=get_support_vals(t,transaction_DB)

#for every transaction find subsets of size 1
sz=1
support_vals=np.zeros((max(t.values()),1))
#fix
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