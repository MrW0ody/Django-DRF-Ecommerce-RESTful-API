# Commands

## Creating and updating schema for api
        python manage.py spectacular --file schema.yaml

## Updating file requirements.txt
        pip freeze > requirements.txt 

## Run coverage
        coverage run -m pytest

## Run coverage in terminal
        pytest --cov