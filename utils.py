import csv

def load_emails(file_path):
    emails = []

    with open(file_path, newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            emails.append(row['email'])

    return emails