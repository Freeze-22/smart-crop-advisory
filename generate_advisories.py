import pandas as pd
from app import create_app
from extensions import db
from models.advisory import Advisory
from models.user import User

app = create_app()

# Advisory templates based on crop
advisory_map = {
    "rice":       {"irrigation": "Flood irrigation every 10 days", "fertilizer": "Urea 150kg/ha + DAP 60kg/ha", "pest_control": "Spray Carbofuran 3G"},
    "wheat":      {"irrigation": "Every 20 days", "fertilizer": "Urea 120kg/ha + SSP 80kg/ha", "pest_control": "Spray Chlorpyrifos"},
    "maize":      {"irrigation": "Every 10 days", "fertilizer": "Urea 100kg/ha + NPK", "pest_control": "Spray Atrazine"},
    "cotton":     {"irrigation": "Every 15 days", "fertilizer": "NPK 150kg/ha", "pest_control": "Spray Imidacloprid"},
    "sugarcane":  {"irrigation": "Every 7 days", "fertilizer": "Urea 200kg/ha", "pest_control": "Spray Lindane"},
    "tomato":     {"irrigation": "Every 5 days", "fertilizer": "NPK 120kg/ha", "pest_control": "Spray Trichoderma"},
    "potato":     {"irrigation": "Every 8 days", "fertilizer": "NPK 150kg/ha", "pest_control": "Spray Mancozeb"},
    "onion":      {"irrigation": "Every 7 days", "fertilizer": "NPK 100kg/ha", "pest_control": "Spray Carbendazim"},
    "mungbean":   {"irrigation": "Every 12 days", "fertilizer": "Rhizobium 8kg/ha", "pest_control": "Neem oil spray"},
    "blackgram":  {"irrigation": "Every 12 days", "fertilizer": "DAP 50kg/ha", "pest_control": "Neem oil spray"},
    "lentil":     {"irrigation": "Every 20 days", "fertilizer": "SSP 60kg/ha", "pest_control": "Spray Thiram"},
    "pomegranate":{"irrigation": "Every 10 days", "fertilizer": "NPK 80kg/ha", "pest_control": "Spray Copper Oxychloride"},
    "banana":     {"irrigation": "Every 5 days", "fertilizer": "Urea 200kg/ha", "pest_control": "Spray Carbendazim"},
    "mango":      {"irrigation": "Every 15 days", "fertilizer": "NPK 100kg/ha", "pest_control": "Spray Dimethoate"},
    "grapes":     {"irrigation": "Every 7 days", "fertilizer": "NPK 120kg/ha", "pest_control": "Spray Mancozeb"},
    "watermelon": {"irrigation": "Every 6 days", "fertilizer": "NPK 90kg/ha", "pest_control": "Spray Imidacloprid"},
    "muskmelon":  {"irrigation": "Every 6 days", "fertilizer": "NPK 85kg/ha", "pest_control": "Neem oil spray"},
    "apple":      {"irrigation": "Every 15 days", "fertilizer": "NPK 110kg/ha", "pest_control": "Spray Captan"},
    "orange":     {"irrigation": "Every 10 days", "fertilizer": "Urea 150kg/ha", "pest_control": "Spray Copper Oxychloride"},
    "papaya":     {"irrigation": "Every 5 days", "fertilizer": "NPK 100kg/ha", "pest_control": "Spray Carbendazim"},
    "coconut":    {"irrigation": "Every 7 days", "fertilizer": "NPK 130kg/ha", "pest_control": "Spray Chlorpyrifos"},
    "jute":       {"irrigation": "Every 10 days", "fertilizer": "Urea 60kg/ha", "pest_control": "Neem oil spray"},
    "coffee":     {"irrigation": "Every 10 days", "fertilizer": "NPK 120kg/ha", "pest_control": "Spray Copper Oxychloride"},
}

seasons = ["Kharif", "Rabi", "Zaid"]
soil_types = ["Loamy", "Clay", "Sandy"]

df = pd.read_csv("Crop_recommendation.csv")

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create admin
    admin = User(username="admin")
    admin.set_password("admin123")
    db.session.add(admin)

    # Generate advisories from dataset
    records = []
    seen = set()

    for _, row in df.iterrows():
        crop = row['label']
        if crop not in advisory_map:
            continue

        # Assign season and soil based on temperature/humidity
        if row['temperature'] > 25:
            season = "Kharif"
        elif row['temperature'] > 18:
            season = "Rabi"
        else:
            season = "Zaid"

        if row['ph'] < 6:
            soil = "Sandy"
        elif row['ph'] > 7:
            soil = "Clay"
        else:
            soil = "Loamy"

        key = (crop, season, soil)
        if key in seen:
            continue
        seen.add(key)

        info = advisory_map[crop]
        records.append(Advisory(
            crop=crop.capitalize(),
            season=season,
            soil_type=soil,
            irrigation=info['irrigation'],
            fertilizer=info['fertilizer'],
            pest_control=info['pest_control'],
            n=round(row['N'], 1),
            p=round(row['P'], 1),
            k=round(row['K'], 1)
        ))

    db.session.add_all(records)
    db.session.commit()
    print(f"✅ Database seeded with {len(records)} advisory records from real dataset!")