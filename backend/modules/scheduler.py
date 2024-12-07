import schedule
import time
from app import collect_data
from modules.notifier import send_slack_notification

def scheduled_task():
    """
    Task to be executed on a schedule.
    """
    print("Scheduled task started.")
    data = collect_data()
    print("Data collection completed.")

    # Slack通知を送信
    send_slack_notification(
        webhook_url="https://hooks.slack.com/services/your/webhook/url",
        message="定期収集タスクが完了しました！"
    )

    # 必要であれば追加処理をここに書く
    print("Task finished.")

def start_scheduler():
    """
    Start the scheduler to run tasks at specified intervals.
    """
    # タスクを30分ごとに実行する:
     schedule.every(30).minutes.do(scheduled_task)

    print("Scheduler started. Waiting for tasks to execute...")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
