export PYTHONPATH=`readlink -f .`
#python -m unittest tests/test_passcheck_length.py
python -m unittest tests/test_passcheck_alphabet.py
