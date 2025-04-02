class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0  # Stores occurrences of the word

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.count += 1  # Increase count at the last letter

    def count_occurrences(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return 0  # Word not found
            node = node.children[char]
        return node.count  # Return word count
