from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import warnings
import os


class RAG:
    """Handles retrival from the vector data base"""
    def __init__(self, embedding_model):

        warnings.filterwarnings("ignore")
        # os.environ["HF_HUB_OFFLINE"] = "1" #ensures the embedding model runs offline

        # instance of the embedding model
        self.embedding = embedding_model
        
        # instance of vector data base
        self.vector_db = Chroma(
            persist_directory="./chroma_db/chroma_db",
            embedding_function= self.embedding,
            collection_metadata={"hnsw:space": "cosine"}
        )
    def retrieve(self, query:str, k: int=1, threshold: float = 0.4) -> list:
        """main retrival function. Returns document based on similarity threshold"""
        results = []
        docs_and_scores = self.vector_db.similarity_search_with_score(query, k=k)
        for doc, score in docs_and_scores:
            if score <= threshold: 
                results.append({
                    "content": doc.page_content,
                    "score": score,
                    "source": doc.metadata.get("source", "Unknown")
                })
                
        return results
    def streamlined_result(self, query:str, k: int=1, threshold: float = 0.4):

        result = self.retrieve(query, k=k, threshold=threshold)
        
        if not result:
            return "No relevant textbook content found for this query."

        raw_text = result[0]['content']
        
        bare_minimum = raw_text.split('.')[0] + "." if "." in raw_text else raw_text
        
        return bare_minimum

if __name__ == "__main__":
    model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"local_files_only": True, "device": "cpu"})
    r = RAG(model)
    print(r.streamlined_result(query="What is mechatronics"))
    while True:
        query = input("Enter query")
        print(r.streamlined_result(query=query))

