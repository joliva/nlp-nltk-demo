****************************************************************************
*  Author:	John Oliva
*  Purpose:	Document Classification
****************************************************************************

Notes
-----

1. The 'analysis' files that are generated during production of the feature
   extractors are not included here - together they are quite large. They 
   may be generated using the supplied scripts.
2. The program has been tested to run on Windows under Cygwin, and on
   Fedora Linux.
4. All of the models are based on the J48 classifier. The classifier was 
   run with the default parameters.

Files
-----

|- readme.txt (this file)
|
|- runSourceLang - simple bash script which initiates ARFF file generation,
|                  model generation, cross-validation and classification based
|                  on Source Language.
|
|- runSourceNO -   same as above for Source News Organization
|- runSourceType - same as above for Source Type (broadcast or newswire)
|- runTopicBroad - same as above for Broad Topic
|
|- /analysis - set of intermediary files generated during analysis of the
|              training text while automatically generating content based
|              feature extractors. (not included with submission)
|
|- /doc - contains a file describing the application architecture
|
|- /code - Python code implementing homework solution
|    |
|    |- main.py - main code which is highly tuned to this homework assignment
|    |- nlputils.py - utility code which is largely re-usable
|    |- hw2utils.py - utility code which specific to this assignment
|    |- udb.py - UDB class for encapsulating uniform data bundles.
|    |- parse.py - code which parses documents into UDB format
|    |- fa.py - base class feature extractor
|    |- faXXXX.py - ensemble of specific feature extractors based on fa.py.
|
|- /data/arff - Weka ARFF files
|    |
|    |- sourceLang.arff - Weka classifier input based on Source Language
|    |- sourceNO.arff - Weka classifier input based on Source News Org.
|    |- sourceType.arff - Weka classifier input based on Source Type
|    |- topicBroad.arff - Weka classifier input based on Broad Topic
|
|- /data/config - Feature extractor configuration files
|    |
|    |- fextract_btopic.config - config for Broad Topic feature extractor
|    |- fextract_slang.config - config for Source Language feature extractor
|    |- fextract_sorg.config - config for Source Org. feature extractor
|    |- fextract_stype.config - config for Source Type feature extractor
|
|- /data/models - Weka classification models 
|    |
|    |- XXXX.J48.model - classified with J48 classifer
|    |- XXXX.NaiveBayes.model - classified with Naive Bayes classifer
|    |- XXXX.DecisionTable.model - classified with Decision Table classifer
|
|- /data/results - Classification & cross-validation results
|    |
|    |- btopic.XXXX.train - classification results based on Broad Topic
|    |- slang.XXXX.train - classification results based on Source Language
|    |- sorg.XXXX.train - classification results based on Source Org.
|    |- stype.XXXX.train - classification results based on Source Type
|
|- /data/tdt4 - source TDT4 documents (not included)
|
|- /tools - scripts used in producing feature extractors and running 
     |      classification
     |
     |- analyze_XXXX - scripts which generate intermediate analysis files
     |                 for each classification task which includes n-gram
     |                 phrase frequencies (word unigrams, bigrams and trigrams)
     |
     |- optimize.py - script which attempts to extract the most useful word 
	 |                phrases identified above for use in classification. 
	 |
     |- optimize_XXXX - scripts which call optimize.py for each classification
     |                  task
	 |
     |- extractors{1,2} - scripts which run analyze_XXXX and optimize_XXXX
	 |
     |- training{1,2} - scripts which execute runXXXX in root directory
	 |
     |- wfreq  - unigram word frequency analysis script
     |- w2freq - bigram word frequency analysis script
     |- w3freq - trigram word frequency analysis script


Program Execution
-----------------

The program requires that Python 2.4+ be installed. There
is no explicit compilation required as Python is a scripting language, however
the Python interpreter will JIT compile the source code into a binary format
for faster execution on successive runs. The program makes use of Weka (a
machine learning tool), and was specifically run against Weka 3.4.11.

usage: runSourceLang model_file_path input_files_path [optional arguments]
       runSourceNO   model_file_path input_files_path [optional arguments]
       runSourceType model_file_path input_files_path [optional arguments]
       runTopicBroad model_file_path input_files_path [optional arguments]

       optional arguments: -M -Cweka_classifier -Rrun_mode -ddebug_level

       -R: running mode = 'train', 'fasttrain' or 'test'(default)
       -C: weka classifier (default=J48) 
       -M: (analysis) dump text chunks pre-pended with classification group 
       -d: level of debug printing

debug_level   purpose
-----------   -------
  1           prints processing state status information during execution

Notes:

1. ARFF file and model generation
   - 'model_file_path' is the full path (including filename) where the model 
     will be stored
   - 'input_files_path' is the full path to a directory where the input 
     training and/or test files will be read

2. Classifier testing
   - 'model_file_path' is the full path (including filename) where the pre-
     generated model will be read from
   - 'input_files_path' is the full path to a directory where the input test 
     files will be read


Feature Extractors
------------------

Initial visual inspection of the input files showed that some of the text
blocks had all lower case characters while others had mixed lower/upper case.
This was deemed to be a potentially useful feature for descrimination. Also,
it was observed that some text blocks had extended ASCII characters (values
above 127) and they seemed correlated with text that had been translated. This
was also chosen as a useful feature. The third feature chosen was the length
of the text block.  There was no visually obvious reason to choose this feature
but it was very simple to extract, and appeared to be orthogonal with the 
other feature extractors, so it was hoped that the model training would yield
some useful correlation with the desired classification types.

Some initial experiments with these feature extractors yielded poor to fair
results.  The specific results weren't recorded because it was obvious that
more work needed to be done in extracting useful features.

Upon further consideration of the document classification task, it was noted 
that the features identified thus far were generally structural features of
the text.  Another aspect of feature analysis that could be mined related to
the syntactic and semantic content.  It was hypothesized that the specific 
words that occurred in the text as well as their local context might provide
features that would drive much more successful classification. There was a
strong intuitive sense that text blocks relating to some broad topic would 
tend to use certain words frequently, that source news organizations might
identify themselves ('this is CNN'), that source types (specifically broadcast
news) might be discerned by topic transition phrases, and that text that had
originally been written in English, Mandarin, or Arabic would be strongly 
correlated with certain parts of the world (cities, states, countries), local 
politics, cultural interests, etc. that would be reflected in the frequency of
specific word occurrence (specifically nouns).

It was clear that the task of extracting word phrases and measuring their
frequency relative to the target classification task was one that needed to
be automated. In order to support syntactic and local context based correlation
analysis relative to the classification tasks, it was decided to extract
unigrams, bigrams, trigrams and their frequencies of occurrence. Once this 
information was available a heuristic approach would be developed to select 
some subset of the phrases for matching in each classification task. Once the
phrases were identified, they would be saved as configuration data to be used
by the set of content based feature extractors.


Processing Architecture
-----------------------

The processing architecture and detailed operation will be explained by 
referring to compute_process.pdf in the 'doc' directory.

There are three phases of operation.  The first phase is the automated
production of feature extractors.  The second phase is extraction of feature
vectors from the input files, production of ARFF files, model generation and 
cross-validation testing. The third phase is classification testing from test
input given a pre-generated classifier model.


Steps in Phase 1:

(left-side blue dashed line analyze_XXXX, optimize_XXXX)

- read training/dev-test files
- produce UDB data bundles representing file content
- extract <TEXT> blocks from UDB data bundles
- for each classification task (source language, source type, source news 
  organization, broad topic), annotate them with the type (i.e. for source type
  they are NWIRE or BN).
- generate unigram, bigram and trigrams for the set of text blocks 
  corresponding to each permuation of classification task and type 
  (i.e. Source Language : Mandarin).
- annotate these classification task/type groups with the frequency for each 
  n-gram.
- use heuristic approach to select a subset of the phrases which is correlated
  (representative) for each group.
- save each classification task/type phrase set to a configuration for use
  during feature extraction


Steps in Phase 2:

(top right-side blue dashed line runXXX training)

- for specified classification task
  + produce ARFF file header
  + read training/dev-test files
  + for each input file
    - produce UDB data bundle representing file content
	- for each <TEXT> element chunk in the UDB data bundle
      + run all classification task appropriate feature extractors and 
	    annotate the chunk with the extracted feature measures
	- for each chunk in the UDB data bundle
	  + extract and save the feature vector to the ARFF file
  + close ARFF file
  + run Weka with the selected classifier using the ARFF file as input, 
    10-fold cross-validation
  + save resulting model to specified model file
  + save output cross-validation and classification results to files


Steps in Phase 3:

(top right-side blue dashed line runXXX testing)

- for specified classification task
  + produce ARFF file header
  + read test files
  + for each input file
    - produce UDB data bundle representing file content
	- for each <TEXT> element chunk in the UDB data bundle
      + run all classification task appropriate feature extractors and 
	    annotate the chunk with the extracted feature measures
	- for each chunk in the UDB data bundle
	  + extract and save the feature vector to the ARFF file
  + close ARFF file
  + run Weka with the selected classifier and pre-generated model file using
    the ARFF file as input 
  + save output classification results to file


Detailed Operation
==================

Uniform Data Bundle (UDB)
-------------------------
One personal desire for this project was to develop re-usable functionality
that would live on.  As such, there was a desire to decouple (as much
as possible) the input file format from the feature extraction. This was to
be achieved by specifying a uniform data structure into which the input data
and associated meta-data could be packaged. Having specified this packaging
format, decoupling would occur by building a parser specific to the input
document format which could generate UDBs, and building feature extractors
which read UDBs and would extract features from the embedded data.

The details of the UDB format are contained in the code/udb.py file. The 
document format was dubbed TDT4 and a parser for that format file into
UDB is found in the code/parser.py file.  It is a fairly straight forward task
to write parsers for other input file formats. A UDB data bundle includes a 
format field which indicates the type of data that can be extracted from the 
bundle.  Feature extractors must support the UDB content format in order to
process the data.


Document Parsing
----------------
The parsing starts by instantiating a UDB data bundle. The file being parsed 
is scanned using a regular expression to find all elements between 
<DOC>...</DOC> tags.  For each document element, a chunk dictionary is added
to the UDB to contain all data related to that document. Each of these document
elements is further scanned using regular expressions to extract elements 
representing document meta-data (source organization, source type, source news
organization, broad topic) and this is added to the chunk as meta-data. Finally,
the <TEXT>...</TEXT> element is extracted as saved in the UDB as the chunk text.

To facilitate the automatic generation of phrase feature extractors, the 
program can dump the chunk text out to standard output to be subsequently 
processed by the analysis and optimization processing tasks.


N-gram Analysis
-----------------
This process operates on each chunk of text, applies a regular expression 
filter to suppress punctuation, and then extracts individual words, pairs of 
consecutive words and trios of consecutive words. The decision to suppress
punctuation to some degree impacts contextual analysis. For example, after 
filtering to remove punctuation, hyphenated words are treated as multiple 
words. This was a concession to simplify the task of separating words from
prefixed or suffixed punctuation. Each n-gram extracted is annotated with the
classification type (i.e. NWIRE, BN, etc.) contained in the UDB meta-data and
corresponding to the classification task the extractors are being built for.
These are written out to intermediate files, one each for unigram, bigram and
trigrams for subsequent processing.

For each classification type and n-gram type, the intermediate file gets sorted
such that each unique phrase is represented once and is also annotated with
the number of occurrences.

At he end of N-gram analysis (for a particular classification task), there are
three files - unigram phrases, bigram phrases and trigram phrases. The phrases
are unique in each file and are annotated and sorted into decreasing order by
number of occurrences. These files are based on the text elements contained in
all of the input files.


Optimization
------------
The question is, how to select a subset of phrases for each classification
type which are highly correlated with that type and not well correlated with
the other types.  The idea being that those phrases are good discriminators
(or features) for that classification type. For example, for the source type
classification task, what phrases were indicative of newswire and not so much
of broadcast news, and vice versa? 

A heuristic algorithm was developed to extract a suitable set of 'best' phrases
for each classification type based on quantities dubbed 'best_factor' and 
'min_count'.  The best_factor was intended to set a minimum ratio of the 
n-gram frequency for the target classification type to the rest of the 
classification types in that task. The min_count was intended to set a minimum
threshold of occurence for specific n-gram to be eligible for inclusion in the
set of best phrases.

This concept was tested by starting with a SWAG estimate for best_factor and 
min_count for a particular case and iterating on the values until the
algorithm was producing enough phrases for each classification type to use in
building the feature extractor. Inspection of the phrases chosen seemed to
be reasonable - they did generally fit the category well. The main problem with
this approach was that it was time consuming to find suitable optimization
parameters (best_factor, min_count), and there were 12 sets that needed to be
determined (classification tasks (4) x types of n-grams (3)). The values 
chosen were also potentially training data dependent. It was determined that
an automated approach was needed to select the optimization parameters. The 
details of this automated approach will need to gleaned from looking at the
code in tools/optimize.py.


Feature Extraction
------------------
One architectural goal for the program was to make it simple to add new feature
detectors, making it very easy to experiment with ideas for effective features.
Rather than embedded the feature extractors directly into the main program, 
the idea was to produce distinct feature extractor modules that were loadable 
at run-time based on configuration data.  The configuration data supplies a 
list of feature extractors and any arguments (if required). 

One constraint in the implementation is that the feature extractor name listed 
in the configuration data file must match the feature extractor module (i.e. 
the text length feature extractor is named 'falen' and is implemented in 
code/falen.py).  The _cool_ part is that the program reads the list of feature
extractors from the configuration file, imports the modules based on the 
feature extractor name and then instantiates each of the feature extractor 
objects. So to add a new feature extractor, all that is needed is to build a 
feature extractor with an appropriate I/O interface, make sure the filename 
matches the feature extractor name, and add it to the configuration data file.

There is a feature extractor base class 'fa' which is sub-classed for each
specific implemented feature extractor. Each feature extractor has feature
name and feature type attribute.  These are used for when constructing the
ARFF file (described next). The feature name is used as the attribute name in
the ARFF file and the feature type is used as the attribute type.  As described
previously there is a text length FX named 'falen', a FX for counting the 
number of capital letters in the text block 'facaps', an FX for counting the 
number of high ascii characters in the text block 'faasciihigh', and finally a 
feature extractor which searches for phrases in the text block and returns the
number of matches which is named 'faphrasecnt'.  This last feature detector is
given a regular expression as an argument which is meant to describe matching
phrases. It is this feature detector that is used to detect the classification
type phrase sets.

As mentioned in the description of UDBs, feature extractors have an I/O
interface prefaced on receiving UDBs and annotating the extracted features
onto them.  The feature extractors must support the format as indicated in the
UDB data bundle. This is of course the case for this implementation.

There are separate feature extraction configuration files for each of the 
classification tasks and they are located in the data/config directory.


Generating ARFF Files
---------------------
This is a fairly straight forward task. The ARFF file name is based on the
classification task and is stored in the data/arff directory. First, some 
boiler plate header information is written to the ARFF file. Next, the code
iterates over the instantiated feature extractors, reads their feature name
and feature type and formats that into ARFF compatible attribute declarations.
Next, the code processes each feature annotated UDB data bundle in succession, 
extracts the vector of features and formats them into an ARFF compatible data
vector. Once all UDB data bundles have been processed, the ARFF file is closed.


Weka Classification
-------------------
Weka is the machine learning and classification engine used for performing the
document classification. Weka is called from the Python main program by 
issuing an os.system() call to execute the Weka java executable with the
appropriate arguments set. The main program defaults to using the J48
classifier, but this can be overridden by using a suitable command line option.

When the main program is run in 'training mode', files in the input file 
directory are processed through the feature extraction process to generate an
ARFF file.  The generated ARFF file, and the specified (or default) classifier
is given to Weka as arguments, along with an argument to perform 10-fold
cross validation.  Weka is also given an argument to save the generated model
file into the command line specified location. After Weka generates the model, 
it outputs results from classification of the training data and from a 10-fold
cross validation analysis.  This is simply dumped to standard output and must
be redirected to a file if it is to be saved.

When the main program is run in 'fast training mode', it is assumed that the
ARFF file has already been generated previously.  This is useful for testing
the performance with a variety of classifiers and a static set of training
data. The rest of the process is the same as for 'training mode'.


Selection of Classifiers
------------------------
It was instructed to try at least 3 different classifier algorithms. Initial
experiments were tried using the Weka Explorer GUI to measure the performance
in both classification accuracy and execution time for about 12 different 
classifiers on the source language ARFF file.  There was a significant range
in terms of both run-time performance and classification accuracy.  Note that
this was a rather cursory process intended to settle in on a few classifiers
for full testing.

Obviously it was important to achieve high classification accuracy, but it was
also important that classification time be performant.  In the long run, it is
probably less important how long it takes to train a model as long as the 
classification performance and classification time once trained is good. 
Another personal preference was to choose classifiers using different basic
approaches to better appreciate the limitations and benefits of these
technologies.

It was observed during some of these initial experiments that training and
10-fold cross validation testing took extremely long.  In several of these
cases Weka ran out of memory even though 1GB had been reserved for the JVM.
Some of this is no doubtedly due to the nature of the classifier algorithm, but
I believe that the reasonably high dimensionality of the feature vectors used
by this implementation were pushing results in this direction.  The source 
type and source language feature vectors were reasonably short while those for
the source news organization and broad topic were fairly large. It was observed
that the computation time was increasing much faster than linearly with the
increase in feature vector dimension.

In the end, the J48, Naive Bayes and Decision Table classifiers were selected.
They are based on different basic approaches, trained the model and performed
10-fold cross-validation in reasonable time, and in the case of J48 and 
Decision Table produced respectable classification accuracy results.


Discussion of Results
=====================

.........................................................................
. Task        Classifier   Correctly Recognized    Correctly Recognized .
.                               Training %         Cross-validation %   .
.........................................................................
.                                                                       .
. SORG        J48                83.08                     67.91        .
.             Decision Table     68.70                     61.53        .
.             Naive Bayes        51.15                     51.14        .
.                                                                       .
. STYPE       J48                88.99                     87.34        .
.             Decision Table     87.54                     85.45        .
.             Naive Bayes        58.21                     58.26        .
.                                                                       .
. SLANG       J48                94.35                     92.95        .
.             Decision Table     90.85                     90.20        .
.             Naive Bayes        86.79                     86.77        .
.                                                                       .
. BTOPIC      J48                67.89                     34.12        .
.             Decision Table     40.00                     36.55        .
.             Naive Bayes        33.76                     32.75        .
.                                                                       .
.........................................................................

     
The remainder of the classification and 10-fold cross validation results are
available in the data/results directory in appropriately named files.

Of the classifiers tested, the J48 algorithm clearly led the pack by 
consistently providing the best classification accuracy, and very good model
training and classification performance. Because of this, the J48 classifier 
was used for training the models included with this submission.

The default options were used for each of the classifiers. It is clearly 
easier to use models with a minimal number of parameters although it is 
reasonable to expect that run-time and classification performance, as well as
memory utilization can probably be tuned much better with models have more 
adjustment parameters.  The difficulty I originally experienced in tuning the 
feature extraction optimization parameters points to the potential difficulty
in setting the classifier parameters well.

The Bayes family of classifiers typically ran the fastest while both training
the model and running cross-validation, while also turning in some of poorest
classification accuracy.  The J48 clearly stood out for good performance in 
both recognition accuracy and runtime execution.

Some experiments using the Weka attribute selection functionality indicated
that significant pruning of the feature vector parameters yielded results 
almost as good as with the full set of features parameters.  This is probably
expected due to the significant correlation between the unigram, bigram and
trigram features.  It may have been prudent to have a single feature based 
on them in order to reduce the dimensionality of the feature vector and 
improve the overall training and cross-validation runtime performance. As a 
general rule it is probably best to strive for orthogonal features. Despite 
this, the addition of the content based features did significantly improve the
overall recognition accuracy relative to the initial experiments with only
the structural features.

It is interesting to note that the Naive Bayes has cross-validation results
essentially equal to the training set accuracy. This suggests that the training
set classification performance is a very good predictor of performance on 
test data other than the training data.

It was not surprising that the source language classification task performed
so well.  A couple of the structural features (capital letters and high ascii)
where correlated with the various languages and the nouns occuring with high
frequency were often well correlated with topics closely associated with the
culture or audience being served. It was somewhat surprising that the 
classification of source organization was as good as was achieved.  This was
probably due to self identification and references to anchors, but with 20
separate organizations, accuracy in the 70-80% range strikes as quite good. 
