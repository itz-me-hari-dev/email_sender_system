from utils import load_emails
from providers.mock_provider import MockProvider
from providers.mailgun_provider import MailgunProvider
from email_sender import run_sequential, run_threaded
from db import init_db, clear_table


# Configuration
DEFAULT_MODE = "mock"   # "mock" or "mailgun"
MAILGUN_TEST_FILE = "mailgun_test.csv"
MAILGUN_EMAIL_LIMIT = 5


def select_mode():
    print("Select email provider:")
    print("1. Mock")
    print("2. Mailgun")

    choice = input(f"Enter choice [1/2] (default: {DEFAULT_MODE}): ").strip().lower()

    if choice in ("", DEFAULT_MODE):
        return DEFAULT_MODE
    if choice in ("1", "mock"):
        return "mock"
    if choice in ("2", "mailgun"):
        return "mailgun"

    raise ValueError("Invalid choice. Use 1 for mock or 2 for mailgun.")


def main():
    init_db()
    mode = select_mode()

    # Provider selection
    if mode == "mock":
        provider = MockProvider()
        users = load_emails("data.csv")
    elif mode == "mailgun":
        provider = MailgunProvider()
        users = load_emails(MAILGUN_TEST_FILE)[:MAILGUN_EMAIL_LIMIT]
    else:
        raise ValueError("Invalid mode. Use 'mock' or 'mailgun'.")

    # Sequential run (only for mock mode)
    if mode == "mock":
        print("Running SEQUENTIAL...\n")
        clear_table()
        _, seq_time = run_sequential(users, provider)
    else:
        seq_time = None

    # Threaded run
    print("Running THREADED...\n")
    clear_table()
    results, thread_time = run_threaded(users, provider)

    # Summary
    total = len(results)
    sent = sum(1 for r in results if r["status"] == "sent")
    failed = sum(1 for r in results if r["status"] == "failed")

    print("\n===== PERFORMANCE COMPARISON =====")
    if seq_time is not None:
        print(f"Sequential Time: {seq_time:.2f} sec")
    print(f"Threaded Time:   {thread_time:.2f} sec")

    print("\n===== SUMMARY =====")
    print(f"Total Emails: {total}")
    print(f"Sent: {sent}")
    print(f"Failed: {failed}")
    print(f"Time Taken: {thread_time:.2f} sec")

    errors = [r for r in results if r["status"] == "failed"]

    if errors:
        print("\n===== ERRORS =====")
        for e in errors[:10]:
            print(f"{e['email']}: {e.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
