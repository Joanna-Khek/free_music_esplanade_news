import schedule
import time
import subprocess


def job():
    subprocess.call("python main.py", shell=True)


if __name__ == "__main__":
    print("Scheduler...")
    schedule.every().day.at("10:00").do(job)

    while 1:
        schedule.run_pending()
        time.sleep(1)
