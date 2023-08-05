import numpy as np
import faiss
import requests
from io import StringIO
import pandas as pd
from GeneVecTools import reader
from GeneVecTools import encoder
import tensorflow as tf
from datetime import datetime


# res = requests.get(
#     "https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/sick2014/SICK_train.txt"
# )

# text = res.text
# text[:100]

# data = pd.read_csv(StringIO(text), sep="\t")
# data.head()

# sentences = data["sentence_A"].tolist()
# print(sentences[:5])


class intToVec:
    def __init__(self) -> None:
        pass

    def embed_int(self, a, n):
        a = str(a)
        k, m = divmod(len(a), n)
        return list(
            (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))
        )

    def unembed_int(self, lst):
        ret = ""
        for elt in lst:
            ret += elt
        return int(ret)


class VecSS:
    def __init__(
        self,
        f="small_cDNA_Sequences_pbmc_1k_v2_S1_L002_R2_001.fastq",
        length=10000,
        encoding="one-hot-encoding",
        bits=8,
    ):
        self.encoding = encoding
        self.bits = bits
        self.__file = f
        self.sequences = self.readq()
        self.s = self.sequences[:length]
        self.embeddings = self.embed(self.s)
        self.samples = 2

    #        self.enc = encoder.Encoder(bits=self.bits, encoding=self.encoding)

    def readq(self):
        R = reader.Reader()
        mp, count, total_len, quality = R.read_fastq(self.__file)

        sequences_dict_items = mp.values()
        sequences = list(sequences_dict_items)

        return sequences

    # INDEPENDENT VARIABLE

    def embed(self, s):
        enc = encoder.Encoder(bits=self.bits, encoding=self.encoding)
        embeddings = []
        for seq in s:
            embeddings.append(enc.encode_sequence(seq))
        return embeddings

    def unembed(self, embeddings):
        enc = encoder.Encoder(bits=self.bits, encoding=self.encoding)
        original = []
        for embedding in embeddings:
            original.append(enc.decode_sequence(embedding))
        return original

    # texts = np.random.random((100000, 64)).astype("float32")
    # print(texts)

    # model = tf.keras.Sequential()
    # embedding_layer = tf.keras.layers.Embedding(len(self.s), 64, input_length=len(self.s[0]))
    # embeddings_64 = embedding_layer(sequences)
    def embed_string(self, embeddings):
        ITV = intToVec()
        embeddings_64 = []
        for s in embeddings:
            embeddings_64.append(ITV.embed_int(s, 64))
        embeddings_64 = np.asarray(embeddings_64).astype("float32")
        return embeddings_64

    # def run_search(self, d=64,embeddings=self.emeddings):
    def run_search(self, d=64, k=4):
        embeddings_64 = self.embed_string(self.embeddings)
        index = faiss.IndexFlatL2(d)  # build the index
        # print(index.is_trained)
        index.add(embeddings_64)  # add vectors to the index
        print("index.ntotal")
        print(index.ntotal)

        startTime = datetime.now()

        D, I = index.search(embeddings_64[:10], k)
        # print("I is index")
        # print(I)
        # print("D is distance squared")
        # print(D)
        # print(datetime.now() - startTime)

        time = datetime.now() - startTime

        return D, I, time
