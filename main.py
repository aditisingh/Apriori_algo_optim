import pygtrie as trie
import itertools
import string

filename='transactionDB1.txt'

f=open(filename,'r')
transaction_DB=[line.split(' ') for line in f.readlines()]

for i in range(len(transaction_DB)):
	transaction_DB[i][-1]=string.replace(transaction_DB[i][-1],'\n','')

num_transactions=len(transaction_DB)

minsup_count=2
k=7

words=open(filename).read().split()

t=trie.StringTrie()

#Create a trie with it
itemset_1=[]
idx=0
for x in words:
	if x not in itemset_1:
		itemset_1.append(x)
		t[x]=idx
		idx=idx+1

#for every transaction find subsets of size 1
sz=1
for i in range(len(transaction_DB)):
	curr=list(itertools.combinations(transaction_DB[i],sz))
	for j in range(len(curr)):
		subset=curr[j]
		print(t[subset[0]])
