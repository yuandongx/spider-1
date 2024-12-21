from .app import app

@app.get('/api/list/{code}')
def list_item(code: str):
    return []