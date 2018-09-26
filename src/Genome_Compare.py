#! /usr/bin/python

"""
Try to get the position based on the question given by edX from the genome

Q1: ccggcctcgggaag
Q2: ttgcggacgctagc
Q3: tcgggctccccccg
Q4: ggggggaaggcgga
Q5: tctgtccccccccg
"""

import os
import json
import numpy

setting_file = os.path.dirname(os.getcwd()) + '/setting.json'
data_file = os.path.dirname(os.getcwd()) + '/data/genome_ref_sample.json'


def split_into_read(origin, max_len):
    array = numpy.empty(shape=(len(origin) - 13, 2), dtype=object)

    for i in range(0, len(origin)-13):
        short_read = origin[0 + i : max_len + i]
        index_position = i
        #print("position: {0}; string: {1}".format(index_position, short_read))
        array[i, 0] = short_read
        array[i, 1] = index_position

    return array


def compare_genome(array):
    qlist = numpy.empty(shape=(5, 1), dtype=object)

    qlist[0] = 'ccggcctcgggaag'
    qlist[1] = 'ttgcggacgctagc'
    qlist[2] = 'tcgggctccccccg'
    qlist[3] = 'ggggggaaggcgga'
    qlist[4] = 'tctgtccccccccg'

    no_match = 0

    for pos, item in enumerate(qlist):
        qcomp = str(item[0])
        print()
        print("Comparing item {0}: {1} with L-long reference".format(pos + 1, qcomp))

        for read in array:
            lcomp = str(read[0])
            lind = int(read[1])

            if lcomp.lower() == qcomp.lower():
                no_match += 1
                print()
                print("++Fully Match ## Long Ref: {0} and Question: {1}".format(lcomp, qcomp))
                # index + 1 because started from 0
                print("++L-long reference index location: {0}".format(lind + 1))
            else:
                no_sub_match = 0
                # Start comparing starting from first character
                for x, y in zip(lcomp, qcomp):
                    if x == y:
                        no_sub_match += 1
                        #print("||++Character Matched ## Long Ref: {0} and Question: {1}".format(x, y))
                    #else:
                        #print("||--Character Not Matched ## Long Ref: {0} and Question: {1}".format(x, y))

                if (read_max_len - 1) == no_sub_match:
                    no_match += 1
                    print()
                    print("||==Total Characters Matched: {0}".format(no_sub_match))
                    print("++Partially Match ## Long Ref: {0} and Question: {1}".format(lcomp, qcomp))
                    # index + 1 because started from 0
                    print("++L-long reference index location: {0}".format(lind + 1))
                #else:
                    #print("||==Total Characters Matched: {0}".format(no_sub_match))
                    #print("--Not Match ## Long Ref: {0} and Question: {1}".format(lcomp, qcomp))

    print()
    print("==Total Fully / Partially Matched Genome: {0}".format(no_match))

"""
Configuration from setting file 
"""
with open(setting_file) as e:
    settings = json.load(e)
    read_max_len = settings['max_length_for_read']


"""
Read the Genome L-long reference from json file
"""
with open(data_file) as f:
    genomes = json.load(f)
    #genome_data = genomes['gen_data']
    genome_origin = genomes['gen_data'][0]['origin']


"""
Get max length of genome origin and create 2d-array for indexing
"""
genome_array = split_into_read(genome_origin, read_max_len)

compare_genome(genome_array)