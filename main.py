from utils import load_emails
from providers.mock_provider import MockProvider
from concurrent.futures import ThreadPoolExecutor
from db import init_db, save_result, clear_table
import time


def send_email_task(user, provider, max_retries=3):
    attempts = 0

    while attempts < max_retries:
        try:
            provider.send(user)
            return {
                "email": user["email"],
                "status": "sent",
                "attempts": attempts + 1
            }
        except Exception:
            attempts += 1

    return {
        "email": user["email"],
        "status": "failed",
        "attempts": max_retries
    }


def main():

    # Initialize database and clear previous logs
    init_db()

    # Clear previous logs for a fresh start
    clear_table()

    users = load_emails("data.csv")
    provider = MockProvider()

    print("Starting email sending...\n")

    start_time = time.time()

    futures = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        for user in users:
            future = executor.submit(send_email_task, user, provider, 3)
            futures.append(future)

    results = []

    for future in futures:
        result = future.result()
        results.append(result)
        save_result(result)

    end_time = time.time()

    # Summary
    total = len(results)
    sent = sum(1 for r in results if r["status"] == "sent")
    failed = sum(1 for r in results if r["status"] == "failed")
    time_taken = end_time - start_time

    print("\n===== SUMMARY =====")
    print(f"Total Emails: {total}")
    print(f"Sent: {sent}")
    print(f"Failed: {failed}")
    print(f"Time Taken: {time_taken:.2f} seconds")


if __name__ == "__main__":
    main()