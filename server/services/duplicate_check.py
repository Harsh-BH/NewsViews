from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from models.news import NewsSubmission, ProcessedSubmission
from typing import List, Tuple, Optional

class DuplicateCheckService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def check_for_duplicate(
        self, 
        new_submission: NewsSubmission, 
        existing_submissions: List[ProcessedSubmission],
        threshold: float = 0.8
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if a submission is too similar to existing submissions.
        Returns (is_duplicate, duplicate_id)
        """
        if not existing_submissions:
            return False, None
            
        # Combine title and description for better comparison
        new_text = f"{new_submission.news_title} {new_submission.news_description}"
        
        # Extract text from existing submissions
        existing_texts = []
        for submission in existing_submissions:
            text = f"{submission.news_title} {submission.news_description}"
            existing_texts.append(text)
        
        # If there are no existing texts, return False
        if not existing_texts:
            return False, None
            
        # Create TF-IDF matrix
        try:
            all_texts = existing_texts + [new_text]
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            
            # Calculate cosine similarity between the new submission and all existing ones
            similarity_scores = cosine_similarity(
                tfidf_matrix[-1:],  # New submission (last row)
                tfidf_matrix[:-1]   # All existing submissions
            )[0]
            
            # Find the highest similarity score and check if it exceeds threshold
            max_similarity = np.max(similarity_scores)
            if max_similarity >= threshold:
                most_similar_idx = np.argmax(similarity_scores)
                duplicate_id = existing_submissions[most_similar_idx].id
                return True, duplicate_id
                
            return False, None
            
        except Exception as e:
            print(f"Error during duplicate check: {str(e)}")
            # In case of an error, allow the submission to proceed
            return False, None
