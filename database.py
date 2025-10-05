import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_name="ats_resumes.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                skills TEXT,
                experience TEXT,
                education TEXT,
                resume_text TEXT,
                ats_score REAL,
                keyword_score REAL,
                skills_score REAL,
                experience_score REAL,
                education_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_resume(self, resume_data, ats_score):
        """Store resume data and ATS scores"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO resumes (
                name, email, phone, skills, experience, education,
                resume_text, ats_score, keyword_score, skills_score,
                experience_score, education_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            resume_data['name'],
            resume_data['email'],
            resume_data['phone'],
            json.dumps(resume_data['skills']),
            resume_data['experience'],
            json.dumps(resume_data['education']),
            resume_data['text'],
            ats_score['total_score'],
            ats_score['keyword_score'],
            ats_score['skills_score'],
            ats_score['experience_score'],
            ats_score['education_score']
        ))
        
        conn.commit()
        conn.close()
    
    def find_matches(self, job_description, min_score):
        """Find candidates matching job requirements"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, email, phone, ats_score, skills, experience
            FROM resumes
            WHERE ats_score >= ?
            ORDER BY ats_score DESC
        ''', (min_score,))
        
        results = cursor.fetchall()
        conn.close()
        
        matches = []
        for row in results:
            matches.append({
                'Name': row[0],
                'Email': row[1],
                'Phone': row[2],
                'ATS Score': f"{row[3]:.1f}%",
                'Skills': json.loads(row[4]) if row[4] else [],
                'Experience': row[5]
            })
        
        return matches
    
    def get_analytics(self):
        """Get analytics data"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                AVG(ats_score) as avg_score,
                MAX(ats_score) as max_score
            FROM resumes
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total_resumes': result[0] or 0,
            'avg_score': result[1] or 0,
            'max_score': result[2] or 0
        }
    
    def get_score_distribution(self):
        """Get score distribution for analytics"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT ats_score FROM resumes')
        scores = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return scores
    
    def get_all_resumes(self):
        """Get all resumes for database view"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, email, phone, ats_score, created_at
            FROM resumes
            ORDER BY created_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        resumes = []
        for row in results:
            resumes.append({
                'Name': row[0],
                'Email': row[1],
                'Phone': row[2],
                'ATS Score': f"{row[3]:.1f}%",
                'Date Added': row[4]
            })
        
        return resumes
    
    def clear_database(self):
        """Clear all resume data"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM resumes')
        
        conn.commit()
        conn.close()