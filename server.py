import json
import sys
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


def get_club_by_email(email):
    # try:
        club = [club for club in clubs if club['email'] == email][0]
        return club


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = get_club_by_email(request.form['email'])
        return render_template('welcome.html', club=club, clubs=clubs, competitions=competitions)
    except IndexError as err:
        error = 'The email address provided does not exist'
        return render_template('index.html', error=error)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    max_places = min(12, int(foundClub["points"]))
    competition_datetime_date = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
    competition_is_not_finished = competition_datetime_date > datetime.now()
    if competition_is_not_finished:
        flash("Perfect. Go on.")
        return render_template('booking.html', club=foundClub, competition=foundCompetition, max_places=max_places)
    else:
        flash("You can't book events in the past")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))