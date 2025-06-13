import uvicorn 
from api import app

from config import load_config

if __name__ == "__main__":
    load_config()
    uvicorn.run("main:app", reload=True, host='0.0.0.0')
