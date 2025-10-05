# ATS Resume Scanner
## AI-Powered Intelligent Recruitment System

### Features
- **Resume Parsing**: Extract text from PDF, DOCX, and TXT files
- **ATS Scoring**: Intelligent scoring based on keyword matching, skills, experience, and education
- **Job Matching**: Find candidates matching specific job requirements
- **Analytics Dashboard**: View recruitment statistics and score distributions
- **Database Management**: Store and manage candidate data

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy model:
```bash
pip -m spacy download en_core_web_sm
```

### Usage

Run the application:
```bash
streamlit run app.py
```

### System Components

1. **Resume Parser** (`resume_parser.py`)
   - Extracts text from various file formats
   - Identifies name, email, phone, skills, experience, and education

2. **ATS Scorer** (`ats_scorer.py`)
   - Calculates comprehensive ATS scores
   - Uses TF-IDF and cosine similarity for keyword matching
   - Evaluates skills, experience, and education relevance

3. **Database** (`database.py`)
   - SQLite database for storing resume data
   - Analytics and reporting functions

4. **Main Application** (`app.py`)
   - Streamlit web interface
   - Multi-page navigation
   - Interactive dashboards

### Scoring Algorithm

The ATS score is calculated using weighted components:
- **Keyword Matching (40%)**: TF-IDF cosine similarity
- **Skills Matching (30%)**: Direct skill keyword matching
- **Experience Relevance (20%)**: Years of experience evaluation
- **Education Relevance (10%)**: Educational background matching

### Pages

1. **Upload Resume**: Upload and analyze individual resumes
2. **Job Matching**: Find candidates matching job descriptions
3. **Analytics**: View recruitment statistics and trends
4. **Database**: Manage stored resume data
