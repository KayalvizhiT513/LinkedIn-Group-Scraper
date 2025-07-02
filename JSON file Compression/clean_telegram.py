import json

# Load your exported JSON file
input_file = "result_comp.json"
output_file = "result_comp_cleaned.json"

# Load the data
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Create a new dict to hold cleaned messages
cleaned_data = {
    "name": data.get("name", ""),
    "type": data.get("type", ""),
    "id": data.get("id", ""),
    "messages": []
}

# Loop through messages
for message in data["messages"]:
    # Extract essential fields
    cleaned_message = {
        "id": message.get("id"),
        "date": message.get("date"),
        "from": message.get("from"),
        "text": None
    }

    # Handle text field, which can be:
    # - a string
    # - a list of parts (entities)
    if isinstance(message.get("text"), list):
        # Join all parts into one string
        cleaned_message["text"] = "".join(
            part["text"] if isinstance(part, dict) else str(part)
            for part in message["text"]
        )
    else:
        cleaned_message["text"] = message.get("text")

    # Append to cleaned list
    cleaned_data["messages"].append(cleaned_message)

# Write cleaned data to output file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print(f"✅ Cleaned JSON saved to {output_file}")
