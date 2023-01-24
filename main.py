import uvicorn
from fastapi import FastAPI
from app.api.api import api_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.api.endpoints.staff import check_abscences
from apscheduler.triggers.cron import CronTrigger


app = FastAPI(
    title="Management App"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


sched = BackgroundScheduler({'apscheduler.timezone': 'Asia/Kolkata'})
sched.add_job(check_abscences, CronTrigger.from_crontab("15 1 * * *"))

sched.start()
