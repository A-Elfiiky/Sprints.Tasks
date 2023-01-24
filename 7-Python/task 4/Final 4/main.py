import csv
import boto3
import datetime
from datetime import timedelta
from pathlib import Path
from typing import List

# initialize an empty list to store phonebook entries
phonebook = []

# create an S3 client
s3 = boto3.client('s3')

# function to add new entry to phonebook with input validation
def add_entry():
    while True:
        name = input("Enter name (only letters): ")
        if name.isalpha():
            break
        print("Invalid input. Please enter only letters.")

    while True:
        phone = input("Enter phone number (11 numbers starting with 01): ")
        if phone.startswith("01") and len(phone) == 11 and phone.isnumeric():
            break
        print("Invalid input. Please enter a valid phone number.")

    while True:
        email = input("Enter email: ")
        if "@" in email:
            break
        print("Invalid input. Please enter a valid email.")

    address = input("Enter address: ")
    entry = {"name": name, "phone": phone, "email": email, "address": address, "date": datetime.datetime.now()}
    phonebook.append(entry)
    export_csv()
    print("Entry added.")

# function to update existing entry in phonebook
def update_entry(name: str, phone: str, email: str, address: str):
    for entry in phonebook:
        if entry["name"] == name:
            entry["phone"] = phone
            entry["email"] = email
            entry["address"] = address
            entry["date"] = datetime.datetime.now()
            export_csv()
            print("Entry updated.")
            return
    print("Entry not found.")

# function to delete existing entry in phonebook
def delete_entry(name: str):
    for entry in phonebook:
        if entry["name"] == name:
            phonebook.remove(entry)
            export_csv()
            print("Entry deleted.")
            return
    print("Entry not found.")

# function to export phonebook to CSV file
def export_csv():
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"phonebook_{date}.csv"
    with open(filename, "w") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "phone", "email", "address", "date"])
        writer.writeheader()
        for entry in phonebook:
            writer.writerow(entry)
    print(f"Phonebook exported to {filename}.")
    backup_to_aws(filename)
    backup_to_local(filename)

# function to backup phonebook to S3 bucket
def backup_to_aws(filename: str):
    try:
        s3.upload_file(filename, "my-phonebook-bucket", f"backups/{filename}")
        print(f"Phonebook backed up to S3.")
    except Exception as e:
        print(f"An error occurred while backing up to S3: {e}")

# function to backup phonebook to local storage
def backup_to_local(filename: str):
    try:
        Path("backups").mkdir(parents=True, exist_ok=True)
        with open(f"backups/{filename}", "w") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "email", "address", "date"])
            writer.writeheader()
            for entry in phonebook:
                writer.writerow(entry)
        print(f"Phonebook backed up to local storage.")
    except Exception as e:
        print(f"An error occurred while backing up to local storage: {e}")

# function to view the phonebook and sort by user's choice
def view_phonebook(sort_by: str):
    if sort_by == "alpha":
        phonebook.sort(key=lambda entry: entry["name"])
    elif sort_by == "date":
        phonebook.sort(key=lambda entry: entry["date"])
    else:
        print("Invalid sorting method.")
        return

    for entry in phonebook:
        print(f"Name: {entry['name']}\nPhone: {entry['phone']}\nEmail: {entry['email']}\nAddress: {entry['address']}\nDate: {entry['date']}\n")

# function to merge from old CSV file
def merge_from_csv(filename: str):
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                phonebook.append(row)
        print(f"Successfully merged data from {filename}.")
    except Exception as e:
        print(f"An error occurred while merging data from {filename}: {e}")

# function to search for an entry and update if found
def search_and_update(name: str):
    for entry in phonebook:
        if entry["name"] == name:
            while True:
                phone = input("Enter new phone number (11 numbers starting with 01): ")
                if phone.startswith("01") and len(phone) == 11 and phone.isnumeric():
                    break
                print("Invalid input. Please enter a valid phone number.")

            while True:
                email = input("Enter new email: ")
                if "@" in email:
                    break
                print("Invalid input. Please enter a valid email.")

            address = input("Enter new address: ")
            update_entry(name, phone, email, address)
            return
    print("Entry not found.")

# Schedule backups to run every day
def schedule_backups():
    while True:
        export_csv()
        time.sleep(60*60*24)

# main loop
while True:
    print("1. Add entry")
    print("2. Update entry")
    print("3. Delete entry")
    print("4. Export to CSV")
    print("5. View phonebook")
    print("6. Merge from CSV")
    print("7. Search and update entry")
    print("8. Schedule backups")
    print("9. Exit")
    choice = input("Enter choice: ")
    if choice == "1":
        add_entry()
    elif choice == "2":
        name = input("Enter name of entry to update: ")
        search_and_update(name)
    elif choice == "3":
        name = input("Enter name of entry to delete: ")
        delete_entry(name)
    elif choice == "4":
        export_csv()
    elif choice == "5":
        sort_by = input("Enter sorting method (alpha or date): ")
        view_phonebook(sort_by)
    elif choice == "6":
        filename = input("Enter the name of the CSV file to merge from: ")
        merge_from_csv(filename)
    elif choice == "7":
        name = input("Enter the name of the entry to search for: ")
        search_and_update(name)
    elif choice == "8":
        schedule_backups()
    elif choice == "9":
        break
    else:
        print("Invalid choice. Please enter a valid number.")
