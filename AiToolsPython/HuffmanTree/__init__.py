class PriorityQueue:
    def __init__(self):
        self.heap = []

    def _parent(self, index):
        return (index - 1) // 2

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _heapify_up(self, index):
        parent_index = self._parent(index)
        if index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        left = self._left_child(index)
        right = self._right_child(index)
        smallest = index
        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def insert(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0:
            raise IndexError('extract_min from empty PriorityQueue')
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        item = self.heap.pop()
        self._heapify_down(0)
        return item

    def is_empty(self):
        return len(self.heap) == 0


class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self, sequence):
        self.sequence = sequence
        self.root = None
        self.codebook = {}
        self.build_huffman_tree()
        self.generate_huffman_codes()

    def build_huffman_tree(self):
        frequency = {}
        for char in self.sequence:
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1

        pq = PriorityQueue()
        for char, freq in frequency.items():
            pq.insert((freq, HuffmanNode(char, freq)))

        while len(pq.heap) > 1:
            freq1, left_node = pq.extract_min()
            freq2, right_node = pq.extract_min()
            merged_node = HuffmanNode(freq=freq1 + freq2)
            merged_node.left = left_node
            merged_node.right = right_node
            pq.insert((merged_node.freq, merged_node))

        self.root = pq.extract_min()[1]

    def generate_huffman_codes(self, node=None, prefix=''):
        if node is None:
            node = self.root
        if node.char is not None:
            self.codebook[node.char] = prefix
        else:
            if node.left:
                self.generate_huffman_codes(node.left, prefix + '0')
            if node.right:
                self.generate_huffman_codes(node.right, prefix + '1')

    def encode_sequence(self):
        encoded_sequence = ''.join(self.codebook[char] for char in self.sequence)
        return encoded_sequence

    def decode_sequence(self, encoded_sequence):
        decoded_sequence = []
        current_node = self.root
        for bit in encoded_sequence:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node.char is not None:
                decoded_sequence.append(current_node.char)
                current_node = self.root
        return ''.join(decoded_sequence)

    def visualize_huffman_tree(self, node=None, graph=None, node_id=0, parent_id=None, edge_label=''):
        from graphviz import Digraph
        if graph is None:
            graph = Digraph()
        if node is None:
            node = self.root

        current_id = node_id
        label = f'{node.char}:{node.freq}' if node.char else f'{node.freq}'
        graph.node(str(current_id), label=label)

        if parent_id is not None:
            graph.edge(str(parent_id), str(current_id), label=edge_label)

        next_id = current_id + 1
        if node.left:
            next_id, graph = self.visualize_huffman_tree(node.left, graph, next_id, current_id, '0')
        if node.right:
            next_id, graph = self.visualize_huffman_tree(node.right, graph, next_id, current_id, '1')

        return next_id, graph

    def render_tree(self, filename='huffman_tree'):
        _, graph = self.visualize_huffman_tree()
        graph.render(filename, format='png', cleanup=True)


# Example usage:
if __name__ == "__main__":
    sequence = "this is an example for huffman encoding"
    huffman = HuffmanCoding(sequence)

    print("Huffman Codes for each character:")
    for char, code in huffman.codebook.items():
        print(f"{char}: {code}")

    encoded_sequence = huffman.encode_sequence()
    print("\nEncoded Sequence:")
    print(encoded_sequence)

    decoded_sequence = huffman.decode_sequence(encoded_sequence)
    print("\nDecoded Sequence:")
    print(decoded_sequence)

    # Optional: Render the Huffman Tree
    huffman.render_tree('huffman_tree')
