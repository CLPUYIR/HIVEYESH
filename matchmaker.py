import json
import os

# --- Frontier Model Database (Maximalist) ---
# Parameters are approximate GB requirements for GGUF/EXL2 at different quants
MODELS = {
    "Reasoning": [
        {"name": "Llama-3.1 405B", "params": "405B", "ram_req": {"Q4_K_M": 230, "Q2_K": 140, "Q8_0": 430}},
        {"name": "DeepSeek-R1", "params": "671B", "ram_req": {"Q4_K_M": 380, "Q2_K": 220, "Q8_0": 700}},
        {"name": "Qwen-2.5 72B", "params": "72B", "ram_req": {"Q4_K_M": 45, "Q8_0": 80}},
        {"name": "Llama-3.1 70B", "params": "70B", "ram_req": {"Q4_K_M": 42, "Q8_0": 75}}
    ],
    "Vision": [
        {"name": "Molmo-72B-D", "params": "72B", "ram_req": {"Q4_K_M": 48, "Q8_0": 85}},
        {"name": "Pixtral-12B", "params": "12B", "ram_req": {"Q4_K_M": 8, "Q8_0": 14}}
    ],
    "Audio": [
        {"name": "Faster-Whisper Large-v3", "params": "1.5B", "ram_req": {"FP16": 3.1, "INT8": 1.6}}
    ],
    "Creative": [
        {"name": "SDXL Turbo (OpenVINO)", "params": "2.6B", "ram_req": {"FP16": 12, "INT8": 6}}
    ]
}

def find_maximalist_fit(intent, capacity_gb):
    """Finds the largest model in the category that fits the capacity."""
    if intent not in MODELS:
        return None
    
    candidates = MODELS[intent]
    best_fit = None
    
    for model in candidates:
        # Check quants from highest to lowest
        # We prefer high parameters over high quant if capacity allows
        sorted_quants = sorted(model["ram_req"].items(), key=lambda x: x[1], reverse=True)
        
        for quant, req in sorted_quants:
            if req <= capacity_gb:
                # If we find a quant that fits, this is our best fit for THIS model.
                # Since candidates are usually ordered by power, first model that fits at ANY quant is likely the maximalist choice.
                best_fit = {
                    "model": model["name"],
                    "params": model["params"],
                    "quant": quant,
                    "ram_used": req,
                    "headroom": round(capacity_gb - req, 2)
                }
                return best_fit
                
    return None

def run_matchmaker(intent):
    if not os.path.exists("node_profile.json"):
        return {"error": "No cluster profile found. Run Stage 2 first."}
    
    with open("node_profile.json", "r") as f:
        profile = json.load(f)
        capacity = profile["net_capacity_gb"]
    
    fit = find_maximalist_fit(intent, capacity)
    return fit

if __name__ == "__main__":
    # Test
    print("--- Hiveesh Stage 4: Maximalist Matchmaker ---")
    intent = "Reasoning"
    res = run_matchmaker(intent)
    if res:
        print(f"Recommended: {res['model']} ({res['params']})")
        print(f"Quantization: {res['quant']}")
        print(f"Memory Usage: {res['ram_used']} GB / Total: {res['ram_used'] + res['headroom']} GB")
    else:
        print("No frontier models fit the current cluster capacity.")
