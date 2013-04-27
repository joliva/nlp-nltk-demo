from nlputils import *


###############################################################################
###	Uniform Datafile Bundle (UDB) format:
###
###	format			// format of udb bundled data
###	bmeta			// bundle metadata
###	chunks[]
###	   chunk		// group data chunk
###
###	Notes:
###	1. The entire block of data encapsulated is the data record. The
###	   format of the udb bundled data record is indicated by the format 
###	   type, and in general may include multiple chunks of data.
###############################################################################


class udb:
	###   constructor
	def __init__(self):
		self.format = None
		self.bmeta = None
		self.chunks = []


	###   set format of bundled data
	def set_format(self, format):
		self.format = format
	

	###   get format of bundled data
	def get_format(self):
		return self.format
	

	###   set meta data for bundled data
	def set_meta(self, meta):
		self.bmeta = meta
	

	###   get meta data for bundled data
	def get_meta(self):
		return self.bmeta
	

	###   add chunk to UDB bundle
	def add_chunk(self, data):
		self.chunks.append(data)
	

	###   get list of chunks
	def get_chunks(self):
		return self.chunks
	

	###   get number of chunks
	def num_chunks(self):
		return len(self.chunks)
	

	###   return trace of UDB data
	def dump(self):
		print "UDB:"
		print "\tformat=" + self.format
		print "\tmeta=",
		print self.bmeta
		print "\tchunks=",
		print self.chunks
		
	
