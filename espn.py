from flask import Flask, render_template
import requests
from espn_api.football import League
from espn_api.football import BoxPlayer

app = Flask(__name__)

league = League(
        league_id=20594, 
        year=2023,
        swid='{3F51D055-B7DD-460E-97D1-47E01D07F052}',
        espn_s2='AEBDpfrnmkEObJfIFNaH%2BXh3XV%2BA%2F%2BTQpy61%2BI4ACWsbjt8BYFcJQJ5WdWSgyURUF6X3bsthfcUPM93h5djreorjHcMuW0W9m3B8P5%2FknTTVphViR6pEFGc4jGTeBpF6QIMeCmV8EB8zfHwAiT0lPkIaPX8kEePERFXPwO%2Bv3hM47%2FjOpU1PHmgKnuVEtARVfzvhVnCC96u4TEQiDZR6dLZo1UIVIUBJB8qou5KoE8cYjxMcNZpthHXerMfCa65dm4TfEBczWf9wvQUIcK5MZG90sgseeSpDOcYa60BjYhr8GwAPDZ%2BLSbISc0fQvhBoR2Y%3D'
    )
all_players = []

@app.route('/')
def index():
    global all_players
    global league
    post_season = range(15, 18)
    box_score_range = []
    for week in post_season:
        box_score_range.append(league.box_scores(week))

    counter = 0
    for box_score in box_score_range:
        for matchup in box_score:
            all_players += matchup.home_lineup + matchup.away_lineup

    ## Combine points for each player
    player_dict = {}
    for player in all_players:
        if player.name not in player_dict:
            player_dict[player.name] = {
                'position': player.position,
                'points': [[player.points, player.projected_points]]
            }
        else:
            player_dict[player.name]['points'].append([player.points, player.projected_points])

    #Convert combined players back to a list
    aggregate_players = []
    for name, data in player_dict.items():
        aggregate_players.append({
            'name': name,
            'position': data['position'],
            'points': data['points'],
            'clutch_score': clutch_score(data['points'])
        })

    #aggregate_players = sorted(aggregate_players, key=lambda x: sum(x['points']), reverse=True)
    
    return render_template('index.html', players=aggregate_players)

def clutch_score(scores = [[]]):
    clutch_scores = []
    for week_score in scores:
        if (week_score[1] != 0):
            clutch_score = (week_score[0] / week_score[1]) * 100
            clutch_scores.append(clutch_score)
        else:
            clutch_scores.append(0)
    return sum(clutch_scores) / len(clutch_scores)
        




if __name__ == '__main__':
    app.run(debug=True)