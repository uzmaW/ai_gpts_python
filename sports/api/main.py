
from fastapi import FastAPI
from controllers import p_router, pr_router, t_router

app = FastAPI()

app.include_router(p_router)
app.include_router(pr_router)
app.include_router(t_router)

@app.get("/")
async def root():
    return {"message": "API health check successful"}

# If running from the command line, main() is called
if __name__ == "__main__":
    #main()
    pass