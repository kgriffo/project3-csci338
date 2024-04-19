set -e # if any of the commands fail, the overall script fails
poetry run black --check *.py
poetry run isort --check *.py
poetry run flake8 *.py
echo "Everything looks good"