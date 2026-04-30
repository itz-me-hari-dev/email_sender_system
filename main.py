from utils import load_emails
from providers.mock_provider import MockProvider
from concurrent.futures import ThreadPoolExecutor

def send_email_task(user, provider, max_retries=3):
    attempts = 0

    while attempts < max_retries:
        try:
            provider.send(user)

            print(f"[SUCCESS] {user['email']} (Attempts: {attempts + 1})")

            return {
                "email": user["email"],
                "status": "sent",
                "attempts": attempts + 1
            }

        except Exception as e:
            attempts += 1
            print(f"[RETRY {attempts}] {user['email']} - {e}")

    print(f"[FAILED] {user['email']} after {max_retries} attempts")

    return {
        "email": user["email"],
        "status": "failed",
        "attempts": max_retries
    }

def main():
    users = load_emails("data.csv")
    print(f"Total users: {len(users)}")
    provider = MockProvider()

    futures = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        for user in users:
            future = executor.submit(send_email_task, user, provider, 3)
            futures.append(future)

    results = []
    for future in futures:
        results.append(future.result())

    print("\nFinal Results:", results)

if __name__ == "__main__":
    main()