import pygtrie as trie
import itertools

filename='transactionDB.txt'

f=open(filename,'r')
transaction_DB=[line.split(' ') for line in f.readlines()]
	
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

#for every transaction find subsets

for 
 list(itertools.combinations(transaction_DB[39],2))

