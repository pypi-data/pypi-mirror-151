from io import TextIOWrapper
import sys
import os
from Bio import SeqIO
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.SeqIO.QualityIO import FastqGeneralIterator
import pysam

# pip install -r requirements.txt


class Reader:
    def __init__(self):
        pass

    def read_fasta(self, input_path):
        count = 0
        total_len = 0
        mp = {}
        with open(input_path) as in_handle:
            for title, seq in SimpleFastaParser(in_handle):
                mp[title] = seq
                count += 1
                total_len += len(seq)
        return mp, count, total_len

    def read_fastq(self, input_path):
        count = 0
        total_len = 0
        mp = {}
        quality = []
        with open(input_path) as in_handle:
            for title, seq, qual in FastqGeneralIterator(in_handle):
                mp[title] = seq
                count += 1
                total_len += len(seq)
                quality.append(qual)
        return mp, count, total_len, quality

    def read_fastq_gen(self, input_path):
        with open(input_path) as in_handle:
            idx = 0
            for title, seq, qual in FastqGeneralIterator(in_handle):
                yield idx, seq, qual
                idx += 1

    def read_sam(self, input_path):
        samfile = pysam.AlignmentFile(input_path, "r")
        iter = samfile.fetch()
        mp = {}
        for x in iter:
            mp[x.query_name] = (
                x.query_sequence,
                x.flag,
                x.reference_id,
                x.reference_start,
                x.mapping_quality,
                x.cigar,
                x.next_reference_id,
                x.next_reference_start,
                x.template_length,
                x.query_qualities,
                x.tags,
            )
        return mp

    def read_bam(self, input_path):
        # note: may need to run 'samtools index X.bam'
        samfile = pysam.AlignmentFile(input_path, "rb")
        iter = samfile.fetch()
        mp = {}
        for x in iter:
            mp[x.query_name] = (
                x.query_sequence,
                x.flag,
                x.reference_id,
                x.reference_start,
                x.mapping_quality,
                x.cigar,
                x.next_reference_id,
                x.next_reference_start,
                x.template_length,
                x.query_qualities,
                x.tags,
            )
        return mp

    def read_cram(self, input_path):
        samfile = pysam.AlignmentFile(input_path, "rc")
        return samfile


# def read_sam(self, input_path, QNAME_list):
#     mate_pairs = {}
#     QNAME_list = set(QNAME_list)
#     with open(input_path, "rb") as samFile:
#         for line in samFile:
#             QNAME = line.split("\t")[0]
#             if QNAME in QNAME_list:
#                 try:
#                     mate_pairs[QNAME].append(line)
#                 except KeyError:
#                     mate_pairs[QNAME] = [line]
#     with open(parsed_SAM_file_path, "wb") as outfile:
#         for read, mate in mate_pairs.values():
#             outfile.write(read + "\n" + mate + "\n")


# def read_fasta(self, input_file):
#     mp = {}
#     fasta_sequences = SeqIO.parse(open(input_file),'fasta')
#     for fasta in fasta_sequences:
#         name, sequence = fasta.id, str(fasta.seq)
#         mp[name] = sequence
#     return mp

# def read_fastq(self,input_file):

# def readFastA(self, input_file,output_file):
#     fasta_sequences = SeqIO.parse(open(input_file),'fasta')
#     with open(output_file) as out_file:
#         for fasta in fasta_sequences:
#             name, sequence = fasta.id, str(fasta.seq)
#             new_sequence = some_function(sequence)
#             write_fasta(out_file)

# def readFastA(self, f: TextIOWrapper):
#     sequences = []
#     for line in f:
#         if line.startswith('>'):
#             _id = line[1:]
#         else:
#             sequences.append({'id': _id, 'sequence': line})
#     return sequences

# def read_fastq(self,
#     def process(lines=None):
#         ks = ['name', 'sequence', 'optional', 'quality']
#         return {k: v for k, v in zip(ks, lines)}

#     try:
#         fn = sys.argv[1]
#     except IndexError as ie:
#         raise SystemError("Error: Specify file name\n")

#     if not os.path.exists(fn):
#         raise SystemError("Error: File does not exist\n")

#     n = 4
#     with open(fn, 'r') as fh:
#         lines = []
#         for line in fh:
#             lines.append(line.rstrip())
#             if len(lines) == n:
#                 record = process(lines)
#                 sys.stderr.write("Record: %s\n" % (str(record)))
#                 lines = []
