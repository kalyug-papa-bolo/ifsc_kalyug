from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Your API token (keep it secret!)
API_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI4NDU3ODI5OTQzIiwianRpIjoiMWEyYTFiOTUtZDJjMS00ZWM5LWI2YmYtNGNjODc5MmVkNmRmIiwiZXhwIjoxNzkxODI1MzU5fQ.izINTakx7ySw9Lj5szrebi2gYTsxYR1Z09-N3p33DWNp-Dga8haGdbYeEsFUwteW3i8mPI8CcMSgBf7AH3lxxZ-M3s-_7IafGWZ4FyvW82o19hnm_CZTEgYbbv4KzEl5e0GUsIbRRFy-9RxJebzWn41_0sMjmRIDTzDCEWO_Wbk"

# Copyright-style username
USERNAME = "© @Kalyug_present"

@app.route("/")
def home():
    return jsonify({
        "message": "Oye, kya dekh raha hai? 😏 Ye API chori karne ka nahi hai!",
        "warning": "© @Kalyug_present ka data hai, respect dena zaroori hai 🤚",
        "note": "Stats dekhna hai toh /user/user_id use karo. Chill maro 😎",
        "example_user_id": 8457829943
    })

@app.route("/user/<int:user_id>")
def get_user_stats(user_id):
    url = f"https://funstat.info/api/v1/users/{user_id}/stats_min"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        data["DEVLOPER 👉🏻"] = USERNAME
        return jsonify(data)
    else:
        return jsonify({
            "error": f"Request failed with status code {response.status_code}",
            "DEVLOPER 👉🏻": USERNAME
        }), response.status_code


# Local test ke liye; Vercel isko ignore kar deta hai
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
