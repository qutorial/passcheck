export PYTHONPATH=`readlink -f .`
python -m unittest `basename tests/*.py`

