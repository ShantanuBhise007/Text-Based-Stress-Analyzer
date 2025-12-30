import os
import csv

# Define the folder path
data_dir = os.path.join("backend", "data")
os.makedirs(data_dir, exist_ok=True)

# Define the data for each CSV
files = {
    "positive_words.csv": [
        ["word", "weight"],
        ["calm", "2"], ["happy", "2"], ["joy", "3"], ["resilient", "3"],
        ["hope", "2"], ["grateful", "2"], ["confident", "2"], ["love", "2"],
        ["excited", "2"], ["relax", "2"], ["peace", "2"], ["strong", "2"],
        ["accomplished", "3"]
    ],
    "stress_words.csv": [
        ["word", "weight"],
        ["busy", "1"], ["deadline", "2"], ["tired", "2"], ["annoyed", "2"],
        ["pressure", "2"], ["rushed", "2"], ["nervous", "2"], ["anxious", "2"],
        ["workload", "2"], ["late", "1"], ["overwhelmed", "3"], ["frustrated", "2"],
        ["tense", "2"], ["headache", "2"]
    ],
    "depressive_words.csv": [
        ["word", "weight"],
        ["hopeless", "4"], ["empty", "3"], ["lonely", "3"], ["darkness", "3"],
        ["pain", "3"], ["useless", "4"], ["exhausted", "3"], ["sad", "2"],
        ["crying", "3"], ["numb", "3"], ["guilty", "3"], ["failure", "4"],
        ["suffering", "4"]
    ],
    "high_risk_words.csv": [
        ["word", "weight"],
        ["suicide", "10"], ["kill myself", "10"], ["end it all", "10"],
        ["die", "10"], ["no reason to live", "10"], ["hurt myself", "10"],
        ["goodbye forever", "10"]
    ]
}

# Create the files
print(f"Creating CSV files in {data_dir}...")
for filename, rows in files.items():
    file_path = os.path.join(data_dir, filename)
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"✅ Created {filename}")

print("\nSuccess! You can now run the backend.")