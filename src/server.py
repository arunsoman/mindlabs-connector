import os

from fastapi import FastAPI 
from routers.recharge import router as rechargeRouter
from routers.subscription import router as subscriptionRouter

print(f"running from {os.getcwd()}")
app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router( rechargeRouter)
app.include_router( subscriptionRouter)