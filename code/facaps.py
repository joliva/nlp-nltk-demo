from nlputils import *
from fa import *


###############################################################################
###	Count of capital letters feature annotator
###	Note: only designed to work with UDB encapulated TDT4
###############################################################################

class facaps(fa):
	###   constructor
	def __init__(self):
		self.attr_name = 'caps_cnt'
		self.attr_type = 'numeric'


	###   annotate feature onto each chunk of UDB bundle
	def annotate(self, bundle):
		for chunk in bundle.chunks:
			cnt = 0
			for ch in chunk[0]:
				if ord(ch) > 64 and ord(ch) < 91: cnt += 1
			chunk[1]['caps_cnt'] = cnt


