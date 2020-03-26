find . -name "__pycache__" | xargs rm -rf
find . -name "*.csv" | xargs rm
find . -name "*.pyc" | xargs rm
