import pandas as pd
from datetime import datetime

from src.email_sender import send_email
from src.report_generator import generate_report
from src.logger import logger

contacts = pd.read_csv("data/contacts.csv")

reminders = pd.read_csv("data/reminders.csv")

with open("templates/reminder_template.txt", "r") as file:

    template = file.read()

results = []

for _, reminder in reminders.iterrows():

    name = reminder["name"]

    contact = contacts[contacts["name"] == name]

    if contact.empty:

        logger.error(f"No contact found for {name}")

        continue

    email = contact.iloc[0]["email"]

    body = template.format(
        name=name,
        task=reminder["task"],
        date=reminder["date"]
    )

    status = send_email(
        email,
        "Reminder Notification",
        body
    )

    results.append({
        "name": name,
        "email": email,
        "task": reminder["task"],
        "status": status,
        "timestamp": datetime.now()
    })

generate_report(results)

print("Automation completed.")