@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo Starting ATS Resume Scanner...
streamlit run app.py

pause