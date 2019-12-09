#!/usr/bin/python3.7

import pandas as pd
import numpy as np
import os, sys

# Read in files.
critical_0to1000 = pd.read_csv("Critical.0-1000.txt", skipinitialspace=True, names=['seqnum', 'mutant_position', 'original_class', 'mutant_class', 'original_score', 'mutant_score', 'delta_score'], header=0, delim_whitespace=True)

critical_1001to2000 = pd.read_csv("Critical.1001-2000.txt", skipinitialspace=True, names=['seqnum', 'mutant_position', 'original_class', 'mutant_class', 'original_score', 'mutant_score', 'delta_score'], header=0, delim_whitespace=True)

min200_pcRNA_fasta_IDs = pd.read_csv("min200.pcRNA.nonewlines.fasta.fixed.IDS.csv", skipinitialspace=True, names=['ENST_ID'], header=None, nrows=2000, delim_whitespace=True)

gff3_basicannotations_simple = pd.read_csv("annotation_summary.tsv", skipinitialspace=True, header=0, delim_whitespace=True)

critical_0to2000 = pd.concat([critical_0to1000, critical_1001to2000], ignore_index=True)
critical_0to2000

# This dictionary maps line numbers in pcRNA fasta file to ENST ID values in the same fasta file.
# Matching on these key,value pairs will let us map Jason's seqnum values in Critical positions
# files to the fafsa ENST IDs.
seqnum_ENST_dict = min200_pcRNA_fasta_IDs.set_index(min200_pcRNA_fasta_IDs.index).T.to_dict('list')

# Pull out lines in Critical positions file for cases in which mutation causes a prediction-flip
predictionflip = critical_0to2000['original_class'] != critical_0to2000['mutant_class']
predflips = critical_0to2000[predictionflip]
predflips.to_csv("critical_0to2000_pcRNA_predflips.csv", index=None, header=True)

# For a given predflip sequence, find feature location ranges critical positions lie within, in gff3 file
# First match tr_id in gff3_basicannotations_simple file with ENST_ID in predflips
# Then see if mutant_position in predflips is >= transcriptomic_start in gff3 AND mutant position
# in predflips is  <= transcriptomic_end in gff3
# Last, concatenate predflip line and all cols of gff3 for lines that pass these 3 conditions.


# No, wait. First join on 'Name', THEN apply value range constraints (conditionals) on joined data frame.


# Map seqnum to ENST_ID in predflips file to make a new 'ENST_ID' col in predflips to compare to gff3 tr_id
predflips['ENST_ID'] = predflips['seqnum'].map(seqnum_ENST_dict)

# Get rid of "dot num" on the end of the tr_id col values in gff3 file so we can do exact pattern matching
# between predflips and gff3 files
gff3_basicannotations_simple['tr_id'] = gff3_basicannotations_simple['tr_id'].str.split(".").str[0]

# Create a common column 'Name' to make joining gff3 and predflips easier:
predflips['Name'] = predflips['ENST_ID'].str[0]
gff3_basicannotations_simple['Name'] = gff3_basicannotations_simple['tr_id']

# Create set of conditionals for joining gff3 and predflips data frames
#feature_location_match = (predflips['ENST_ID'] == gff3_basicannotations_simple['tr_id']) & (predflips['mutant_position'] >= gff3_basicannotations_simple['transcriptomic_start']) & (predflips['mutant_position'] <= gff3_basicannotations_simple['transcriptomic_end'])

# Make sure we can maintain original int dtypes, because they'll all be floats after joining. So store original dtypes in dict.
orig_dtypes_dict = predflips.dtypes.to_dict()
orig_dtypes_dict.update(gff3_basicannotations_simple.dtypes.to_dict())

# Join gff3 file to predflips
joined = predflips.join(gff3_basicannotations_simple.set_index('Name'), on='Name')

# Make all NaN values are "-1", an int. These are where no matches were made during the join
joined.fillna(-1, inplace=True)

# Restore original dtypes to cols in the data frame, because God those floats are annoying
joined_original_dtypes = joined.apply(lambda x: x.astype(orig_dtypes_dict[x.name]))

# Identify important features / locations:
feature_mutation_loc_match = (joined_original_dtypes['mutant_position'] >= joined_original_dtypes['transcriptomic_start']) & (joined_original_dtypes['mutant_position'] <= joined_original_dtypes['transcriptomic_end'])

important_features = joined_original_dtypes[feature_mutation_loc_match] 

# Write important features to file, but drop redundant ID fields for clarity
joined_original_dtypes = joined_original_dtypes.drop(labels=['ENST_ID', 'tr_id'], axis='columns')
important_features.to_csv("min200_pcRNA_gff3_substitutions_important_features.csv", index=True, header=True, index_label='index')
