from extensions import db

class Advisory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    soil_type = db.Column(db.String(50), nullable=False)
    irrigation = db.Column(db.String(200), nullable=False)
    fertilizer = db.Column(db.String(200), nullable=False)
    pest_control = db.Column(db.String(200), nullable=False)
    n = db.Column(db.Float, nullable=False)
    p = db.Column(db.Float, nullable=False)
    k = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "crop": self.crop,
            "season": self.season,
            "soil_type": self.soil_type,
            "irrigation": self.irrigation,
            "fertilizer": self.fertilizer,
            "pest_control": self.pest_control,
            "n": self.n,
            "p": self.p,
            "k": self.k
        }