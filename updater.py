import os
from apscheduler.schedulers.blocking import BlockingScheduler
from src.http_req import get_responses
from src.database.client import Client
from src.set_proxy import run_proxy


scheduler = BlockingScheduler()


def get_update(name: str):
    run_proxy()
    db = Client()
    urls = db.list(name)
    links = get_responses(urls)
    if links:
        db.update(name, "\n".join(links))
    return links


def updater():
    get_update("share")
    get_update("v2ray")
    os.system("pkill -9 lite")


scheduler.add_job(updater, "interval", minutes=30)
scheduler.start()
