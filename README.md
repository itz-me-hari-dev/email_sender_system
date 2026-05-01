# Multi-threaded Email Sending System

A simple Python CLI project for sending emails to multiple users using either a mock email provider or the Mailgun API. The system reads users from CSV files, sends emails with retry support, stores results in SQLite, and compares sequential vs threaded performance in mock mode.

## Features

- Read users from CSV with `name` and `email` columns
- Send emails using `MockProvider` for simulated sending
- Send real emails using `MailgunProvider`
- Use `ThreadPoolExecutor` for multithreaded sending
- Retry failed sends up to 3 attempts
- Store send results in SQLite
- Print total emails, sent count, failed count, and time taken
- Show sequential vs threaded performance comparison in mock mode
- Switch between mock and Mailgun mode using configuration in `main.py`

## Project Structure

```text
project/
├── main.py
├── email_sender.py
├── providers/
│   ├── mock_provider.py
│   └── mailgun_provider.py
├── db.py
├── utils.py
├── data.csv
├── mailgun_test.csv
├── .env
└── requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd project
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

### Mock Mode

In `main.py`, set:

```python
MODE = "mock"
```

Run:

```bash
python main.py
```

Mock mode reads users from `data.csv`, simulates email sending, and shows sequential vs threaded performance.

### Mailgun Mode

In `main.py`, set:

```python
MODE = "mailgun"
```

Run:

```bash
python main.py
```

Mailgun mode reads recipients from `mailgun_test.csv` and sends only a limited number of real emails.

## Mailgun Setup

1. Create a Mailgun account.
2. Get your Mailgun API key and domain.
3. Add verified recipient email addresses in Mailgun if using a sandbox domain.
4. Create a `.env` file:

```env
MAILGUN_API_KEY=your_api_key
MAILGUN_DOMAIN=your_mailgun_domain
```

5. Add 3 to 5 verified recipients to `mailgun_test.csv`.

## Example Output

```text
Running SEQUENTIAL...

Running THREADED...

===== PERFORMANCE COMPARISON =====
Sequential Time: 131.23 sec
Threaded Time:   16.19 sec

===== SUMMARY =====
Total Emails: 500
Sent: 497
Failed: 3
Time Taken: 16.19 sec
```

## Notes

- Mock mode does not send real emails. It simulates delay and random failures.
- Mailgun mode sends real emails through the Mailgun API.
- Sandbox Mailgun domains can send only to verified recipients.
- SQLite results are stored in `emails.db`.
