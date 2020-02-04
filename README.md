Install: pip install -r requirements.txt 

Testing: python server.py
Production: gunicorn --bind 0.0.0.0:8080 wsgi:app --timeout 10 --max-requests 150 -w 2