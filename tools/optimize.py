#!/usr/local/bin/python

import sys
from datetime import datetime

def optimize(path, num_words, class_list):
	debug = True
	classes = class_list
	num_words = int(num_words)

	if path[-1] != '/': path += '/'
	
	### heuristic to set optimization parameters: best_factor and min_count
	lowest = 5000	# lowest ranking phrase to compare
	middle = 20		# mid-range ranking phrase
	low_tot = 0		# total accumulated lower ranking phrases occurrences
	ratio_tot = 0	# total upper/mid accumulated for computing avg
	low_cnt = 0		# number of lower ranking phrases checked
	mid_cnt = 0		# number of mid ranking phrases checked
	
	for name in classes:
		infile = open(path+name, 'r')
		buffer = infile.readlines(500000)

		try:
			upper = int(buffer[0].split()[0])
		except:
			upper = 0

		try:
			mid = int(buffer[middle].split()[0])
			mid_cnt += 1
		except:
			mid = 0

		try:
			lower = int(buffer[lowest].split()[0])
			low_tot += lower
			low_cnt += 1
		except:
			lower = 0

		if mid > 0:
			ratio = upper/mid
			ratio_tot += ratio

	best_factor = ratio_tot/mid_cnt
	min_count = low_tot/low_cnt
	print name + ": best_factor = " + str(best_factor)
	print name + ": min_count = " + str(min_count)

	num_compared = 20000	# max number of secondaries to search
	
	dt = datetime(2007,10,22)
	
	total={}

	if debug:
		print dt.now()
	for cl in classes:
		tot = 0
		infile1 = open(path+cl,"r")
		
		if debug:
			print "counting " + cl
		for line in infile1:
			cols = line.split()
			if len(cols) == num_words+2:
				tot += int(cols[0])
		total[cl] = tot
		if debug:
			print cl, tot
		infile1.close()
	if debug:
		print dt.now()
	
	if debug:
		print dt.now()
	for pri in classes:
		if debug:
			print "finding best for: " + pri
		infile1 = open(path+pri,"r")
		ofile_strings = open(path+pri+'_best',"w")
		ptot = total[pri]
	
		dict = {}
		if debug:
			print "reading secondary classes into dictionaries"
		for sec in classes:
			if pri == sec: continue
			d = dict[sec] = {}
			cnt = 0
			infile2 = open(path+sec,"r")
	
			### read most frequent of secondary into dictionaries
			for line in infile2:
				cols = line.split()
				if len(cols) == num_words+2:
					cnt += 1
					if cnt < num_compared:
						phrase='' 
						for idx in range(1,num_words+1):
							phrase += cols[idx]
						d[phrase] = cols[0]
					else:
						break
			infile2.close()
	
		infile1.seek(0)		# reset to beginning
		cnt = 0
		for line in infile1:
			cols = line.split()
			if len(cols) == num_words+2:
				if cnt < 20:
					phrase='' 
					for idx in range(1,num_words+1):
						phrase += cols[idx]
	
					pfreq = float(cols[0])/ptot
	
					# cycle over secondary classes and test with the 
					# primary is better than all secondaries
					cond = True
					for sec in classes:
						if pri == sec: continue
						stot = total[sec]
						d = dict[sec]
	
						if phrase in d:
							sfreq = float(d[phrase])/stot
							cond = cond and (int(cols[0]) > min_count)
							cond = cond and (pfreq > best_factor * sfreq)
						else:
							sfreq = 0
							cond = cond and (int(cols[0]) > min_count)
							# make sure doesn't include class tag
							for idx in range(1,num_words+1):
								if cols[idx] == cols[num_words+1]: cond = False
	
					# if better than all secondaries, save
					if cond:
						cnt += 1
						if debug:
							print (phrase + '  ').ljust(24),
							print cols[0].ljust(8),
							print pri + ': ' + str(pfreq),
							print sec + ': ' + str(sfreq) 
						temp='' 
						for idx in range(1,num_words+1):
							temp += cols[idx] + ' '
						temp += '\n'
						ofile_strings.write(temp)
				else:
					break
	
		del dict
	
		infile1.close()
		ofile_strings.close()

		# encode list of phrases for use by feature classier 'faphrasecnt'
		ofile_strings = open(path+pri+'_best',"r")
		ofile_call = open(path+pri+'.call',"w")

		fcall = 'faphrasecnt(' + pri + str(num_words) + '_cnt' + ',numeric,'
		lines = ofile_strings.readlines()
		for line in lines:
			line = line.strip() 
			if line[-1] == '\n':
				fcall += line[:-1] + '|'  # drop line feed
			else:
				fcall += line + '|'
		fcall = fcall[:-1] + ')' # drop final |
		ofile_call.write(fcall)

		ofile_call.close()
		ofile_strings.close()
	
	if debug:
		print dt.now()

##########################################################

usage =  'usage: optimize.py path num_words class_list'
usage += '\twhere class_list like \'AA BB CC DD\''

if (len(sys.argv) == 4):
	optimize(sys.argv[1], sys.argv[2], sys.argv[3].split(' '))
else:
	print usage + '\n'
	
