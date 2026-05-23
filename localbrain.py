import requests 
import json
import os
from collections import deque
from langchain_huggingface import HuggingFaceEmbeddings

# custom modules
from retriver import RAG
from semantic_router import Semantic_router

class MechatronicTutor:
    """
    The unified brain of the Edge AI Tutor.
    Now utilizing external RAG and Semantic Routing dependencies.
    """
    def __init__(self,max_memory=5):
        self.url = "http://127.0.0.1:8080/v1/chat/completions"
        self.embedding_model= HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"local_files_only": True, "device": "cpu"}
    )
        self.rag = RAG(self.embedding_model)
        self.router = Semantic_router(self.embedding_model)
        
        # Initialize Memory
        self.chat_history = deque(maxlen=max_memory)
        self.persona = (
            "You are an autonomous mechatronics tutor running on Edge AI. "
            "Explain engineering concepts clearly, briefly, and accurately. "
            "Always base your answers strictly on the provided textbook context. "
            "If a student asks a good question, feel free to ask a brief follow-up question to test their understanding."
        )
        print("[SYSTEM] Cognitive Core Ready.")

    def _get_context(self, question: str) -> str:
        """Uses the injected router and RAG classes to fetch data."""
        intent = self.router.semantic_class(question)
        
        if intent == "Technical":
            print("\n[ROUTER] Technical intent detected. Searching Vector DB...")
            # Utilizing your custom streamlined_result method!
            context = self.rag.streamlined_result(question)
            
            if "No relevant textbook content found" not in context:
                print("[RAG] Textbook context retrieved.")
                return context
            else:
                print("[RAG] Query off-topic. No safe threshold match found.")
                return ""
        else:
            print("\n[ROUTER] Casual conversation detected. Bypassing Vector DB.")
            return ""

    def generate_response(self, question: str):
        """Streams tokens from the local BitNet server."""
        textbook_data = self._get_context(question)
        
        messages = [{'role': 'system', 'content': self.persona}]
        
        for interaction in self.chat_history:
            messages.append({'role': 'user', 'content': interaction['user']})
            messages.append({'role': 'assistant', 'content': interaction['tutor']})
            
        if textbook_data:
            augmented_prompt = f"Textbook Hint: {textbook_data}\n\nStudent's Question: {question}"
        else:
            augmented_prompt = question
            
        messages.append({'role': 'user', 'content': augmented_prompt})
        
        payload = {
            'messages': messages, 
            'stream': True, 
            'max_tokens': 256, 
            'temperature': 0.6, 
            'top_k': 40, 
            'repeat_penalty': 1.18, 
            'stop': ['user:', 'User:', '\nUser', 'Student:']
        }
        
        full_reply = ""
        try:
            response = requests.post(self.url, json=payload, stream=True)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').replace('data: ', '').strip()
                    if decoded_line == '[DONE]':
                        break
                    try:
                        chunk = json.loads(decoded_line)
                        token = chunk['choices'][0]['delta'].get('content', '')
                        full_reply += token
                        yield token
                    except json.JSONDecodeError:
                        continue
                        
        except requests.exceptions.RequestException as e:
            yield f"\n[Error] Connection failed: {e}"
            return
            
        self.chat_history.append({'user': augmented_prompt, 'tutor': full_reply})

# --- SYSTEM INITIALIZATION & MAIN LOOP ---
if __name__ == "__main__":
    os.environ["HF_HUB_OFFLINE"] = "1"
    
    print("[SYSTEM] Booting up Hardware Dependencies...")
    
    # 1. Load the heavy embedding model exactly ONCE
    
    
    # 2. Inject it into your specialized modules
    # rag_module = RAG(shared_embedding_model)
    # router_module = Semantic_router(shared_embedding_model)
    
    # 3. Boot the tutor with the active modules
    tutor = MechatronicTutor()
    
    while True:
        prompt = input('\nYou: ')
        if prompt.lower() in ['exit', 'quit']:
            break
        if not prompt.strip():
            continue

        print("Tutor: ", end="", flush=True)
        for token in tutor.generate_response(prompt):
            print(token, end='', flush=True)
            
        print("\n")