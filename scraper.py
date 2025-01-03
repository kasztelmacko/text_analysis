from firecrawl import FirecrawlApp
import pandas as pd
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

data = pd.read_csv("data/ai_pricing_index.csv")

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

class ExtractSchema(BaseModel):
    call_to_action: str | None = Field(..., title="Text on the main button")
    tier_names: list[str] | None = Field(..., title="Names of the pricing tiers")
    tier_prices: list[str] | None = Field(..., title="Prices of the pricing tiers")
    frequently_asked_questions: list[str] | None = Field(..., title="Frequently asked questions")
    frequently_asked_questions_answers: list[str] | None = Field(..., title="Answers to the frequently asked questions")

extracted_data = []

for index, row in data.iterrows():
    url = row["URL"]
    try:
        response = app.scrape_url(url, {
            'formats': ["extract"],
            'extract': {
                'schema': ExtractSchema.model_json_schema(),
            }
        })

        extracted_data.append({
            "url": url,
            "company": row["Company"],
            "ai_pricing_model": row["AI Pricing Model"],
            "category": row["Category"],
            "data": response.get("extract")
        })
        print(f"Extracted data for {url}")

    except requests.exceptions.HTTPError as e:
        print(f"Failed to scrape {url}: {e}")
        continue

with open("data/batch3.json", "w") as json_file:
    json.dump(extracted_data, json_file, indent=4)