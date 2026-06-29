# extractor.py
from PIL import Image
import base64
import json
import urllib.request


# ─────────────────────────────
# Option 1 — Claude Vision API (needs API key)
# ─────────────────────────────
def extract_bill_claude(image_path: str, api_key: str) -> dict:

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": """Extract from this MSEDCL bill, return ONLY JSON no explanation no markdown:
{
    "consumer_name": "",
    "consumer_no": "",
    "connection_type": "",
    "sanctioned_load_kw": "",
    "bill_month": "",
    "bill_amount": 0,
    "monthly_units": [
        {"month": "Feb-2025", "units": 0},
        {"month": "Mar-2025", "units": 0},
        {"month": "Apr-2025", "units": 0},
        {"month": "May-2025", "units": 0},
        {"month": "Jun-2025", "units": 0},
        {"month": "Jul-2025", "units": 0},
        {"month": "Aug-2025", "units": 0},
        {"month": "Sep-2025", "units": 0},
        {"month": "Oct-2025", "units": 0},
        {"month": "Nov-2025", "units": 0},
        {"month": "Dec-2025", "units": 0},
        {"month": "Jan-2026", "units": 0}
    ]
}
Fill monthly_units from the consumption history on the bill."""
                }
            ]
        }]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
    )

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    raw = data["content"][0]["text"].strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

# ─────────────────────────────
# Option 2 — Gemini Vision (free API key)
# ─────────────────────────────
def extract_bill_gemini(image_path: str, api_key: str) -> dict:
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    img = Image.open(image_path)

    prompt = """Extract these fields from this MSEDCL Maharashtra electricity bill.
Return ONLY valid JSON, no explanation, no markdown, no backticks.

{
    "consumer_name": "",
    "consumer_no": "",
    "connection_type": "",
    "sanctioned_load_kw": "",
    "bill_month": "",
    "bill_amount": 0,
    "monthly_units": [
        {"month": "Feb-2025", "units": 0},
        {"month": "Mar-2025", "units": 0},
        {"month": "Apr-2025", "units": 0},
        {"month": "May-2025", "units": 0},
        {"month": "Jun-2025", "units": 0},
        {"month": "Jul-2025", "units": 0},
        {"month": "Aug-2025", "units": 0},
        {"month": "Sep-2025", "units": 0},
        {"month": "Oct-2025", "units": 0},
        {"month": "Nov-2025", "units": 0},
        {"month": "Dec-2025", "units": 0},
        {"month": "Jan-2026", "units": 0}
    ]
}
Fill monthly_units from the consumption history on the bill.
bill_amount = total payable amount."""

    response = model.generate_content([prompt, img])
    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


# ─────────────────────────────
# Main router — called by app.py
# ─────────────────────────────
def extract_bill_data(image_path: str, api_key: str = None, method: str = "gemini") -> dict:
    if method == "claude" and api_key:
        return extract_bill_claude(image_path, api_key)
    elif method == "gemini" and api_key:
        return extract_bill_gemini(image_path, api_key)
    else:
        raise ValueError("Please provide an API key for Claude or Gemini.")