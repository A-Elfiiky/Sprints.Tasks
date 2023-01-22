import csv
import boto3
import datetime

# initialize an empty list to store phonebook entries
phonebook = []

# create an S3 client
s3 = boto3.client('s3')

# function to add new entry to phonebook
def add_entry():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")
    address = input("Enter address: ")
    entry = {"name": name, "phone": phone, "email": email, "address": address}
    phonebook.append(entry)
    export_csv()
    print("Entry added.")

# function to update existing entry in phonebook
def update_entry():
    name = input("Enter name of entry to update: ")
    for entry in phonebook:
        if entry["name"] == name:
            entry["phone"] = input("Enter new phone number: ")
            entry["email"] = input("Enter new email: ")
            entry["address"] = input("Enter new address: ")
            export_csv()
            print("Entry updated.")
            return
    print("Entry not found.")

# function to delete existing entry in phonebook
def delete_entry():
    name = input("Enter name of entry to delete: ")
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
        writer = csv.DictWriter(file, fieldnames=["name", "phone", "email", "address"])
        writer.writeheader()
        for entry in phonebook:
            writer.writerow(entry)
    print(f"Phonebook exported to {filename}.")

# function to backup phonebook to S3 bucket
def backup_to_aws(bucket_name, file_path):
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"phonebook_{date}.csv"
    try:
        s3.upload_file(filename, bucket_name, f"{file_path}/{filename}")
        print(f"Phonebook backed up to S3.")
    except Exception as e:
        print(f"An error occurred while backing up to S3: {e}")

# function to backup phonebook to local storage
def backup_to_local(file_path):
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{file_path}/phonebook_{date}.csv"
    try:
        with open(filename, "w") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "email", "address"])
            writer.writeheader()
            for entry in phonebook:
                writer.writerow(entry)
        print(f"Phonebook backed up to {file_path}.")
    except Exception as e:
        print(f"An error occurred while backing up to {file_path}: {e}")

# main loop
while True:
    print("1. Add entry")
    print("2. Update entry")
    print("3. Delete entry")
    print("4. Export to CSV")
    print("5. Backup to AWS")
    print("6. Backup to Local")
    print("7. Exit")
    choice = input("Enter choice: ")
    if choice == "1":
        add_entry()
    elif choice == "2":
        update_entry()
    elif choice == "3":
        delete_entry()
    elif choice == "4":
        export_csv()
    elif choice == "5":
        bucket_name = input("Enter S3 bucket name: ")
        file_path = input("Enter file path in S3 bucket: ")
        backup_to_aws(bucket_name, file_path)
    elif choice == "6":
        file_path = input("Enter local file path: ")
        backup_to_local(file_path)
    elif choice == "7":
        break
    else:
        print("Invalid choice.")

# automatically save the data to csv file after input
export_csv()

