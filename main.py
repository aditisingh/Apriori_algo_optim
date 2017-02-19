#!/usr/bin/env python

import itertools
import string
import numpy as np
import sys
import time
import cProfile, pstats, StringIO
import pdb

def get_support_vals(dict2, x, node, sz): #not working for >=2 number of itemsets
	support_vals=np.zeros((1,node))	
	p1=time.clock()
	for transaction in x: #for every transaction
		comb=list(itertools.combinations(transaction,sz))
		for curr in comb:
			key='/'.join(str(x) for x in (curr))
			#constructed key
			if(dict2.get(key)):	#add it
				node_val=dict2[str(key)]
				support_vals[0][node_val]=support_vals[0][node_val]+1
	print('Part1 time: ' + str(time.clock() - p1)+ ' seconds')
	p2=time.clock()
	for key in dict2:
		if(key.count('/')==sz-1):
			idx=dict2[key] 
			dict2[key]=support_vals[0][idx]
			# print(t[key])
	print('Part2 time: ' + str(time.clock() - p2)+ ' seconds')
	return dict2;

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

pr = cProfile.Profile()
pr.enable()

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

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()


print ('Argument reading time: ' + str(time.clock() - start)+ ' seconds')
pt_1= time.clock()

pr = cProfile.Profile()
pr.enable()

sz=1
print('Size: '+str(sz))
dict2={}
count=0

for i in word_index:
	dict2[str(i)]=count
	count=count+1

pdb.set_trace()

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()

print('Candidate generation done in '+ str(time.clock() - pt_1)+ ' seconds')
f_o=open(out,'r+')
pt_2= time.clock()

pr = cProfile.Profile()
pr.enable()

# cProfile.run(get_support_vals(get_support_vals(dict,transaction_DB,count,sz))
dict2=get_support_vals(dict2,transaction_DB,count+1,sz) 
pdb.set_trace()

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()

print('Support values generation done in '+ str(time.clock() - pt_2)+ ' seconds')
pt_3=time.clock()
# cProfile.run(dict,minsup_count,sz)

pr = cProfile.Profile()
pr.enable()

#pruning
dict1={}
for key in dict2:
		if dict2[key]>=minsup_count:
			dict1[key]=dict2[key]

dict2=dict1
pdb.set_trace()

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()

print('Pruning done in '+ str(time.clock() - pt_3)+ ' seconds')

pt_4=time.clock()
pr = cProfile.Profile()
pr.enable()

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
	print('Writing done in '+ str(time.clock() - pt_4)+ ' seconds')
print('\n')

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()

for sz in range(2, 1+len(max(transaction_DB,key=len))):
	print('Size: '+str(sz))
	pt_5=time.clock()
	pr = cProfile.Profile()
	pr.enable()
	add1=0
	l=list(dict2)
	l1=[ll for ll in l if ll.count('/')==0]
	l2=[ll for ll in l if ll.count('/')==sz-2]
	if(len(l2)==0):
		break
	# l=l1+l2
	candidates=list(itertools.product(l1,l2))
	pdb.set_trace()
	for c in candidates:
		element='/'.join(c)
		ll=element.split('/')
		ll=list(set(ll))
		ll.sort(key=int)
		if(element.count('/')==sz-1 and len(ll)==sz):
			element='/'.join(ll)
			result = list(( ll.count(i)) for i in ll)
			if(sum(result)-len(result)==0):
				dict2[element]=count+1
				add1=add1+1
				count=count+1
	# print(t)
	pdb.set_trace()
	#No new candidates generated
	if(add1==0):
		break
	# print('\n')
	pr.disable()
	s = StringIO.StringIO()
	sortby = 'cumulative'
	ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
	ps.print_stats()
	print s.getvalue()

	print('Candidate generation done '+ str(time.clock() - pt_5)+ ' seconds')
	pt_2= time.clock()

	pr = cProfile.Profile()
	pr.enable()
	dict2=get_support_vals(dict2,transaction_DB,count+1,sz) # prune outside
	pdb.set_trace()

	pr.disable()
	s = StringIO.StringIO()
	sortby = 'cumulative'
	ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
	ps.print_stats()
	print s.getvalue()

	print('Support values generation done in '+ str(time.clock() - pt_2)+ ' seconds')
	# print(t)
	pt_3=time.clock()

	pr = cProfile.Profile()
	pr.enable()
	# cProfile.run(d,minsup_count,sz)
	#pruning
	pdb.set_trace()
	dict1={}
	for key in dict2:
			if dict2[key]>=minsup_count:
				dict1[key]=dict2[key]
	dict2=dict1
	pdb.set_trace()
	pr.disable()
	s = StringIO.StringIO()
	sortby = 'cumulative'
	ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
	ps.print_stats()
	print s.getvalue()

	print('Pruning done in '+ str(time.clock() - pt_3)+ ' seconds')
	# print(t)
	pt_4=time.clock()
	pr = cProfile.Profile()
	pr.enable()

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
		print('Writing done in '+ str(time.clock() - pt_4)+ ' seconds')

	pr.disable()
	s = StringIO.StringIO()
	sortby = 'cumulative'
	ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
	ps.print_stats()
	print s.getvalue()

	print('\n')
	# j=0
	
f_o.close()
print(dict)

print ('Total execution time: ' + str(time.clock() - start)+ ' seconds')