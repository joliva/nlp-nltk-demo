import sys, os
from nlputils import *
from hw2utils import *

params = {}	# parameters dictionary

params['debug_level'] = 0	  # no debugging by default
params['progname'] = "runXXXX"    # temporary
params['run_mode'] = 'test'
params['dump_text'] = False
params['classifier'] = 'weka.classifiers.trees.J48'

### function usage
def usage():
	temp = "\nusage: " + params['progname'] + " model_file_path input_files_path [-M -Cweka_classifier -Rrun_mode -ddebug_level]\n"
	temp += "\t-R: running mode = 'train', 'fasttrain' or 'test'(default)\n"
	temp += "\t-C: weka classifier (default=J48)\n"
	temp += "\t-M: (dev only) dump text chunks pre-pended with class.\n"
	temp += "\t-d: (dev only) level of debug printing\n"
	print temp

### Note: no ARFF generation if running_mode = 'fasttrain'

###############################################################################
### set paths for input and output files
###############################################################################

params['model_path'] = "data/models/"  # relative location to persist models
params['arff_path'] = "data/arff/"  # relative location to access ARFF files
params['config_path'] = "data/config/"  # relative location to read configuration files

#params['weka_path'] = '\'c:\\Program Files\\Weka-3-4\\\''  # PC
params['weka_path'] = '/home/cs4705/bin/'  # CLIC

###############################################################################
### validate program inputs and file i/o
###############################################################################

from string import atoi

### parse input line
if len(sys.argv) < 4:
	usage()
	sys.exit()

### parse and handle optional command line arguments
if len(sys.argv) > 4:
	for parm in sys.argv[4:]:
		if parm[:2] == "-R":
			temp = parm[2:]
			if (temp == 'test') or (temp == 'train') or (temp == 'fasttrain'):
				params['run_mode'] = temp
			else:
				print "\nIllegal running mode - see usage.",
				usage()
				sys.exit()
		elif parm[:2] == "-d":
			try:
				params['debug_level'] = atoi(parm[2:])
			except:
				usage()
				sys.exit()
		elif parm[:2] == "-C":
				params['classifier'] = parm[2:]
		elif parm[:2] == "-M":
			params['dump_text'] = True
		else:
			usage()
			sys.exit()

### set classification type based on bash script name invoking this script
loc = sys.argv[3].find("run")
if loc != -1:
	params['progname'] = sys.argv[3][loc:]
	params['arff_file'] = params['arff_path']
	if params['progname'] == "runSourceType":
		if params['run_mode'] == 'test':
			params['arff_file'] += "sourceTypeTest.arff"
		else:
			params['arff_file'] += "sourceType.arff"
		task_type = "stype"
	elif params['progname'] == "runSourceLang":
		if params['run_mode'] == 'test':
			params['arff_file'] += "sourceLangTest.arff"
		else:
			params['arff_file'] += "sourceLang.arff"
		task_type = "slang"
	elif params['progname'] == "runSourceNO":
		if params['run_mode'] == 'test':
			params['arff_file'] += "sourceNOTest.arff"
		else:
			params['arff_file'] += "sourceNO.arff"
		task_type = "sorg"
	elif params['progname'] == "runTopicBroad":
		if params['run_mode'] == 'test':
			params['arff_file'] += "topicBroadTest.arff"
		else:
			params['arff_file'] += "topicBroad.arff"
		task_type = "btopic"
	else:
		print "Unexpected classification type. Exiting.\n"
		sys.exit()
else:
	print "Unexpected classification type passed to script. Exiting.\n"
	sys.exit()

params['task_type'] = task_type
params['model_file'] = sys.argv[1]
params['indir'] = sys.argv[2]

### verify config file exists. save feature extractor list to parameter list
temp = params['config_path'] + 'fextract' + '_' + task_type + '.config'
try:
	infile = open(temp, "r")
	lst = infile.readlines()
	params['fextractors'] = []
	for item in lst:
		item = item[:-1]   # drop linefeed
		if item != '': params['fextractors'].append(item)
	infile.close()
except IOError:
	print "Unable to read config file: " + temp
	sys.exit()

### verify input files exist and output file(s) can be opened

if params['run_mode'] == 'test':
	### test mode: verify the model file exists
	temp = params['model_file']
	if not file_readable(temp):
		print "Unable to open model file: " + temp
		sys.exit()

	temp = params['arff_file']
	if not file_writable(temp):
		print "Unable to open ARFF file for writing: " + temp
		sys.exit()

elif params['run_mode'] == 'train':
	### train mode: verify that the model file can be opened for writing
	temp = params['model_file']
	if not file_writable(temp):
		print "Unable to open model file for writing: " + temp
		sys.exit()

	temp = params['arff_file']
	if not file_writable(temp):
		print "Unable to open ARFF file for writing: " + temp
		sys.exit()

else:
	### fasttrain mode: verify that the model file can be opened for writing
	temp = params['model_file']
	if not file_writable(temp):
		print "Unable to open model file for writing: " + temp
		sys.exit()

### verify there are input files for training or testing
### side-effect: leaves names of input files in input_files[] list
temp = params['indir']
if dir_exists(temp):
	input_files = os.listdir(params['indir'])
	num_files = len(input_files)
	if num_files == 0:
		print "No input files found in: " + params['indir']
		sys.exit()
else:
	print "Unable to access input file directory: " + temp
	sys.exit()


###############################################################################
###  If optioned, dump text chunks pre-pended with classification group for
###  n-gram generation and word frequency analysis.  (DEV MODE)
###############################################################################

if params['dump_text'] == True:
	dump_text(params, input_files)
	sys.exit()


###############################################################################
###  Perform training, fast training or test mode operations
###############################################################################

if params['run_mode'] == 'test':
	run_testing(params, input_files)
else: 
	run_training(params, input_files)


###############################################################################
### cleanup
###############################################################################

