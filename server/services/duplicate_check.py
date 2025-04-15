import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import NewsSubmission, DuplicateCheckResult
import config
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("services.duplicate_check")

class DuplicateChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def check_duplicate(self, new_submission: NewsSubmission, existing_submissions: list) -> DuplicateCheckResult:
        """Check if a new submission is a duplicate of any existing submission"""
        if not existing_submissions:
            logger.info("No existing submissions to compare against. Skipping duplicate check.")
            return DuplicateCheckResult(is_duplicate=False)
        
        # Extract existing descriptions
        existing_texts = [sub["description"] for sub in existing_submissions]
        
        # Add new submission text
        all_texts = existing_texts + [new_submission.description]
        
        logger.info(f"Checking for duplicates among {len(existing_texts)} existing submissions")
        
        # Generate TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        # Get the vector for the new submission (last row)
        new_submission_vector = tfidf_matrix[-1]
        
        # Compare with all existing submissions
        similarity_scores = cosine_similarity(
            new_submission_vector,
            tfidf_matrix[:-1]  # Exclude the last row (new submission)
        )[0]
        
        # Find the highest similarity score and its index
        max_similarity = max(similarity_scores) if len(similarity_scores) > 0 else 0.0
        most_similar_index = np.argmax(similarity_scores) if len(similarity_scores) > 0 else -1
        
        # Check if it exceeds the threshold
        if max_similarity >= config.DUPLICATE_THRESHOLD:
            logger.warning(f"Potential duplicate detected! Similarity score: {max_similarity:.4f}, matching entry ID: {most_similar_index}")
            return DuplicateCheckResult(
                is_duplicate=True,
                similarity_score=float(max_similarity),
                duplicate_entry_id=str(most_similar_index)  # Ensure this is a string
            )
        else:
            logger.info(f"No duplicates detected. Highest similarity score: {max_similarity:.4f}")
            return DuplicateCheckResult(is_duplicate=False)
