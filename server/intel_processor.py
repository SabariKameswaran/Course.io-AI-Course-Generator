from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import daal4py as d4p
from sklearnex import patch_sklearn
import intel_extension_for_pytorch as ipex
import torch
from transformers import AutoTokenizer, AutoModel

patch_sklearn()

app = Flask(__name__)
CORS(app)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")
model = ipex.optimize(model)

class IntelOptimizedProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.kmeans = d4p.kmeans(n_clusters=5)
    
    def generate_embeddings(self, texts):
        with torch.no_grad():
            inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy()
    
    def process_request(self, data):
        main_topic = data['main_topic']
        subtopics = data['subtopics']
        num_topics = int(data['num_topics'])
        
        all_topics = [main_topic] + subtopics
        embeddings = self.generate_embeddings(all_topics)
        
        clusters = self.kmeans.compute(embeddings).centroids
        
        return self._generate_course_structure(main_topic, subtopics, num_topics, clusters)
    
    def _generate_course_structure(self, main_topic, subtopics, num_topics, clusters):
        course_structure = {
            main_topic.lower(): []
        }
        
        for i in range(num_topics):
            topic = {
                "title": f"Topic {i+1}",
                "subtopics": []
            }
            
            for j in range(3):
                subtopic = {
                    "title": subtopics[j] if j < len(subtopics) else f"Generated Subtopic {j+1}",
                    "theory": "",
                    "youtube": "",
                    "image": "",
                    "done": False
                }
                topic["subtopics"].append(subtopic)
            
            course_structure[main_topic.lower()].append(topic)
        
        return course_structure

processor = IntelOptimizedProcessor()

@app.route('/api/prompt', methods=['POST'])
def process_prompt():
    try:
        data = request.json
        prompt_data = json.loads(data['prompt'])
        
        result = processor.process_request(prompt_data)
        
        return jsonify({
            "success": True,
            "generatedText": json.dumps(result)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(port=5001)