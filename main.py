from utils import load_emails
from providers.mock_provider import MockProvider
from providers.mailgun_provider import MailgunProvider
from concurrent.futures import ThreadPoolExecutor
from db import init_db, save_result, clear_table
import time


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


#Sequential version (no threading)
def run_sequential(users, provider):
    results = []
    start_time = time.time()

    for user in users:
        result = send_email_task(user, provider, 3)
        results.append(result)
        save_result(result)

    end_time = time.time()
    return results, end_time - start_time


# Threaded version
def run_threaded(users, provider):
    results = []
    futures = []

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for user in users:
            futures.append(
                executor.submit(send_email_task, user, provider, 3)
            )

    for future in futures:
        result = future.result()
        results.append(result)
        save_result(result)

    end_time = time.time()
    return results, end_time - start_time


def main():
    init_db()

    users = load_emails("data.csv")

    #SWITCH PROVIDER HERE
    use_mock = False   #change to False for Mailgun

    if use_mock:
        provider = MockProvider()
    else:
        provider = MailgunProvider()
        users = [
            {"name": "Fixpoint", "email": "fixpoint.noreply@gmail.com"},
            {"name": "Hari Dev", "email": "harikrishnan.mb.dev@gmail.com"},
            {"name": "Hari", "email": "harikrishnanmb36@gmail.com"}
        ]  #IMPORTANT: limit real emails

    #Run Sequential (only for mock)
    if use_mock:
        print("Running SEQUENTIAL...\n")
        clear_table()
        _, seq_time = run_sequential(users, provider)
    else:
        seq_time = 0  # not needed for Mailgun

    #Run Threaded
    print("Running THREADED...\n")
    clear_table()
    results, thread_time = run_threaded(users, provider)

    #Summary
    total = len(results)
    sent = sum(1 for r in results if r["status"] == "sent")
    failed = sum(1 for r in results if r["status"] == "failed")

    #Performance output
    print("\n===== PERFORMANCE COMPARISON =====")
    if use_mock:
        print(f"Sequential Time: {seq_time:.2f} sec")
    print(f"Threaded Time:   {thread_time:.2f} sec")

    #Final Summary
    print("\n===== SUMMARY =====")
    print(f"Total Emails: {total}")
    print(f"Sent: {sent}")
    print(f"Failed: {failed}")

    if failed:
        print("\n===== ERRORS =====")
        for result in results:
            if result["status"] == "failed":
                print(f"{result['email']}: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
