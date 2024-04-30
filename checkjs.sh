set -e # if any of the commands fail, the overall script fails
poetry run black --check *.jsx
poetry run isort --check *.jsx
poetry run flake8 *.jsx
echo "Everything looks good"