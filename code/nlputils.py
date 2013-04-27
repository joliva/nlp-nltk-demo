import sys, os, re, string

###############################################################################
###  miscellaneous helper routines
###############################################################################

### debug print routine
def debug_print(level, debug_level, str):
	if level == debug_level:
		print str
		sys.stdout.flush()


###############################################################################
###  NLP helper constants
###############################################################################

### offsets in sentence list
SENTENCE = 0
SENT_START = 1
SENT_END = 2
WORD_LIST = 3
WORD_START_LIST = 4
WORD_END_LIST = 5
WORD_POS_LIST = 6
MARKUP_LIST = 7

### various regex entities within a sentence
wrd = "[a-zA-Z'-]+"
capwrd = "[A-Z]'?[a-zA-Z'-]*'?"
num = "'?[0-9,]+"
abbr1 = "(?:Sr\.|Jr\.|Mr\.|Mrs\.|Ms\.|Dr\.|St\.)"
abbr2 = "[A-Z]\.[A-Z]\."
spc = "[ \t]+"
terma = "[\?\!]"
terma = "[\.\?\!]"
quot = "\"?"
endline = "\n?"
punca = "\,\:\;\-\@\#\$\%\^\&\*\(\)"
puncb = "\_\+\=\~\/\\\|\{\}\[\]\<\>"
punc = "["+punca+puncb+"]+"

### regex templates for start, middle and end of sentence
fstart = quot+"(?:"+capwrd+"|"+num+"|"+abbr1+"|"+abbr2+")"+quot+"(?:"+punc+")?(?:"+spc+")"
	
fmid = quot+"(?:"+wrd+"|"+num+"|"+abbr1+"|"+abbr2+"|"+punc+")"+quot+"(?:"+punc+")?(?:"+spc+")"
	
fend = "(?:"+wrd+"|"+num+"|"+abbr1+"|"+abbr2+")"+quot+"(?:"+abbr1+"|"+abbr2+"|"+terma+")"+quot+endline
	
### regex template for an entire sentence
FSENT = "(?:"+fstart+")(?:"+fmid+")+(?:"+fend+")"

### regex model for word in sentence
#FWORD = "(?:"+wrd+"|"+num+"|"+abbr1+"|"+abbr2+"|"+terma+"?)"
FWORD = "(?:"+wrd+"|"+num+"|"+abbr1+"|"+abbr2+")(?:"+terma+"?)"

TOKEN_WIDTH = 10

###############################################################################
###  NLP helper routines
###############################################################################

### returns list of sentence words and associated meta-data
def sent_details(sent):
	lst = []
	for idx1 in range(0,len(sent[WORD_LIST])):
		row=[]
		for idx2 in range(WORD_LIST, len(sent)):
			row.append(sent[idx2][idx1])

		lst.append(tuple(row))

	return lst


### extract sentences from input text and return as list of sentences
def extract_sentences(text):
	regx = re.compile(FSENT)
	
	iter = regx.finditer(text)
	sentences=[]
	
	for sentence in iter:
		sentences.append([sentence.group(),sentence.start(),sentence.end()])
	return sentences

### extract words, start and stop positions from input sentence and return
### as a list
def extract_words(sent):
	regx = re.compile(FWORD)
	
	iter = regx.finditer(sent[SENTENCE])
	wlist=[]   # WORD_LIST
	wslist=[]   # WORD_START_LIST
	welist=[]   # WORD_END_LIST
	
	for word in iter:
		### handle special case of word at end of sentence
		echar = word.group()[-1]
		if echar == '?' or echar =='!' or echar == '.':
			wlist.append(word.group()[:-1])
			wslist.append(sent[SENT_START] + word.start())
			welist.append(sent[SENT_START] + word.end()-1)

			wlist.append(echar)
			wslist.append(sent[SENT_START] + word.end())
			welist.append(sent[SENT_START] + word.end())

		else:
			wlist.append(word.group())
			wslist.append(sent[SENT_START] + word.start())
			welist.append(sent[SENT_START] + word.end())
	
	return [wlist, wslist, welist]

### determine whether file can be opened for reading
def file_readable(file_path):
	if os.access(file_path, os.R_OK):
		return True
	else:
		return False

### determine whether file can be opened for writing
def file_writable(file_path):
	try:
		outfile = open(file_path, "w")
		outfile.close()
		os.remove(file_path)
		return True
	except IOError:
		return False

### determine whether directory exists
def dir_exists(dir_path):
	if os.access(dir_path, os.F_OK):
		return True
	else:
		return False


### returns function used for character deletion/translation
def translator(frm='', to='', delete='', keep=None):
	allchars = string.maketrans('','')

	if len(to) == 1:
		to = to * len(frm)
	trans = string.maketrans(frm, to)

	if keep is not None:
		delete = allchars.translate(allchars, keep.translate(allchars, delete))

	def callable(s):
		return s.translate(trans, delete)
	return callable
	

### returns the number of times 'phrase' regex occurs in 'instring'
def phrase_cnt(instring, phrase):
	regex = phrase
	rxc = re.compile(regex)
	cnt = len(rxc.findall(instring))

	return cnt
