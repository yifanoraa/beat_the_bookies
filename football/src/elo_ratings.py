import pandas as pd
import numpy as np

with open("epl-training.csv") as training_set:
    df = pd.read_csv(training_set, skipinitialspace=True)
    


def getEloRanking():
    csv_dict = df.to_dict(orient='list')
    home_team = csv_dict['HomeTeam']
    away_team = csv_dict['AwayTeam']
    Ftr = csv_dict['FTR']

    #find the number of teams in the league:
    num_team = []
    for i in range(len(home_team)):
        if home_team[i] not in num_team:
            num_team.append(home_team[i])
    #total number of 36 team.
    
    #initialise elo rating 
    ratings = np.ones(len(num_team))*1500
    elo_ratings = dict(zip(num_team,ratings))
    #Home Advantage initially guess 100
    HA = 100
    #G is the margin parameters needs to be calculated through 
    #the difference

    #parameters setting for K 
    K = 20

    #parameters setting for G
    def G_calculator(Home_goal,Away_goal):
        if abs(Home_goal-Away_goal) == 1:
            G = 1
        elif abs(Home_goal-Away_goal) == 0:
            G = 1
        elif abs(Home_goal-Away_goal) == 2:
            G = 1.5
        else:
            G = (11+abs(Home_goal-Away_goal))/8
        return G

    #create home and away elo rating list, for training
    home_elo = []
    away_elo = []
    sum_elo = 0
    for i in range(len(home_team)):
        home = home_team[i]
        away = away_team[i]
        dr = elo_ratings[home] - elo_ratings[away] + HA 
        home_elo.append(elo_ratings[home])
        away_elo.append(elo_ratings[away])
        # account for home advantage
        E = 1/(1+10**(-dr/400))
        H = csv_dict['HTHG'][i]
        A = csv_dict['HTAG'][i]
        G = G_calculator(H,A)
        if csv_dict['FTR'][i] == 'H':
            O = 1
        elif csv_dict['FTR'][i] == 'D':
            O = 0.5
        elif csv_dict['FTR'][i] == 'A':
            O = 0
        delta_elo = K*G*(O-E)
        #update elo ratings
        elo_ratings[home] = elo_ratings[home] + delta_elo
        elo_ratings[away] = elo_ratings[away] - delta_elo
        #update home advantage parameters
        sum_elo = sum_elo + delta_elo
        HA = HA + sum_elo*0.075
    return home_elo, away_elo

print(len(home_elo))
