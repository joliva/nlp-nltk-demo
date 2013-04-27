from nlputils import *
from fa import *


###############################################################################
###	Count of regex phrase match annotator
###
###	Notes: 1. only designed to work with UDB encapulated TDT4
###        2. regex_list = list containiing regular expressions strings
###           example: ['(.*)','<word>','finis?']
### 
###############################################################################

class faphrasecnt(fa):
	###   constructor
	def __init__(self, arg_string):
		arg_list = arg_string.split(',')
		self.attr_name = arg_list[0]			# feature name
		self.attr_type = arg_list[1]			# feature type
		if len(arg_list) > 2:
			self.regex_list = arg_list[2].split('|')
		else:
			self.regex_list = []	# empty


	###   annotate feature onto each chunk of UDB bundle
	def annotate(self, bundle):
		# build translator to filter out all characters except [a-zA-Z ]
		trans = translator(keep=string.letters+' ')
		for chunk in bundle.chunks:
			# cycle over regex list and add up matches
			filt_text = trans(chunk[0])

			cnt = 0
			for regex in self.regex_list:
				cnt += phrase_cnt(filt_text, regex)

			chunk[1][self.attr_name] = cnt


