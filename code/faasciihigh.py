from nlputils import *
from fa import *


###############################################################################
###	Count of characters with ascii > 127 feature annotator
###	Note: only designed to work with UDB encapulated TDT4
###############################################################################

class faasciihigh(fa):
	###   constructor
	def __init__(self):
		self.attr_name = 'asciihigh_cnt'
		self.attr_type = 'numeric'


	###   annotate feature onto each chunk of UDB bundle
	def annotate(self, bundle):
		for chunk in bundle.chunks:
			cnt = 0
			for ch in chunk[0]:
				if ord(ch) > 127: cnt += 1
			chunk[1]['asciihigh_cnt'] = cnt


