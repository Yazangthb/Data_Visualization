import csv
import json
import time
import requests
from datetime import datetime

# Configuration: note that in Docker Compose the service name "server" resolves to the Flask server container.
SERVER_URL = "http://server:5000/data"
CSV_FILE = "packages.csv"

def send_package(package):
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(SERVER_URL, data=json.dumps(package), headers=headers)
        if response.status_code != 200:
            print("Error sending package:", response.text)
        else:
            print("Package sent:", package)
    except Exception as e:
        print("Exception sending package:", e)

def main():
    packages = []
    # Read the CSV file and convert each row into a dictionary.
    with open(CSV_FILE, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pkg = {}
            pkg["ip"] = row["ip address"]
            pkg["latitude"] = float(row["Latitude"])
            pkg["longitude"] = float(row["Longitude"])
            # Convert the Unix epoch (provided as string) into a datetime object.
            pkg_timestamp = int(row["Timestamp"])
            pkg["timestamp"] = datetime.fromtimestamp(pkg_timestamp)
            # Convert suspicious into an integer: 0 or 1.
            pkg["suspicious"] = int(float(row["suspicious"]))
            packages.append(pkg)

    if not packages:
        print("No packages found in CSV!")
        return

    # Use the first package’s timestamp as the reference.
    ref_time = packages[0]["timestamp"]
    for pkg in packages:
        # Calculate delay based on the timestamp difference.
        delay = (pkg["timestamp"] - ref_time).total_seconds()
        if delay > 0:
            print(f"Sleeping for {delay} seconds...")
            time.sleep(delay)
        # Update reference time to the current package’s timestamp.
        ref_time = pkg["timestamp"]

        # Convert datetime back to string in ISO format for JSON serialization.
        pkg_to_send = {
            "ip": pkg["ip"],
            "latitude": pkg["latitude"],
            "longitude": pkg["longitude"],
            "timestamp": pkg["timestamp"].isoformat(),
            "suspicious": pkg["suspicious"]
        }
        send_package(pkg_to_send)

if __name__ == "__main__":
    main()
