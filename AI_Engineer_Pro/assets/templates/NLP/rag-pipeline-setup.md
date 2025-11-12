# RAG Pipeline Setup

Complete Retrieval-Augmented Generation system for document Q&A.

## Architecture

```
User Query → Embedding → Vector Search → Context Retrieval → LLM → Answer
```

## Full RAG Implementation

```python
from sentence_transformers import SentenceTransformer
import chromadb
from transformers import pipeline
import torch

class RAGPipeline:
    def __init__(self, embedding_model="all-MiniLM-L6-v2", llm_model="gpt2"):
        # Embedding model
        self.embedder = SentenceTransformer(embedding_model)
        
        # Vector database
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("documents")
        
        # LLM for generation
        self.llm = pipeline(
            "text-generation",
            model=llm_model,
            device=0 if torch.cuda.is_available() else -1
        )
    
    def add_documents(self, documents, ids=None):
        """Add documents to vector store"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Generate embeddings
        embeddings = self.embedder.encode(documents).tolist()
        
        # Store in ChromaDB
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )
        
        print(f"✅ Added {len(documents)} documents")
    
    def retrieve(self, query, top_k=3):
        """Retrieve relevant documents"""
        # Embed query
        query_embedding = self.embedder.encode(query).tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results['documents'][0], results['distances'][0]
    
    def generate_answer(self, query, context):
        """Generate answer using LLM with context"""
        prompt = f"""Context: {context}

Question: {query}

Answer:"""
        
        response = self.llm(
            prompt,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        
        return response[0]['generated_text'].split("Answer:")[-1].strip()
    
    def query(self, question, top_k=3):
        """End-to-end RAG query"""
        # 1. Retrieve relevant docs
        docs, distances = self.retrieve(question, top_k=top_k)
        
        print(f"\n📚 Retrieved {len(docs)} documents:")
        for i, (doc, dist) in enumerate(zip(docs, distances)):
            print(f"  {i+1}. [{dist:.3f}] {doc[:100]}...")
        
        # 2. Combine context
        context = "\n\n".join(docs)
        
        # 3. Generate answer
        answer = self.generate_answer(question, context)
        
        return {
            'answer': answer,
            'sources': docs,
            'distances': distances
        }

# Usage
if __name__ == "__main__":
    # Initialize
    rag = RAGPipeline()
    
    # Add knowledge base
    documents = [
        "PCB scratches are surface defects caused by handling or manufacturing.",
        "Solder bridges occur when solder connects two pins that should be separate.",
        "Missing components are detected by comparing actual vs expected component positions.",
        "Cracks in PCB substrate can cause electrical failures and should be rejected.",
    ]
    
    rag.add_documents(documents)
    
    # Query
    result = rag.query("What causes solder bridges?")
    print(f"\n💬 Answer: {result['answer']}")
```

## Advanced RAG with LangChain

```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader, PDFLoader

# 1. Load documents
loader = TextLoader("knowledge_base.txt")
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
texts = text_splitter.split_documents(documents)

# 3. Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 4. Create vector store
vectorstore = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 5. Setup LLM
from transformers import pipeline
llm_pipeline = pipeline(
    "text-generation",
    model="gpt2",
    max_new_tokens=256
)
llm = HuggingFacePipeline(pipeline=llm_pipeline)

# 6. Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# 7. Query
query = "Explain PCB defect types"
result = qa_chain({"query": query})

print(f"Answer: {result['result']}")
print(f"Sources: {len(result['source_documents'])} documents")
```

## RAG with OpenAI

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# Setup
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(documents, embeddings)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Create conversational chain
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Chat with history
chat_history = []
query = "What are PCB defects?"
result = qa({"question": query, "chat_history": chat_history})

print(result["answer"])
chat_history.append((query, result["answer"]))

# Follow-up question
query2 = "How can we detect them?"
result2 = qa({"question": query2, "chat_history": chat_history})
print(result2["answer"])
```

## Hybrid Search (Keyword + Semantic)

```python
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Semantic search
        self.embeddings = self.embedder.encode(documents)
        
        # Keyword search (BM25)
        tokenized_docs = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def search(self, query, top_k=5, alpha=0.5):
        """
        Hybrid search combining semantic and keyword matching
        alpha: weight for semantic search (1-alpha for BM25)
        """
        # Semantic scores
        query_embedding = self.embedder.encode(query)
        semantic_scores = np.dot(self.embeddings, query_embedding)
        semantic_scores = (semantic_scores - semantic_scores.min()) / (semantic_scores.max() - semantic_scores.min())
        
        # Keyword scores
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_scores = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min())
        
        # Combine scores
        hybrid_scores = alpha * semantic_scores + (1 - alpha) * bm25_scores
        
        # Get top K
        top_indices = np.argsort(hybrid_scores)[-top_k:][::-1]
        
        return [self.documents[i] for i in top_indices], hybrid_scores[top_indices]

# Usage
retriever = HybridRetriever(documents)
results, scores = retriever.search("PCB solder defects", top_k=3)
```

## Evaluation Metrics

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall

# Prepare evaluation dataset
eval_data = {
    'question': ["What causes solder bridges?"],
    'answer': [generated_answer],
    'contexts': [[context1, context2]],
    'ground_truths': [["Solder bridges occur when..."]]
}

# Evaluate
result = evaluate(
    eval_data,
    metrics=[faithfulness, answer_relevancy, context_recall]
)

print(result)
```

## Best Practices

1. **Chunking**: Split docs into 300-500 tokens with 50-100 token overlap
2. **Embeddings**: Use domain-specific models when possible
3. **Retrieval**: Start with k=3-5, tune based on results
4. **Re-ranking**: Use cross-encoder for better ranking
5. **Caching**: Cache frequently accessed embeddings
6. **Metadata**: Store metadata (source, date) with chunks

## Production Tips

- Use **pgvector** or **Pinecone** for scale
- Implement **caching** for common queries
- Add **re-ranking** layer for better results
- Monitor **latency** (aim for <2s end-to-end)
- Use **streaming** for real-time responses
