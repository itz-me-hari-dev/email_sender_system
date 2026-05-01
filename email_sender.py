from concurrent.futures import ThreadPoolExecutor
import time

from db import save_result


def send_email_task(user, provider, max_retries=3):
    attempts = 0
    last_error = ""

    while attempts < max_retries:
        try:
            provider.send(user)
            return {
                "email": user["email"],
                "status": "sent",
                "attempts": attempts + 1
            }
        except Exception as error:
            last_error = str(error)
            attempts += 1

    return {
        "email": user["email"],
        "status": "failed",
        "attempts": max_retries,
        "error": last_error
    }


def run_sequential(users, provider):
    results = []
    start_time = time.time()

    for user in users:
        result = send_email_task(user, provider, 3)
        results.append(result)
        save_result(result)

    end_time = time.time()
    return results, end_time - start_time


def run_threaded(users, provider):
    results = []
    futures = []

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for user in users:
            futures.append(executor.submit(send_email_task, user, provider, 3))

    for future in futures:
        result = future.result()
        results.append(result)
        save_result(result)

    end_time = time.time()
    return results, end_time - start_time
