from nlputils import *


###############################################################################
###	Feature Annotator Base Class
###############################################################################

class fa:
	###   constructor
	def __init__(self):
		self.attr_name = None
		self.attr_type = None


	###   get feature attribute name
	def get_feat_name(self):
		return self.attr_name
	

	###   get feature type
	def get_feat_type(self):
		return self.attr_type
	

	###   annotate feature onto each chunk of UDB bundle
	def annotate(self, bundle):
		raise Exception, "Illegal to call fa.annotate()"

