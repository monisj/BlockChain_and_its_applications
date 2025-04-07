import openai
import json
import subprocess
import datetime

# === 1. CONFIGURATION ===
openai.api_key = 'your-openai-api-key'
CHAIN_NAME = "chain1"
STREAM_NAME = "smartcontractstream"

# === 2. FAKE DATA INPUT (Replace with real GTFS feed integration) ===
def get_real_time_features():
    return {
        "route": "R1",
        "time": "08:00",
        "passenger_count": 420,
        "vehicle_count": 8,
        "weather": "rainy",
        "day_type": "weekday"
    }

# === 3. FARE AI MODEL SIMULATION (replace with actual model.predict) ===
def predict_discount(features):
    if features["passenger_count"] < 500:
        return 0.1  # 10% discount
    return 0.0

# === 4. PROMPT BUILDER ===
def build_prompt(route, time, passenger_count, weather, day_type, discount):
    reasons = []
    if passenger_count < 500:
        reasons.append("low ridership")
    if weather.lower() in ["rainy", "snowy"]:
        reasons.append(f"{weather.lower()} weather")
    if day_type.lower() == "weekday":
        reasons.append("weekday")
    elif day_type.lower() == "weekend":
        reasons.append("weekend")

    reason_str = ", ".join(reasons)
    discount_percent = int(discount * 100)

    return (
        f"Modify the contract for Route {route} at {time}. "
        f"If passenger count is below {passenger_count} and "
        f"conditions are: {reason_str}, reduce fare by {discount_percent}%."
    )

# === 5. GENERATIVE AI ===
def get_generated_contract_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Python smart contract generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response['choices'][0]['message']['content']

# === 6. CODE VALIDATION ===
def validate_code(code):
    try:
        compile(code, "<string>", "exec")
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False

# === 7. MULTICHAIN DEPLOYMENT ===
def deploy_to_multichain(route, time, discount, contract_code):
    timestamp = datetime.datetime.utcnow().isoformat()
    key = f"{route}_{timestamp}"
    payload = {
        "route": route,
        "time": time,
        "discount": discount,
        "code": contract_code,
        "timestamp": timestamp
    }
    json_payload = json.dumps({"json": payload})
    subprocess.run([
        "multichain-cli", CHAIN_NAME,
        "publish", STREAM_NAME,
        key, json_payload
    ])
    print(f"Contract for {route} deployed with key: {key}")
    import os

LOG_FILE = "fare_update_log.json"

def log_deployment(route, time, discount, prompt, contract_code, success=True):
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "route": route,
        "time": time,
        "discount": discount,
        "prompt": prompt,
        "contract_code": contract_code,
        "status": "Success" if success else "Failed"
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([log_entry], f, indent=2)
    else:
        with open(LOG_FILE, 'r+') as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=2)


# === 8. MAIN EXECUTION LOOP ===
def main():
    features = get_real_time_features()
    discount = predict_discount(features)

    if discount > 0:
        prompt = build_prompt(
            features["route"],
            features["time"],
            features["passenger_count"],
            features["weather"],
            features["day_type"],
            discount
        )

        print("AI Prompt:\n", prompt)
        contract_code = get_generated_contract_code(prompt)
        print("\nGenerated Code:\n", contract_code)

        if validate_code(contract_code):
            deploy_to_multichain(features["route"], features["time"], discount, contract_code)
            log_deployment(features["route"], features["time"], discount, prompt, contract_code, success=True)

        else:
            print("Generated contract code is invalid. Skipping deployment.")
    else:
        print("No discount needed, skipping update.")

if __name__ == "__main__":
    main()
