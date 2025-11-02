import json

# Read the urban park scenario
with open('scenarios/urban_park.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Before: {len(data['environment']['walls'])} walls")

# Keep only the first 4 boundary walls
data['environment']['walls'] = data['environment']['walls'][:4]

print(f"After: {len(data['environment']['walls'])} walls")

# Write back
with open('scenarios/urban_park.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done! Removed all internal walls, kept only 4 boundary walls.")
