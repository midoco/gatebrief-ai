import os
from openai import OpenAI

key = os.environ.get("NEBIUS_API_KEY")
if not key:
    raise SystemExit("Set NEBIUS_API_KEY first.")

client = OpenAI(base_url="https://api.tokenfactory.nebius.com/v1/", api_key=key)
for model in client.models.list().data:
    if "nvidia" in model.id.lower() or "nemotron" in model.id.lower():
        print(model.id)
