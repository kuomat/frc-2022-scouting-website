from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Scout(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(20))
    round = db.Column(db.String(20))
    alliance = db.Column(db.String(20))

    starting_pos = db.Column(db.String(20))
    taxi = db.Column(db.String(20))
    auton_upper_in = db.Column(db.String(20))
    auton_upper_missed = db.Column(db.String(20))
    auton_upper_unreliable = db.Column(db.String(20))

    auton_lower_in = db.Column(db.String(20))
    auton_lower_missed = db.Column(db.String(20))
    auton_lower_unreliable = db.Column(db.String(20))

    tele_upper_in = db.Column(db.String(20))
    tele_upper_missed = db.Column(db.String(20))
    tele_upper_unreliable = db.Column(db.String(20))

    tele_lower_in = db.Column(db.String(20))
    tele_lower_missed = db.Column(db.String(20))
    tele_lower_unreliable = db.Column(db.String(20))

    hang = db.Column(db.String(20))
    win = db.Column(db.String(20))
    cargo_bonus = db.Column(db.String(20))
    hangar_bonus = db.Column(db.String(20))
    
    notes = db.Column(db.String(200))
