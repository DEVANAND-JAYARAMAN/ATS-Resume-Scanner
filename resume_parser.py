import PyPDF2
import docx
import re
import nltk
from textblob import TextBlob
import spacy

class ResumeParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            self.nlp = None
        
        # Download required NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            pass
    
    def parse_resume(self, file):
        """Extract text and parse resume content"""
        text = self._extract_text(file)
        
        return {
            'name': self._extract_name(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'text': text
        }
    
    def _extract_text(self, file):
        """Extract text from uploaded file"""
        text = ""
        
        if file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        
        else:  # txt file
            text = str(file.read(), "utf-8")
        
        return text
    
    def _extract_name(self, text):
        """Extract candidate name"""
        lines = text.split('\n')
        # Assume name is in first few lines
        for line in lines[:3]:
            line = line.strip()
            if len(line.split()) >= 2 and len(line) < 50:
                return line
        return "Name not found"
    
    def _extract_email(self, text):
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else "Email not found"
    
    def _extract_phone(self, text):
        """Extract phone number"""
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else "Phone not found"
    
    def _extract_skills(self, text):
        """Extract skills from resume"""
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'node.js',
            'sql', 'mongodb', 'aws', 'azure', 'docker', 'kubernetes',
            'machine learning', 'data science', 'artificial intelligence',
            'project management', 'agile', 'scrum', 'git', 'html', 'css'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_experience(self, text):
        """Extract work experience"""
        exp_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'experience\s*:?\s*(\d+)\s*(?:years?|yrs?)',
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return f"{match.group(1)} years"
        
        return "Experience not specified"
    
    def _extract_education(self, text):
        """Extract education information"""
        education_keywords = [
            'bachelor', 'master', 'phd', 'degree', 'university',
            'college', 'institute', 'b.tech', 'm.tech', 'mba'
        ]
        
        text_lower = text.lower()
        education = []
        
        for keyword in education_keywords:
            if keyword in text_lower:
                education.append(keyword)
        
        return education if education else ["Education not specified"]