from fastapi import FastAPI

def init(app:FastAPI , prefix="/api"):
	import models,database,v1,v2
	
	models.Base.metadata.create_all(bind=database.engine)

	app.include_router(v1.router, prefix=prefix+"/v1")
	app.include_router(v2.router, prefix=prefix+"/v2")