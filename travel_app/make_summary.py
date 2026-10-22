import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV = BASE_DIR.parent / "data" / "cleaned" / "Hotel_Reviews_PowerBI.csv"

df = pd.read_csv(CSV)
skip = {"VADER_Sentiment", "VADER_Compound", "Reviewer_Score", "Review_Text"}

parts = []
for col in df.columns:
    if col in skip:
        continue
    if 1 < df[col].nunique() <= 30:
        g = (
            df.groupby([df[col].astype(str), "VADER_Sentiment"])
            .size()
            .reset_index(name="Reviews")
        )
        g.columns = ["Value", "Sentiment", "Reviews"]
        g.insert(0, "Category", col)
        parts.append(g)

out = pd.concat(parts, ignore_index=True)
out.to_csv(BASE_DIR / "summary.csv", index=False)
print("Saved summary.csv with categories:", sorted(out["Category"].unique()))