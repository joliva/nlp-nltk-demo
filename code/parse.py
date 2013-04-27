import re
from nlputils import *
from udb import *


###############################################################################
###   TDT4 internal format:
###
###   format = 'TDT4'
###   bmeta = { sfile, ... }
###   chunks = []
###      chunk = [ text, cmeta={ stype,slang,sorg,date,btopic,ntopic, ... } ]
###
###   Notes:
###      1. text: text contained in the <TEXT>..</TEXT> element
###      2. cmeta{}: dictionary for storing chunk meta-data
###      3. bmeta{}: dictionary for storing bundle meta-data
###
###############################################################################

### regex templates to extract fields from TDT4 source data
RX_DOC = "<DOC>(.*?)</DOC>"
RX_STYPE = "<SOURCE_TYPE>(.*?)</SOURCE_TYPE>"
RX_SLANG = "<SOURCE_LANG>(.*?)</SOURCE_LANG>"
RX_SORG = "<SOURCE_ORG>(.*?)</SOURCE_ORG>"
RX_DDATE = "<DOC_DATE>(.*?)</DOC_DATE>"
RX_BTOPIC = "<BROAD_TOPIC>(.*?)</BROAD_TOPIC>"
RX_NTOPIC = "<NARROW_TOPIC>(.*?)</NARROW_TOPIC>"
RX_TEXT = "<TEXT>(.*?)</TEXT>"

###############################################################################
### Parse TDT4 source content and return as a UDB encapsulated TDT4 object
###############################################################################

def parse_to_udb (src_data, src_mdata, options):

	# options are unused at this time

	bundle = udb()
	bundle.format = 'TDT4'	# TDT4 internal format
	bundle.bmeta = src_mdata

	### extract chunks and meta data and insert into UDB bundle

	### interate to extract DOC elements
	rx_doc = re.compile(RX_DOC,re.DOTALL)
	iter = rx_doc.finditer(src_data)
	for match in iter:
		doc = match.group(1)
		chunk=[]
		cmeta = {}        # cmeta dictionary

		### find SOURCE_TYPE element
		rx_stype = re.compile(RX_STYPE, re.DOTALL)
		stype = rx_stype.search(doc)
		if stype != None:
			cmeta['stype'] = stype.group(1)
		else:
			cmeta['stype'] = None
			print "Warning: SOURCE_TYPE missing in DOC"

		### find SOURCE_LANG element
		rx_slang = re.compile(RX_SLANG, re.DOTALL)
		slang = rx_slang.search(doc)
		if slang != None:
			cmeta['slang'] = slang.group(1)
		else:
			cmeta['slang'] = None
			print "Warning: SOURCE_LANG missing in DOC"

		### find SOURCE_ORG element
		rx_sorg = re.compile(RX_SORG, re.DOTALL)
		sorg = rx_sorg.search(doc)
		if sorg != None:
			cmeta['sorg'] = sorg.group(1)
		else:
			cmeta['sorg'] = None
			print "Warning: SOURCE_ORG missing in DOC"

		### find DOC_DATE element
		rx_ddate = re.compile(RX_DDATE, re.DOTALL)
		ddate = rx_ddate.search(doc)
		if ddate != None:
			cmeta['ddate'] = ddate.group(1)
		else:
			cmeta['ddate'] = None
			print "Warning: DOC_DATE missing in DOC"

		### find BROAD_TOPIC element
		rx_btopic = re.compile(RX_BTOPIC, re.DOTALL)
		btopic = rx_btopic.search(doc)
		if btopic != None:
			cmeta['btopic'] = btopic.group(1)
		else:
			cmeta['btopic'] = None
			print "Warning: BROAD_TOPIC missing in DOC"

		### find NARROW_TOPIC element
		rx_ntopic = re.compile(RX_NTOPIC, re.DOTALL)
		ntopic = rx_ntopic.search(doc)
		if ntopic != None:
			cmeta['ntopic'] = ntopic.group(1)
		else:
			cmeta['ntopic'] = None
			print "Warning: NARROW_TOPIC missing in DOC"


		### find TEXT element
		rx_text = re.compile(RX_TEXT, re.DOTALL)
		text = rx_text.search(doc)
		if text != None:
			chunk_text = text.group(1)
		else:
			chunk_text = None
			print "Warning: TEXT missing in DOC"

		chunk.append(chunk_text)
		chunk.append(cmeta)

		bundle.chunks.append(chunk)

	return bundle

