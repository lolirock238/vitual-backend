from fastapi import FastAPI
#create an instance
app = FastAPI()

#create routes to access resources.
@app.get("/")
def read_root():
    return {"Hello": "World"}