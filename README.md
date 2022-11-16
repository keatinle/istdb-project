# IST-DBM1 Project

## Pre-requisites

- Python 
- Pip packages
    - `psycopg2`
    - `pandas`
    - `pandasql`
- Makefile (optional)

## Running (with make)

### First Run
```
make first-run
```

### Subsequently
```
make run
```

## Running (without make)

### First Run

```
docker-compose up --build
python clean_data.py
```

### Subsequently

```
docker-compose up
```
