from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from .models import Scout
from . import db
import csv
import tbapy

tba = tbapy.TBA('h39XHSEqXkc59WvXY0lteYagmwOzWD0wmLV2CxZulOMcB89YIHFUIczJxvGTtM6X')
auth = Blueprint('auth', __name__)

# Create a list of teams attending the event
all_teams_simple = tba.event_teams("2022tant", "simple")
all_teams = []
for i in range (len(all_teams_simple)):
    all_teams.append(all_teams_simple[i]['team_number'])

# home.html
@auth.route('/')
@auth.route('/home')
def home():
    return render_template('home.html')

# data.html
@auth.route('/data', methods=['GET','POST'])
def data():    
    # Show all the scouting data
    data = Scout.query.order_by(Scout.team).all()

    # Search teams
    if request.method == 'POST':
        searched_team = request.form.get('searched_team')
        data = Scout.query.filter_by(team=searched_team).all()

    return render_template('data.html', data=data)

# scouting.html
@auth.route('/scout', methods=['GET', 'POST'])
def attempt():
    if request.method == 'POST':
        team = request.form.get('team')
        round = request.form.get('round')
        alliance = request.form.get('alliance')

        # Auton
        starting_pos = request.form.get('starting_pos')
        taxi = request.form.get('taxi')

        auton_upper_in = request.form.get('auton_upper_in')
        auton_upper_missed = request.form.get('auton_upper_missed')
        auton_upper_unreliable = request.form.get('auton_unreliable_upper')

        auton_lower_in = request.form.get('auton_lower_in')
        auton_lower_missed = request.form.get('auton_lower_missed')
        auton_lower_unreliable = request.form.get('auton_lower_unreliable')

        # Teleop
        tele_upper_in = request.form.get('tele_upper_in')
        tele_upper_missed = request.form.get('tele_upper_missed')
        tele_upper_unreliable = request.form.get('tele_unreliable_upper')

        tele_lower_in = request.form.get('tele_lower_in')
        tele_lower_missed = request.form.get('tele_lower_missed')
        tele_lower_unreliable = request.form.get('tele_lower_unreliable')

        hang = request.form.get('hang')
        win = request.form.get('win')
        cargo_bonus = request.form.get('cargo_bonus')
        hangar_bonus = request.form.get('hangar_bonus')

        notes = request.form.get('notes')

        new_scout = Scout(team=team, round=round, alliance=alliance, starting_pos=starting_pos, \
                          taxi=taxi, auton_upper_in=auton_upper_in, auton_upper_missed=auton_upper_missed, \
                          auton_upper_unreliable=auton_upper_unreliable, auton_lower_in=auton_lower_in, \
                          auton_lower_missed=auton_lower_missed, auton_lower_unreliable=auton_lower_unreliable, \
                          tele_upper_in=tele_upper_in, tele_upper_missed=tele_upper_missed, \
                          tele_upper_unreliable=tele_upper_unreliable, tele_lower_in=tele_lower_in, \
                          tele_lower_missed=tele_lower_missed, tele_lower_unreliable=tele_lower_unreliable, \
                          hang=hang, win=win, cargo_bonus=cargo_bonus, hangar_bonus=hangar_bonus, notes=notes)

        # Add to database
        db.session.add(new_scout)
        db.session.commit()
        
    return render_template('scout.html', all_teams=all_teams)

# Delete a data entry
@auth.route('/delete/<int:id>')
@auth.route('/delete', defaults={'id': None})
def delete(id):
    team_delete = Scout.query.get_or_404(id)
    db.session.delete(team_delete)
    db.session.commit()
    data = Scout.query.all()
    return render_template('data.html',data=data)

# Download the database
@auth.route('/download')
def download():
    data = Scout.query.all()

    # Store it as csv 
    with open(r'website/static/data.csv', 'w') as s_key:
        csv_out = csv.writer(s_key)

        # Horizontal labels
        csv_out.writerow(["Team", "Round", "Alliance", "Starting_pos", "Taxi", "A_Upper_In", "A_Upper_Missed", "A_Upper_Unreliable", "A_Lower_In", "A_Lower_Missed", "A_Lower_Unreliable", "T_Upper_In", "T_Upper_Missed", "T_Upper_Unreliable", "T_Lower_In", "T_Lower_Missed", "T_Lower_Unreliable", "Hang", "Cargo", "Hangar","Notes"])
        
        # Database data
        data = db.session.query(Scout.team, Scout.round, Scout.alliance, Scout.starting_pos, Scout.taxi, Scout.auton_upper_in, Scout.auton_upper_missed, Scout.auton_upper_unreliable, Scout.auton_lower_in, Scout.auton_lower_missed, Scout.auton_lower_unreliable, Scout.tele_upper_in, Scout.tele_upper_missed, Scout.tele_upper_unreliable, Scout.tele_lower_in, Scout.tele_lower_missed, Scout.tele_lower_unreliable, Scout.hang, Scout.cargo_bonus, Scout.hangar_bonus, Scout.notes)
        
        for i in data:
            csv_out.writerow(i)
        return render_template('download.html')
