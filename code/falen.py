from nlputils import *
from fa import *


###############################################################################
###	Text length feature annotator
###	Note: only designed to work with UDB encapulated TDT4
###############################################################################

class falen(fa):
	###   constructor
	def __init__(self):
		self.attr_name = 'text_length'
		self.attr_type = 'numeric'


	###   annotate feature onto each chunk of UDB bundle
	def annotate(self, bundle):
		for chunk in bundle.chunks:
			chunk[1]['text_length'] = len(chunk[0])


