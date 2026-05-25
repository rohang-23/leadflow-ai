from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODELS = [
    "openai/gpt-oss-20b:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free"
]


@app.route("/")
def home():
    return render_template("index.html")


def try_model(prompt, model):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "LeadFlow AI"
        },
        json={
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        timeout=60
    )

    if response.status_code != 200:
        return None, response.text

    result = response.json()

    if "choices" not in result:
        return None, result

    return result["choices"][0]["message"]["content"], None


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if not OPENROUTER_API_KEY:
            return jsonify({
                "result": "OPENROUTER_API_KEY missing in .env"
            })

        data = request.json

        prompt = f"""
You are an expert B2B sales automation assistant.

Qualify this inbound SaaS lead.

Lead Details:
Name: {data.get('name')}
Company: {data.get('company')}
Industry: {data.get('industry')}
Company Size: {data.get('size')}
Budget: {data.get('budget')}
Problem Statement: {data.get('problem')}

Rules:
- Score 0 to 100
- Hot = 75+
- Warm = 45–74
- Cold = below 45

Return EXACTLY:

Lead Score: X/100
Category: Hot/Warm/Cold

Summary:
2–3 line business summary

Recommended Action:
Best next action

Follow-up Email:
Professional concise follow-up email
"""

        for model in MODELS:
            output, error = try_model(prompt, model)
            if output:
                return jsonify({
                    "result": output
                })

        return jsonify({
            "result": f"All providers failed. Last error: {error}"
        })

    except Exception as e:
        return jsonify({
            "result": f"System Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)