from fastapi import FastAPI
from app.api import ping, notes
from app.db import metadata, engine, database

metadata.create_all(engine)
app = FastAPI()

'''
Startup event will run before the application starts
'''
@app.on_event("startup")
async def startup():
    # waiting for the database to start
    await database.connect()

'''
Shutdown event will run when the application is shutting down
'''
@app.on_event("shutdown")
async def shutdown():
    # wait for the database to disconnect
    await database.disconnect()

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])

