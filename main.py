from fastapi import FastAPI
import appPokeList

app = FastAPI()
appPokeList.init(app)