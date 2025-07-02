import json
import os
import math

# ======= CONFIGURATION =======
input_file = "result_comp_cleaned.json"   # your input JSON
output_folder = "json_chunks"             # folder to store minified chunks
num_chunks = 5                             # number of chunks
# =============================

# 1. Load data
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Ensure messages exist
messages = data.get("messages", [])
total_messages = len(messages)

# Compute chunk size
chunk_size = math.ceil(total_messages / num_chunks)

# 2. Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# 3. Split messages and save minified chunks
for i in range(0, total_messages, chunk_size):
    chunk = messages[i:i + chunk_size]

    # Create chunk dict
    chunk_data = {
        "name": data.get("name", ""),
        "type": data.get("type", ""),
        "id": data.get("id", ""),
        "messages": chunk
    }

    # Output filename
    chunk_num = i // chunk_size + 1
    output_file = os.path.join(output_folder, f"chunk_{chunk_num:03d}.json")

    # Save minified JSON (no spaces)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunk_data, f, separators=(',', ':'))

    print(f"✅ Saved {output_file} ({len(chunk)} messages)")

print("🎉 All minified chunks created successfully!")
