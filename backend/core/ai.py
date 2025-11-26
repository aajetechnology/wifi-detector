# backend/core/ai.py
import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def analyze_network(network: dict) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("GEMINI_API_KEY missing!")
        return {"risk": "risky", "reason": "No API key", "vpn_needed": True}

    # UPDATED MODEL FOR 2025 - gemini-2.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    prompt = f"""WiFi Security Analysis:
- SSID: {network['ssid']}
- Security: {network['security']}
- Signal: {network['signal']} dBm

Risk assessment:
- "safe" for WPA3/WPA2 with strong signal
- "risky" for WPA2/weak signal or public
- "dangerous" for Open/WEP

Return ONLY valid JSON (no other text):
{{"risk": "safe|risky|dangerous", "reason": "max 6 words", "vpn_needed": true|false}}"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
        }
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            print(f"Analyzing {network['ssid']} with Gemini 2.5...")
            response = await client.post(url, json=payload)
            
            if response.status_code != 200:
                print(f"HTTP {response.status_code}: {response.text}")
                return {"risk": "risky", "reason": "API error", "vpn_needed": True}

            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"Gemini response: {text}")
            
            # Parse JSON
            result = json.loads(text)
            print(f"Parsed AI result: {result}")
            return result

    except Exception as e:
        print(f"AI failed completely: {e}")
        return {"risk": "risky", "reason": "AI unavailable", "vpn_needed": True}