import requests
import time

# Configuration
API_KEY = ""
BASE_URL = "https://data.guavy.com/v1"
TARGET_ASSET = "BTC"
THRESHOLD = 0.7  # Alert if sentiment is higher than 70% bullish

def get_market_sentiment(asset):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        # Targeting the sentiment endpoint
        response = requests.get(f"{BASE_URL}/sentiment/{asset}", headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Structure assumed from 2026 Guavy Sandbox docs
        score = data.get("sentiment_score", 0)
        summary = data.get("summary", "No data")
        return score, summary
    except Exception as e:
        print(f"Error connecting to the Alchemical Data Stream: {e}")
        return None, None
        
def monitor_loop():
    print(f"--- Sentinel Active: Monitoring {TARGET_ASSET} ---")
    while True:
        score, summary = get_market_sentiment(TARGET_ASSET)
        
        if score is not None:
            status = "BULLISH" if score > THRESHOLD else "STAGNANT"
            print(f"[{time.strftime('%H:%M:%S')}] Score: {score:.2f} | Status: {status}")

            if score > THRESHOLD:
                print(f"ALERT: High Volatility Detected - {summary}")

        # Wait 5 minutes between polls (to stay within Free Tier limits)
        time.sleep(300)

if __name__ == "__main__":
    monitor_loop()