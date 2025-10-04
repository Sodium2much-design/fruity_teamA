from fastapi import FastAPI
from pydantic import BaseModel
from collections import defaultdict

app = FastAPI()

# Simulate a database for counting juice clicks
juice_counter = defaultdict(int)

# List of all juice types with initial click count set to 0
all_juices = ['starfruit', 'dragonfruit', 'mangosteen', 'melon', 'lemon', 'watermelon']

class Juice(BaseModel):
    name: str
    click_count: int

@app.post("/juices/{juice_type}/click")
def update_juice_click(juice_type: str):
    # Increase click count for the juice type
    juice_counter[juice_type] += 1
    return {"message": f"Clicked {juice_type} juice"}

@app.get("/juices/")
def get_juice_stats():
    # Ensure all juices have a click count, even if there were no clicks
    stats = []
    for juice in all_juices:
        # Add juices that have not been clicked yet with a default count of 0
        stats.append({"name": juice, "click_count": juice_counter[juice]})
    return stats
