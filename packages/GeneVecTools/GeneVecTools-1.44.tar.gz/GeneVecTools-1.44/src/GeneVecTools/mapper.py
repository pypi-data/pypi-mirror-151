import enum
from GeneVecTools import reader
import numpy as np
import warnings
import gzip

# from functools import lru_cache

# import tensorflow_io as tfio
# import tensorflow as tf
import math
import zlib
from GeneVecTools import encoder

# from PineConeExperiments.kmeans import Cluster


class Mapper:
    __mapping = {"A": 0, "C": 1, "G": 2, "T": 3}
    __rmapping = {0: "A", 1: "C", 2: "G", 3: "T"}

    def __init__(self, R, k, m):
        self.fs = Mapper.feature_set(R, k)
        self.hfs = Mapper.select_high_variance(self.fs, m)

    @classmethod
    def encode(cls, s) -> int:
        res = 0
        for i, c in enumerate(s):
            res += cls.__mapping[c] * (4 ** i)
        return res

    @classmethod
    def decode(cls, c, k) -> str:
        res = ""
        for i in range(k):
            res += cls.__rmapping[c % 4]
            c //= 4
        return res

    @classmethod
    def vec(cls, i, j, k, R) -> float:
        return (R[i].count(cls.decode(j, k)) / len(R[i]), i)

    @classmethod
    def feature_set(cls, R, k):
        return [[cls.vec(i, j, k, R) for j in range(4 ** k)] for i in range(len(R))]

    @classmethod
    def select_high_variance(cls, feature_set, m):
        fm = np.array(feature_set)
        # [:,:,0] = [...,0]
        var = np.var(fm[:, :, 0], 0)
        return fm[:, var >= np.sort(var)[-m]]


# @lru_cache
# cython here??
def kmeans(V, k):
    from sklearn.cluster import KMeans

    res = KMeans(n_clusters=k, random_state=0).fit(V[..., 0])
    return V[res.labels_ == 0], V[res.labels_ == 1]


def dist(v1: np.ndarray, v2: np.ndarray) -> float:
    return np.linalg.norm(v1 - v2)


def mindist(ca0: np.ndarray, cb: np.ndarray) -> np.ndarray:
    d = np.array([dist(cbi, ca0) for cbi in cb])
    return cb[d == np.min(d)][0]


# cython here??
def cluster(V, l=0.3):
    if len(V) < 3:
        return [V]
    else:

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            c1, c2 = kmeans(V, 2)
        if len(c1) == 0:
            return [c2]
        if len(c2) == 0:
            return [c1]

        if len(c1) + len(c2) >= 4 and (len(c1) == 1 and len(c2) == 1):
            if len(c1) != 1:
                c2, c1 = c1, c2
            ca, cb = c1, c2

            cbmin = mindist(ca[0], cb)
            if dist(ca[0], cbmin) < l * dist(mindist(cbmin, cb[cb != cbmin])):
                ca = np.array([ca[0], cbmin])
                cb = cb[cb != cbmin]
                return cluster(cb, l) + [ca]
        else:
            return cluster(c1, l) + cluster(c2, l)


def transform(V):
    S = []
    for v in V:
        S.append((v[..., 0], int(v[0, 1])))
    return S


def encode_base(base):
    # turn into dictionary
    if base == "A":
        # 1000
        return 8
    elif base == "C":
        # 0100
        return 4
    elif base == "G":
        # 0010
        return 2
    elif base == "T":
        # 0001
        return 1
    else:
        # 1111
        return 15


def encode_sequence(sequence):
    # output_sequence = []
    # for base in sequence:
    #     output_sequence.append(map_base(base))
    # return output_sequence
    val = 0
    for i, base in enumerate(sequence):
        val += encode_base(base) * (16 ** i)
    return val
    # to reverse int(tmp,2)


# cython; too speed up
# setting types prior
# Pypy just in time complier for python
# parallelize

# def encode_cluster(cluster_of_sequences):
#     output_cluster = []
#     output_indexes = []

#     for sequences in cluster_of_sequences:
#         inner_list = []
#         inner_list_index = []
#         for sequence, i in sequences:
#             # encoded_sequence is an int
#             encoded_sequence = encode_sequence(sequence)
#             # compressed_data = zlib.compress
#             bytes_sequence = encoded_sequence.to_bytes(
#                 (encoded_sequence.bit_length() + 7) // 8, byteorder="little"
#             )
#             inner_list.append(bytes_sequence)
#             inner_list_index.append(i)
#         output_cluster.append(inner_list)
#         output_indexes.append(inner_list_index)
#     return output_cluster, output_indexes


# def encode_cluster(cluster, sequences):
#     output_cluster = []
#     for _, index in cluster:
#         output_cluster.append(encode_sequence(sequences[index]))
#     return output_cluster


def groupings(S, sequences):
    clust = []
    # S = cluster(mapper.hfs)
    for x, V in enumerate(S):
        sub_list = []
        for _, i in transform(V):
            sub_list.append((sequences[i], i))
        clust.append(sub_list)
    return clust


def compress_clusters(int_binary_cluster, compressor=gzip):
    """
    The problem we are facing is that a byte can only represent numbers from 0-255.
    What we can do is split an integer N into multiple smaller integers {a0, a1, a2,..., a_k}
    where N = Σ (a_j * (256^k), then convert that list of smaller integers into a byte array.
    """
    comp = []
    for int_sequences in int_binary_cluster:
        comp.append(compressor.compress(int_sequences))
        # list() to reverse, alt is bytearray
        # inner_list = []
        # for int_sequence, i in int_sequences:
        #     inner_list.append(gzip.compress(bin(int_sequence)), gzip.compress(bin(i)))
        #     # to reverse int(tmp,2)
        # compressed.append(inner_list)
    return comp


def get_size_compressed(compressed_cluster):
    return sum([len(cluster) for cluster in compressed_cluster])


def decode_base(int_base):
    if int_base == 8:
        # 1000
        return "A"
    elif int_base == 4:
        # 0100
        return "C"
    elif int_base == 2:
        # 0010
        return "G"
    elif int_base == 1:
        # 0001
        return "T"
    else:
        # 1111
        return "N"


def decode_sequence(val):
    # output_sequence = []
    # for base in sequence:
    #     output_sequence.append(map_base(base))
    # return output_sequence
    sequence = ""
    n = math.floor(math.log(val) / math.log(16))

    while val > 0:
        next_layer = val % 16 ** n
        sequence = str(decode_base(int((val - next_layer) / 16 ** n))) + sequence
        n -= 1
        val = next_layer

    return sequence
    # to reverse int(tmp,2)


def decode_cluster(output_cluster, output_indexes):
    cluster_of_sequences = []

    for i, encoded_sequences in enumerate(output_cluster):
        inner_list = []
        for j, encoded_sequence in enumerate(encoded_sequences):
            inner_list.append((decode_sequence(encoded_sequence), output_indexes[i][j]))
        cluster_of_sequences.append(inner_list)

    return cluster_of_sequences


def convert(num: int) -> list:
    numlist = []
    while num > 0:
        base = num % 16
        if base == 1:
            numlist.append([0, 0, 0, 1])
        elif base == 2:
            numlist.append([0, 0, 1, 0])
        elif base == 4:
            numlist.append([0, 1, 0, 0])
        elif base == 8:
            numlist.append([1, 0, 0, 0])
        else:
            numlist.append([1, 1, 1, 1])
        num //= 16
    return numlist


# def encode_cluster(cluster, sequences):
#     output_cluster = []
#     for _, index in cluster:
#         output_cluster.append(encode_sequence(sequences[index]))
#     return output_cluster


# def decode_groupings(S, sequences):
#     clust = []
#     # S = cluster(mapper.hfs)
#     for x, V in enumerate(S):
#         sub_list = []
#         if x > 500:
#             break
#         for _, i in transform(V):
#             sub_list.append((sequences[i], i))
#         clust.append(sub_list)
#     return clust


# convert list of integers into byte array -> should be compatible with gzip
# Implement reverse for decompress


if __name__ == "__main__":
    # print(Mapper.encode('GT'))
    R = reader.Reader()
    mp, count, total_len, quality = R.read_fastq(
        "smaller_cDNA_100_sequences/small_cDNA_Sequences_pbmc_1k_v2_S1_L002_R2_001.fastq"
    )
    sequences_dict_items = mp.values()
    sequences = list(sequences_dict_items)

    # unclustered_sequences_bytes = bytearray([x.encode() for x in sequences])
    # unclustered_compressed = gzip.compress(sequences)
    # f_out = gzip.open("/unclustered.gz", "wb")
    # f_out.writelines(unclustered_compressed)
    # f_out.close()

    mapper = Mapper(sequences, 2, 3)
    # print(mapper.hfs)

    # for v, i in transform(mapper.hfs):
    #     print(sequences[i], v)
    groups_of_similar_kmers = cluster(mapper.hfs)

    cluster_of_sequences = groupings(groups_of_similar_kmers, sequences)

    print(np.shape(cluster_of_sequences))

    # clustered_compressed = gzip.compress(cluster_of_sequences)
    # f_out = gzip.open("/clustered.gz", "wb")
    # f_out.writelines(clustered_compressed)
    # f_out.close()

    # print(np.shape(cluster_of_sequences))
    # int_binary_cluster, output_indexes = encode_cluster(cluster_of_sequences)
    # print(int_binary_cluster)
    # gzipped_int_binary_cluster = zlib.compress(int_binary_cluster)
    # with gzip.open("clustered_compressed.gz", "wb") as f:
    #     f.write(gzipped_int_binary_cluster)
    # f.close()

    # compress:
    encoder = encoder.Encoder(4)
    c = encoder.encode_sequences(sequences)
    print(c)
    # print(len(sequences))
    # print(len(c))
    # compressed_cluster = compress_clusters(c)
    # print(compressed_cluster)
    # size = get_size_compressed(compressed_cluster)
    # print(size)

    # decompress:
    # TODO
    # decompress_clusters(compressed_cluster)

    # # print(compressed_cluster)
    # decoded = Encoder.self.decode_clusters(c)
    # decoded = encoder.decode_clusters(c)

    # with open("decoded.out", "a")

    # print(decoded)
    # print(cluster_of_sequences == decoded)
    # print(cluster_of_sequences)
    # print(cluster_of_sequences)

    # print(clusters)

    # # C = Cluster()
    # # cluster_set = C.k_means(mapper.hfs, 0.5)
    # # print(cluster_set)
    # # print(kmeans(mapper.hfs, 2))
    # print(mindist(np.array([0, 1]), np.array([[1, 2], [3, 4]])))
