## Install dependency
```commandline
pip install -r requirments
```

## Setting database 
Setting database .env file in folder app/system   

## Run
```bash
uvicorn app.system.main:app  --port 8000
```

This will expose fastapi application on port 8000

swagger docs - `http://localhost:8000/docs`

redoc - `http://localhost:8000/redoc`


## Running Test
```commandline
pytest -v
```