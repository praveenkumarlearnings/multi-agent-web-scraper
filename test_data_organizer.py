
import json

from data_organizer import save_dataset

# Read research data
with open(
    "research_dataset.json",
    "r",
    encoding="utf-8"
) as file:

    records = json.load(file)

# Organize and export data
save_dataset(records)

print("\nDataset generation completed!")
