## Install dependency
```bash
pip install -r requirments
```

## Setting database 
.env file in folder app/system   

## Run
```bash
uvicorn app.system.main:app  --port 8000
```

This will expose fastapi application on port 8000

swagger docs - `http://localhost:8000/docs`

redoc - `http://localhost:8000/redoc`

websocket - `http://localhost:8000/ws/{room_id}/{user_id}`


## Running Unit Test
```bash
pytest -v
```