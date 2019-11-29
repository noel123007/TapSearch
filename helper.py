from collections import defaultdict
import re
import pickle


class Index:
    def __init__(self, filename):
        self.docID = {}
        self.index = defaultdict(list)
        self.id = 0
        self.filename = filename

    def index_doc(self):
        with open(self.filename, 'rt') as f:
            text = f.read()
        documents = text.split('\n\n')
        for doc in documents:
            self.docID[self.id] = doc
            tokens = [t.lower() for t in re.split(r'\W+', doc)]
            for token in tokens:
                if self.id not in self.index[token]:
                    self.index[token].append(self.id)
            self.id += 1
        with open('./database/doc_id.pickle', 'wb') as f0:
            pickle.dump(self.docID, f0, pickle.HIGHEST_PROTOCOL)
        with open('./database/index.pickle', 'wb') as f1:
            pickle.dump(self.index, f1, pickle.HIGHEST_PROTOCOL)



