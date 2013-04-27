import os, sys, re, udb
from datetime import datetime
from nlputils import *
from udb import *
from parse import *


###############################################################################
### ARFF file generation
###############################################################################

def generate_arff(params, input_files):

	debug_level = params['debug_level']

	RX_KERNEL = '\(.*\)'  # regex for finding extractor constructor argument

	### import feature extractors and instantiate extractor objects
	if debug_level > 0:
		temp = "++ import and instantiate feature extractors"
		debug_print(1, debug_level, temp)

	anlist = []
	for annotator in params['fextractors']:
		# extract constructor argument (if any)
		rx_kernel = re.compile(RX_KERNEL, re.DOTALL)
		kernel = rx_kernel.search(annotator)
		arg = None
		if kernel != None:
			arg = kernel.group()[1:-1]   # drop parenthesis
			annotator = (annotator[:kernel.start()]).strip()  # dump kernel

		exec('from ' + annotator + ' import *')
		obj = locals().get(annotator)
		if arg == None:
			anlist.append(obj())
		else:
			anlist.append(obj(arg))

	### open ARFF file
	arff_file = open(params['arff_file'], "w")

	### produce ARFF file header

	if debug_level > 0:
		temp = "++ produce ARFF file header"
		debug_print(1, debug_level, temp)

	entry =  '% ARFF file produced for W4705 HW2 assignment\n'
	dt = datetime(2007,10,20)
	entry += '% Generated: ' + str(dt.now()) + '\n\n'
	entry += '@RELATION'.ljust(16)

	task_type = params['task_type']

	if task_type == 'slang':
		entry += 'source_language'
	elif task_type == 'stype':
		entry += 'source_type'
	elif task_type == 'sorg':
		entry += 'source_organization'
	else:
		entry += 'broad_topic'

	arff_file.write(entry + '\n\n')

	for annotator in anlist:
		entry =  '@ATTRIBUTE'.ljust(16)
		entry += annotator.get_feat_name().ljust(16)
		entry += annotator.get_feat_type()
		arff_file.write(entry + '\n')

	### save dependent attribute declaration
	entry =  '@ATTRIBUTE'.ljust(16)
	entry += 'class'.ljust(16)
	if task_type == 'slang':
		entry += '{ARB, ENG, MAN}'
	elif task_type == 'stype':
		entry += '{BN, NWIRE}'
	elif task_type == 'sorg':
		entry += '{APW, NYT, CNN, ABC, NBC, PRI, VOA, MNB, XIN, ZBN, '
		entry += 'CBS, CTS, VOM, CNR, CTV, AFP, ALH, ANN, VAR, NTV}'
	else:
		entry += '{BT_1, BT_2, BT_3, BT_4, BT_5, BT_6, BT_7, BT_8, '
		entry += 'BT_9, BT_10, BT_11, BT_12, BT_13}'

	arff_file.write(entry + '\n')

	arff_file.write('\n\n@DATA\n')

	### cycle over each input file
	if debug_level > 0:
		temp = "++ running feature extractors over each input file data"
		debug_print(1, debug_level, temp)

	num_files = len(input_files)
	file_cnt = 0
	for filename in input_files:
		if debug_level == 1:
			file_cnt += 1
			temp = "\r++ processing file: "+str(file_cnt)+' of '+str(num_files)
			print temp,
			sys.stdout.flush()

		### open file for parsing
		infile = open(params['indir'] + "/" + filename, "r")
		src_data = infile.read()

		###############################################################
		### Parse the file contents into an internal format (UDB) 
		### for processing. 
		###############################################################

		src_meta = {'sfile':filename}
		options = {}  # unused at this time

		bundle = parse_to_udb(src_data, src_meta, options)

		###############################################################
		### annotate features onto each UDB chunk
		###############################################################
		
		for annotator in anlist:
			annotator.annotate(bundle)

		###############################################################
		### insert feature vector into ARFF file
		###############################################################

		for chunk in bundle.chunks:
			cmeta = chunk[1]

			### dont't include feature vector when doing broad topic
			### classification and broad topic type wasn't pre-annotated
			if task_type == 'btopic' and cmeta[task_type] == 'NONE':
				continue

			entry = ''
			for annotator in anlist:
				fname = annotator.get_feat_name()
				ftype = annotator.get_feat_type()
				if ftype == 'string':
					entry += '\'' + cmeta[fname] + '\', '
				else:
					entry += str(cmeta[fname]) + ', '

			### save dependent attribute declaration
			entry += cmeta[task_type]
			arff_file.write(entry + '\n')

		### close file
		infile.close()

	### close ARFF file

	if debug_level == 1:
		print 
		sys.stdout.flush()

	arff_file.close()


###############################################################################
### Model training 
###############################################################################

def run_training(params, input_files):
	debug_level = params['debug_level']

	### only generate ARFF for training mode, not fast training mode
	if params['run_mode'] == 'train':
		generate_arff(params, input_files)

	if debug_level > 0:
		temp = "++ generating and saving model file"
		debug_print(1, debug_level, temp)

	### generate and save model
	### -i: more detail results, -x 10: 10-fold cross-validation
	cmd =  'java -Xmx1G -cp ' + params['weka_path'] + 'weka.jar '
	cmd += params['classifier'] + ' -t ' + params['arff_file']
	cmd += ' -x 10 -d ' + params['model_file']
	os.system(cmd)


###############################################################################
### Testing against model
###############################################################################

def run_testing(params, input_files):
	debug_level = params['debug_level']

	generate_arff(params, input_files)

	if debug_level > 0:
		temp = "++ testing data against model file"
		debug_print(1, debug_level, temp)

	### run test data against model
	### -i: more detail results
	cmd =  'java -Xmx1G -cp ' + params['weka_path'] + 'weka.jar '
	cmd += params['classifier'] + ' -T ' + params['arff_file']
	cmd += ' -l ' + params['model_file']
	os.system(cmd)


###############################################################################
### Dump text chunks pre-pended with classification group for subsequent
### n-gram generation and word frequency analysis
###############################################################################

def dump_text(params, input_files):
	### cycle over each input file
	for filename in input_files:
		### open file for parsing
		infile = open(params['indir'] + "/" + filename, "r")
		src_data = infile.read()

		###############################################################
		### Parse the file contents into an internal format (UDB) 
		### for processing. 
		###############################################################

		src_meta = {'sfile':filename}
		options = {}  # unused at this time

		bundle = parse_to_udb(src_data, src_meta, options)

		task_type = params['task_type']

		for chunk in bundle.chunks:
			cmeta = chunk[1]

			ostr = cmeta[task_type] + '\t'
			ostr += chunk[0].replace('\n',' ')
			print ostr

		### close file
		infile.close()
