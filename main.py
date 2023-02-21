import uvicorn
from fastapi import FastAPI
from app.api.api import api_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.api.endpoints.staff_attendance import check_abscences
from apscheduler.triggers.cron import CronTrigger
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Management App"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


sched = BackgroundScheduler()
sched.add_job(check_abscences, CronTrigger.from_crontab("15 1 * * *"))


sched.start()
