import sys
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

INTEL_AVAILABLE = False

try:
    import daal4py as d4p
    from sklearnex import patch_sklearn
    patch_sklearn()
    INTEL_AVAILABLE = True
except ImportError:
    pass

class CourseProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.kmeans = None
        self._initialize_clustering()

    def _initialize_clustering(self):
        try:
            if INTEL_AVAILABLE:
                self.kmeans_init = d4p.kmeans_init(5, method="randomDense")
                self.kmeans = lambda data: d4p.kmeans(5).compute(data, self.kmeans_init.compute(data))
                print("Using Intel oneAPI optimizations", file=sys.stderr)
            else:
                raise ImportError("Intel oneAPI not available")
        except Exception as e:
            print(f"Falling back to standard scikit-learn: {str(e)}", file=sys.stderr)
            self.kmeans = KMeans(n_clusters=5, random_state=42)

    def process_request(self, data):
        try:
            main_topic = data.get('main_topic', '')
            subtopics = data.get('subtopics', [])
            num_topics = int(data.get('num_topics', 5))
            
            return self._generate_course_structure(main_topic, subtopics, num_topics)
        except Exception as e:
            print(f"Error processing request: {str(e)}", file=sys.stderr)
            return self._generate_simple_structure(main_topic, num_topics)

    def _generate_course_structure(self, main_topic, subtopics, num_topics):
        try:
            if len(subtopics) >= 3:
                all_topics = [main_topic] + subtopics
                vectors = self.vectorizer.fit_transform([t.lower() for t in all_topics]).toarray()
                
                if len(vectors) >= 5:
                    if INTEL_AVAILABLE:
                        result = self.kmeans(vectors)
                    else:
                        self.kmeans.fit(vectors)
        except Exception as e:
            print(f"Clustering failed, using simple structure: {str(e)}", file=sys.stderr)
        
        return self._generate_structure(main_topic, subtopics, num_topics)

    def _generate_structure(self, main_topic, subtopics, num_topics):
        course_structure = {
            "title": main_topic,
            "topics": []
        }
        
        for i in range(num_topics):
            topic = {
                "title": f"Module {i+1}: {subtopics[i] if i < len(subtopics) else 'Additional Topic'}",
                "subtopics": [
                    {
                        "title": f"Lesson {j+1}",
                        "content_type": "theory"
                    } for j in range(3)
                ]
            }
            course_structure["topics"].append(topic)
        
        return course_structure

    def _generate_simple_structure(self, main_topic, num_topics):
        return self._generate_structure(main_topic, [], num_topics)

def process_input():
    processor = CourseProcessor()
    for line in sys.stdin:
        try:
            data = json.loads(line)
            result = processor.process_request(data)
            print(json.dumps(result))
            sys.stdout.flush()
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON input"}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == '__main__':
    process_input()