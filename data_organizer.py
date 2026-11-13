
import json
import pandas as pd


def save_dataset(records):

    if not records:
        print("No research records found.")
        return

    # Save JSON dataset
    with open("research_dataset.json", "w", encoding="utf-8") as file:
        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )

    # Convert to DataFrame
    df = pd.DataFrame(records)

    # Convert key_topics list into CSV-friendly text
    if "key_topics" in df.columns:
        df["key_topics"] = df["key_topics"].apply(
            lambda topics: " | ".join(topics)
            if isinstance(topics, list)
            else topics
        )

    # Save CSV dataset
    df.to_csv(
        "research_dataset.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nDataset saved successfully!")
    print(f"Total records: {len(records)}")
    print("JSON: research_dataset.json")
    print("CSV: research_dataset.csv")
