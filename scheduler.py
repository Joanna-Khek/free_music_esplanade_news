import schedule
import time
import subprocess


def job():
    subprocess.call("python main.py", shell=True)


if __name__ == "__main__":
    print("Scheduler...")
    schedule.every(1).hour.do(job)

    while 1:
        schedule.run_pending()
        time.sleep(1)
