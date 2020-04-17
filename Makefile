init:
    pip install -r requirements.txt
test :
    py.test tests
    curl -v localhost:8000
    http localhost:8000
