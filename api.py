from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

RAZORPAY_IFSC_BASE_URL = "https://ifsc.razorpay.com"


@app.route("/", methods=["GET"])
def home():
    # Simple info route
    return jsonify({
        "message": "IFSC Bank Info API by @Kalyug_present",
        "usage": "/ifsc?code=HDFC0000314"
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

        # Basic validation (11 chars, 5th char 0)
        if len(ifsc) != 11:
            return jsonify({
                "success": False,
                "credit": "@Kalyug_present",
                "error": "Invalid IFSC format. It must be 11 characters."
            }), 400

        # Call Razorpay IFSC API
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
            # Razorpay 404 etc.
            return jsonify({
                "success": False,
                "credit": "@Kalyug_present",
                "error": "IFSC not found or invalid."
            }), 404

        data = r.json()

        # Ensure all expected keys exist (fill with None if missing)
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


# Local testing only – Vercel itsko ignore kar dega
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
