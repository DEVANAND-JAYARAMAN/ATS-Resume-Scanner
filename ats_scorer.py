from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import nltk
from nltk.corpus import stopwords

class ATSScorer:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
    
    def calculate_score(self, resume_data, job_description):
        """Calculate comprehensive ATS score"""
        scores = {}
        
        # Keyword matching score (40%)
        scores['keyword_score'] = self._keyword_matching_score(
            resume_data['text'], job_description
        ) * 0.4
        
        # Skills matching score (30%)
        scores['skills_score'] = self._skills_matching_score(
            resume_data['skills'], job_description
        ) * 0.3
        
        # Experience relevance score (20%)
        scores['experience_score'] = self._experience_score(
            resume_data['experience'], job_description
        ) * 0.2
        
        # Education relevance score (10%)
        scores['education_score'] = self._education_score(
            resume_data['education'], job_description
        ) * 0.1
        
        # Calculate total score
        scores['total_score'] = sum(scores.values())
        
        return scores
    
    def _keyword_matching_score(self, resume_text, job_description):
        """Calculate keyword matching using TF-IDF and cosine similarity"""
        try:
            # Preprocess texts
            resume_clean = self._preprocess_text(resume_text)
            job_clean = self._preprocess_text(job_description)
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([resume_clean, job_clean])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return similarity * 100
        except:
            return 0
    
    def _skills_matching_score(self, resume_skills, job_description):
        """Calculate skills matching score"""
        if not resume_skills:
            return 0
        
        job_description_lower = job_description.lower()
        matched_skills = 0
        
        for skill in resume_skills:
            if skill.lower() in job_description_lower:
                matched_skills += 1
        
        return (matched_skills / len(resume_skills)) * 100 if resume_skills else 0
    
    def _experience_score(self, experience, job_description):
        """Calculate experience relevance score"""
        # Extract required experience from job description
        exp_patterns = [
            r'(\d+)\s*(?:\+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'minimum\s*(\d+)\s*(?:years?|yrs?)',
            r'at least\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        required_exp = 0
        for pattern in exp_patterns:
            match = re.search(pattern, job_description.lower())
            if match:
                required_exp = int(match.group(1))
                break
        
        # Extract candidate experience
        candidate_exp = 0
        if isinstance(experience, str):
            exp_match = re.search(r'(\d+)', experience)
            if exp_match:
                candidate_exp = int(exp_match.group(1))
        
        # Score based on experience match
        if required_exp == 0:
            return 80  # No specific requirement
        elif candidate_exp >= required_exp:
            return 100
        elif candidate_exp >= required_exp * 0.8:
            return 80
        elif candidate_exp >= required_exp * 0.6:
            return 60
        else:
            return 30
    
    def _education_score(self, education, job_description):
        """Calculate education relevance score"""
        if not education:
            return 50
        
        job_description_lower = job_description.lower()
        education_keywords = [
            'bachelor', 'master', 'phd', 'degree', 'university',
            'college', 'b.tech', 'm.tech', 'mba', 'engineering'
        ]
        
        # Check if job requires specific education
        requires_education = any(keyword in job_description_lower 
                               for keyword in education_keywords)
        
        if not requires_education:
            return 80  # No specific education requirement
        
        # Check education match
        education_str = ' '.join(education).lower()
        matches = sum(1 for keyword in education_keywords 
                     if keyword in education_str and keyword in job_description_lower)
        
        return min(100, matches * 25 + 50)
    
    def _preprocess_text(self, text):
        """Clean and preprocess text"""
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text