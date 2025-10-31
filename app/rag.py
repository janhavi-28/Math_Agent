# RAG engine (same as v1) with minor improvements
import os, json, numpy as np
from sentence_transformers import SentenceTransformer
import faiss

KB_FILE = os.path.join(os.path.dirname(__file__), "..", "kb.json")

class RAGEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2', k=3):
        self.k = k
        self.model = SentenceTransformer(model_name)
        self.docs = []
        self.embeddings = None
        self.index = None
        self._load_kb()

    def _load_kb(self):
        if not os.path.exists(KB_FILE):
            sample = [
                {"id":"q1","question":"what is the sum of 2+3?","solution":"Step 1: Recognize these are integers. Step 2: Add them: 2+3=5. Final: 5"},
                {"id":"q2","question":"differentiate x^2","solution":"d/dx x^2 = 2x"},
                {"id":"q3","question":"integrate 2x","solution":"∫2x dx = x^2 + C"}
            ]
            with open(KB_FILE,"w") as f:
                json.dump(sample,f,indent=2)
        with open(KB_FILE,"r") as f:
            self.docs = json.load(f)
        texts = [d['question'] for d in self.docs]
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings)

    def retrieve(self, query):
        q_emb = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(q_emb)
        D, I = self.index.search(q_emb, self.k)
        scores = D[0].tolist()
        idxs = I[0].tolist()
        if scores[0] < 0.65:
            return None, []
        results = [{"doc": self.docs[i], "score": scores[j]} for j,i in enumerate(idxs) if i != -1]
        return results[0]['doc'], results
