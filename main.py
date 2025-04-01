import uvicorn 
from dotenv import load_dotenv
from config import load_config
from api import app
load_dotenv()

if __name__ == "__main__":
    load_config()
    uvicorn.run("main:app", reload=True, host='0.0.0.0')
