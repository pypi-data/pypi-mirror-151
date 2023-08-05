# from email.policy import default

from numpy import byte


class Encoder:
    # one-hot encoding
    __mapping = {"A": 8, "C": 4, "G": 2, "T": 1, "N": 15, "E": 0}
    __rmapping = {8: "A", 4: "C", 2: "G", 1: "T", 15: "N", 0: "E"}

    # paper
    # __mapping = {"A": 0, "C": 1, "G": 2, "T": 3}
    # __rmapping = {0: "A", 1: "C", 2: "G", 3: "T"}

    # not encoded
    # __mapping = {"A": ord('A'), "C": ord('C'), "G": ord('G'), "T": ord('T')}
    # __rmapping = {ord('A'): "A", ord('C'): "C", ord('G'): "G", ord('T'): "T"}

    def __init__(self, bits=8, encoding="one-hot-encoding"):
        self.__bits = bits
        self.__base_size = 2 ** bits

        if encoding == "one-hot-encoding":
            self.__mapping = {"A": 8, "C": 4, "G": 2, "T": 1, "N": 15, "E": 0}
            self.__rmapping = {8: "A", 4: "C", 2: "G", 1: "T", 15: "N", 0: "E"}
        elif encoding == "standard":
            self.__mapping = {"A": 0, "C": 1, "G": 2, "T": 3, "N": 4}
            self.__rmapping = {0: "A", 1: "C", 2: "G", 3: "T", 4: "N"}
        elif encoding == "no-encoding":
            self.__mapping = {
                "A": ord("A"),
                "C": ord("C"),
                "G": ord("G"),
                "T": ord("T"),
                "N": ord("N"),
            }
            self.__rmapping = {
                ord("A"): "A",
                ord("C"): "C",
                ord("G"): "G",
                ord("T"): "T",
                ord("N"): "N",
            }
        else:
            pass

#    def raw_encoding(self,sequence):
        
    def encode_sequence(self, sequence):
        val = 0
        for i, base in enumerate(sequence):
            val += self.__mapping[base] * (self.__base_size ** i)
        return val

    def encode_sequences(self, cluster):
        ec = []
        for sequence in cluster:
            es = self.encode_sequence(sequence)
            ec.append(es)
        return ec

    # TODO
    def decode_sequences(self, cluster):
        ec = []
        for sequence, index in cluster:
            length = (len(sequence) + (8 // self.__bits) - 1) // (8 // self.__bits)
            es = self.encode_sequence(sequence).to_bytes(length, "little")
            ec.append(es)
        return ec

    def encode_cluster(self, cluster) -> bytearray:
        ec = []
        N = len(cluster)
        indices = []
        lengths = []

        byte_array = N.to_bytes(4, "little")

        for sequence, index in cluster:
            length = (len(sequence) + (8 // self.__bits) - 1) // (
                8 // self.__bits
            )  # one-hot encoding
            # length = (len(sequence) + 4) // 4 # paper

            es = self.encode_sequence(sequence).to_bytes(length, "little")
            ec.append(es)
            indices.append(index)
            lengths.append(length)
            # print(sequence, int.from_bytes(b, 'little', signed=False))

        for index in indices:
            byte_array += index.to_bytes(4, "little")

        for length in lengths:
            byte_array += length.to_bytes(1, "little")

        for es in ec:
            byte_array += es

        return byte_array

    def encode_clusters(self, clusters):
        out = []
        for cluster in clusters:
            out.append(self.encode_cluster(cluster))
        return out

    def decode_sequence(self, val):
        import math

        # output_sequence = []
        # for base in sequence:
        #     output_sequence.append(map_base(base))
        # return output_sequence
        sequence = ""
        n = math.floor(math.log(val) / math.log(self.__base_size))

        while val > 0:
            next_layer = val % self.__base_size ** n
            sequence = (
                str(self.__rmapping[int((val - next_layer) / self.__base_size ** n)])
                + sequence
            )
            n -= 1
            val = next_layer

        return sequence

    def decode_cluster(self, byte_array):
        N = int.from_bytes(byte_array[:4], "little", signed=False)
        indices = []
        lengths = []
        cluster = []

        for i in range(1, N + 1):
            indices.append(
                int.from_bytes(byte_array[4 * i : 4 * i + 4], "little", signed=False)
            )

        for i in range(4 * N + 4, 5 * N + 4):
            lengths.append(
                int.from_bytes(byte_array[i : i + 1], "little", signed=False)
            )

        indent = 5 * N + 4
        for i in range(N):
            esb = byte_array[indent : indent + lengths[i]]
            es = int.from_bytes(esb, "little", signed=False)
            cluster.append((self.decode_sequence(es), indices[i]))
            indent += lengths[i]

        return cluster

    def decode_clusters(self, clusters):
        out = []
        for cluster in clusters:
            out.append(self.decode_cluster(cluster))
        return out


if __name__ == "__main__":
    cluster = [
        [["ACGT", 1], ["TCGA", 1], ["ACGTGTCGAGTGT", 2]],
        [["ACGATGCGCGCTAGGT", 1], ["ACGTGTCGCGCAATCGCTAGAC", 2]],
    ]

    encoder = Encoder(8, encoding="no-encoding")

    encoded = encoder.encode_clusters(cluster)
    print(encoded)
    decoded = encoder.decode_clusters(encoded)
    print(decoded)
    print(decoded == cluster)
