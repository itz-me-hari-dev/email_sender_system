from utils import load_emails

def main():
    emails = load_emails("data.csv")
    print("Loaded Emails:", emails)

if __name__ == "__main__":
    main()