from langchain_huggingface import HuggingFaceEmbeddings
import os
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

os.environ["HF_HUB_OFFLINE"] = "1"

# semantic classes
TECH_DESC = """
mechatronics, robotics, engineering, physics, hardware, electronics, programming, 
algorithms, components, circuits, motors, sensors, voltage, current, pid, arduino, 
esp32, python, kinematics, torque, signals, microcontrollers.
"""

SMALL_TALK_DESC = """
hello, hi, hey, greetings, thanks, thank you, goodbye, bye, casual conversation, 
how are you, good morning, good evening, okay, cool, awesome, yes, no.
"""
class Semantic_router:
    def __init__(self, embedding_model):
        
        self.embedding = embedding_model
        self.tech_vector = self.embedding.embed_query(TECH_DESC)
        self.casual_vector = self.embedding.embed_query(SMALL_TALK_DESC)
        self.tech_keywords = {'motor', 'sensor', 'voltage', 'current', 'pid', 'arduino', 'esp32',
                            'code', 'python', 'kinematics', 'robot', 'circuit', 'power', 'torque',
                            'signal', 'pwm', 'servo', 'actuator', 'microcontroller', 'resistor',
                            'capacitor', 'transistor', 'diode', 'feedback', 'control', 'mechatronics'}
        self.casual_keywords = {'hello', 'hi', 'hey', 'thanks', 'thank', 'bye', 'goodbye', 'ok', 'okay', 'cool'}

    @staticmethod
    def cosine_similarity(v1, v2):
        return np.dot(v1, v2)/ (np.linalg.norm(v1) * np.linalg.norm(v2))  
    
    def semantic_class(self, question:str):
        """Takes a sentence/word as an input then determines whether its a causual sentence/word or a technical one,
          returns either string 'Casual' or 'Technical' """
        

        clean_words = set(question.lower().replace('?', '').replace('.', '').replace(',', '').split())
        
       
        if clean_words.intersection(self.tech_keywords):
            return "Technical"
            
        if clean_words.intersection(self.casual_keywords) and len(clean_words) < 6:
            return "Casual"
        
        q_vector = self.embedding.embed_query(question)

        tech_score = self.cosine_similarity(q_vector, self.tech_vector)
        casual_score = self.cosine_similarity(q_vector, self.casual_vector)
      

      
        if tech_score > casual_score :
            return "Technical"
        else:
            return "Casual"
        
if __name__ == "__main__":
    embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2",
                                        model_kwargs = {"local_files_only": True, "device": "cpu"})
    router = Semantic_router(embedding_model)
    while True:
        prompt = input("query:")
        print(router.semantic_class(prompt))