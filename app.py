from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if not OPENROUTER_API_KEY:
            return jsonify({
                "result": "Error: OPENROUTER_API_KEY not found in .env file"
            })

        data = request.json

        prompt = f"""
You are an expert B2B sales automation assistant.

Your job is to qualify inbound leads for a SaaS company.

Analyze the lead using:
- budget
- company size
- industry fit
- problem urgency
- likelihood to convert

Lead Details:
Name: {data.get('name')}
Company: {data.get('company')}
Industry: {data.get('industry')}
Company Size: {data.get('size')}
Budget: {data.get('budget')}
Problem Statement: {data.get('problem')}

Rules:
- Score between 0–100
- Hot = 75+
- Warm = 45–74
- Cold = below 45

Return EXACTLY:

Lead Score: X/100
Category: Hot/Warm/Cold

Summary:
2–3 lines business summary

Recommended Action:
clear sales next step

Follow-up Email:
professional concise email
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Lead Qualification Bot"
            },
            json={
                "model": "openai/gpt-oss-20b:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({
                "result": f"API Error {response.status_code}: {response.text}"
            })

        result = response.json()

        return jsonify({
            "result": result["choices"][0]["message"]["content"]
        })

    except Exception as e:
        return jsonify({
            "result": f"System Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)