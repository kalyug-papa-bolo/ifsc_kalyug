from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

RAZORPAY_IFSC_BASE_URL = "https://ifsc.razorpay.com"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "IFSC Bank Info API by @Kalyug_present",
        "usage": "/ifsc?code=HDFC0000314",
        "credit": "@Kalyug_present"
    })


@app.route("/ifsc", methods=["GET"])
def ifsc_lookup():
    try:
        ifsc = request.args.get("code", "").strip().upper()

        if not ifsc:
            return jsonify({
                "success": False,
                "credit": "@Kalyug_present",
                "error": "IFSC code (code) parameter is required."
            }), 400

        if len(ifsc) != 11:
            return jsonify({
                "success": False,
                "credit": "@Kalyug_present",
                "error": "Invalid IFSC format. It must be 11 characters."
            }), 400

        url = f"{RAZORPAY_IFSC_BASE_URL}/{ifsc}"

        try:
            r = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            return jsonify({
                "success": False,
                "credit": "@Kalyug_present",
                "error": f"Upstream IFSC service error: {str(e)}"
            }), 502

        if r.status_code != 200:
            return jsonify({
                "success": False,
                "credit": "@Kalyug_present",
                "error": "IFSC not found or invalid."
            }), 404

        data = r.json()

        keys = [
            "BRANCH", "ADDRESS", "STATE", "MICR", "CONTACT",
            "UPI", "RTGS", "CITY", "CENTRE", "DISTRICT",
            "NEFT", "IMPS", "SWIFT", "ISO3166",
            "BANK", "BANKCODE", "IFSC"
        ]
        cleaned = {k: data.get(k) for k in keys}

        return jsonify({
            "success": True,
            "credit": "@Kalyug_present",
            "ifsc_details": cleaned
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "credit": "@Kalyug_present",
            "error": f"Unexpected server error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

