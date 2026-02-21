from app import create_app
from extensions import db, bcrypt
from models.user import User
from models.advisory import Advisory

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create admin user
    admin = User(username="admin")
    admin.set_password("Hero@12345#")
    db.session.add(admin)

    # Seed advisory data
    advisories = [
        Advisory(crop="Wheat", season="Rabi", soil_type="Loamy", irrigation="Every 20 days", fertilizer="Urea 120kg/ha", pest_control="Spray Chlorpyrifos", n=120, p=60, k=40),
        Advisory(crop="Wheat", season="Rabi", soil_type="Clay", irrigation="Every 25 days", fertilizer="DAP 100kg/ha", pest_control="Spray Mancozeb", n=100, p=50, k=30),
        Advisory(crop="Wheat", season="Rabi", soil_type="Sandy", irrigation="Every 15 days", fertilizer="NPK 80kg/ha", pest_control="Neem oil spray", n=80, p=40, k=20),
        Advisory(crop="Rice", season="Kharif", soil_type="Clay", irrigation="Flood irrigation", fertilizer="Urea 150kg/ha", pest_control="Spray Carbofuran", n=150, p=60, k=50),
        Advisory(crop="Rice", season="Kharif", soil_type="Loamy", irrigation="Every 10 days", fertilizer="DAP 120kg/ha", pest_control="Spray Monocrotophos", n=120, p=50, k=40),
        Advisory(crop="Rice", season="Kharif", soil_type="Sandy", irrigation="Every 7 days", fertilizer="NPK 100kg/ha", pest_control="Neem oil spray", n=100, p=40, k=30),
        Advisory(crop="Cotton", season="Kharif", soil_type="Loamy", irrigation="Every 15 days", fertilizer="NPK 150kg/ha", pest_control="Spray Imidacloprid", n=150, p=70, k=60),
        Advisory(crop="Cotton", season="Kharif", soil_type="Clay", irrigation="Every 20 days", fertilizer="Urea 130kg/ha", pest_control="Spray Cypermethrin", n=130, p=60, k=50),
        Advisory(crop="Cotton", season="Kharif", soil_type="Sandy", irrigation="Every 10 days", fertilizer="DAP 110kg/ha", pest_control="Neem oil spray", n=110, p=50, k=40),
        Advisory(crop="Maize", season="Kharif", soil_type="Loamy", irrigation="Every 10 days", fertilizer="Urea 100kg/ha", pest_control="Spray Atrazine", n=100, p=50, k=40),
        Advisory(crop="Maize", season="Rabi", soil_type="Sandy", irrigation="Every 12 days", fertilizer="NPK 90kg/ha", pest_control="Spray Chlorpyrifos", n=90, p=40, k=30),
        Advisory(crop="Maize", season="Zaid", soil_type="Clay", irrigation="Every 8 days", fertilizer="DAP 80kg/ha", pest_control="Neem oil spray", n=80, p=35, k=25),
        Advisory(crop="Tomato", season="Rabi", soil_type="Loamy", irrigation="Every 5 days", fertilizer="NPK 120kg/ha", pest_control="Spray Trichoderma", n=120, p=60, k=80),
        Advisory(crop="Tomato", season="Zaid", soil_type="Sandy", irrigation="Every 4 days", fertilizer="Urea 100kg/ha", pest_control="Spray Mancozeb", n=100, p=50, k=70),
        Advisory(crop="Tomato", season="Kharif", soil_type="Clay", irrigation="Every 6 days", fertilizer="DAP 90kg/ha", pest_control="Neem oil spray", n=90, p=45, k=60),
        Advisory(crop="Soybean", season="Kharif", soil_type="Loamy", irrigation="Every 15 days", fertilizer="Rhizobium 10kg/ha", pest_control="Spray Profenofos", n=30, p=60, k=40),
        Advisory(crop="Soybean", season="Kharif", soil_type="Clay", irrigation="Every 18 days", fertilizer="NPK 80kg/ha", pest_control="Spray Endosulfan", n=25, p=55, k=35),
        Advisory(crop="Groundnut", season="Kharif", soil_type="Sandy", irrigation="Every 10 days", fertilizer="Gypsum 200kg/ha", pest_control="Spray Chlorothalonil", n=20, p=40, k=30),
        Advisory(crop="Groundnut", season="Rabi", soil_type="Loamy", irrigation="Every 12 days", fertilizer="DAP 60kg/ha", pest_control="Neem oil spray", n=25, p=50, k=35),
        Advisory(crop="Sugarcane", season="Zaid", soil_type="Loamy", irrigation="Every 7 days", fertilizer="Urea 200kg/ha", pest_control="Spray Lindane", n=200, p=80, k=100),
        Advisory(crop="Sugarcane", season="Kharif", soil_type="Clay", irrigation="Every 10 days", fertilizer="NPK 180kg/ha", pest_control="Spray Chlorpyrifos", n=180, p=70, k=90),
    ]

    db.session.add_all(advisories)
    db.session.commit()
    print("✅ Database seeded successfully with 21 records!")