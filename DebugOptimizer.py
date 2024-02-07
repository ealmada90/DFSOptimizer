import csv
from Objects.DFSPlayer import *
from pulp import *
import json
from itertools import combinations


#declare variables
lineupSlots = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
positionRequirements = ["PG", "PG", "SG", "SG", "SF", "SF", "PF", "PF", "C"]

#declare functions
def create_player_from_row(row):
    positions = row['Position'].split("/")
    return DFSPlayer(int(row['\ufeffLineStarId']), row['Name'], row['Team'], positions, int(row['Salary']), float(row['Projected']))

def initPlayersDictionary(list):
    players = {}
    for p in list:
        s = json.dumps(p)
        j = json.loads(s)
        player = DFSPlayer(**j)
        if(player.projection > 0):
            player.positions = player.positions.split("/")
            players[player.id] = player
    return players

def initPlayerNames(list):
    returnList = []
    for player in list:
        if player.name not in returnList:
            returnList.append(player.name)
    return returnList

def initPlayerContainers(list):
    for slot,players in lineupSlots.items():
        for playerId in list:
            if(positionRequirements[slot] in list[playerId].position):
                players.append(playerId)

def initPlayerList(list):
    returnList = []
    for player in list:
        if("/" in player.position):
            positions = player.position.split("/")
            for pos in positions:
                p = DFSPlayer(player.name, player.team, pos, player.salary, player.projection)
                returnList.append(p)
        else:
            returnList.append(player)

    return returnList

def initTeamList(list):
    teamList = []
    for playerId in list:
        if(list[playerId].team not in teamList):
            teamList.append(list[playerId].team)
        
    return teamList

ordered_positions = ['PG', 'PG', 'SG', 'SG', 'SF', 'SF', 'PF', 'PF', 'C']
def orderLineup(lineup, dictionary):
    orderedLineup = []
    for index in range(9):
        for playerId in lineup:
            if(dictionary[playerId] == ordered_positions[index] and playerId not in orderedLineup):
                orderedLineup.append(playerId)

                break

    return orderedLineup

#run program
if __name__ == "__main__":

    playerList = [{'team': 'DAL', 'positions': 'PG', 'projection': 62.99, 'id': 1242359, 'salary': 12200, 'name': 'Luka Doncic'}, {'team': 'MIL', 'salary': 12100, 'positions': 'PF', 'projection': 54.53, 'name': 'Giannis Antetokounmpo', 'id': 1242360}, {'name': 'Donovan Mitchell', 'salary': 10300, 'positions': 'SG/PG', 'projection': 50.63, 'team': 'CLE', 'id': 1242361}, {'team': 'CHA', 'positions': 'PG', 'salary': 9800, 'id': 1242363, 'projection': 47.74, 'name': 'LaMelo Ball'}, {'salary': 10000, 'name': 'Kevin Durant', 'id': 1242362, 'positions': 'SF/PF', 'projection': 46.49, 'team': 'PHO'}, {'team': 'DAL', 'id': 1242364, 'salary': 9800, 'name': 'Kyrie Irving', 'positions': 'PG/SG', 'projection': 45.62}, {'positions': 'C', 'name': 'Alperen Sengun', 'id': 1242366, 'team': 'HOU', 'salary': 9400, 'projection': 45.54}, {'id': 1242368, 'positions': 'C', 'name': 'Bam Adebayo', 'projection': 43.89, 'team': 'MIA', 'salary': 8900}, {'positions': 'SG', 'team': 'PHO', 'id': 1242365, 'projection': 43.76, 'salary': 9700, 'name': 'Devin Booker'}, {'name': 'Rudy Gobert', 'projection': 41.9, 'team': 'MIN', 'salary': 8200, 'positions': 'C', 'id': 1242375}, {'name': 'Anthony Edwards', 'id': 1242369, 'team': 'MIN', 'salary': 8800, 'projection': 41.09, 'positions': 'SG/SF'}, {'salary': 9000, 'projection': 40.52, 'name': 'Damian Lillard', 'team': 'MIL', 'positions': 'PG', 'id': 1242367}, {'salary': 8400, 'id': 1242373, 'projection': 40.32, 'name': 'Fred VanVleet', 'team': 'HOU', 'positions': 'PG'}, {'positions': 'C/PF', 'salary': 8500, 'projection': 39.67, 'id': 1242372, 'name': 'Jarrett Allen', 'team': 'CLE'}, {'projection': 38.77, 'positions': 'SF/PF', 'id': 1242376, 'team': 'MIA', 'salary': 8100, 'name': 'Jimmy Butler'}, {'salary': 8700, 'projection': 37.51, 'team': 'MEM', 'name': 'Jaren Jackson', 'id': 1242370, 'positions': 'PF/C'}, {'projection': 37.23, 'name': 'Karl-Anthony Towns', 'id': 1242371, 'team': 'MIN', 'salary': 8600, 'positions': 'PF/C'}, {'id': 1242374, 'name': 'Cade Cunningham', 'positions': 'PG/SG', 'salary': 8300, 'team': 'DET', 'projection': 36.68}, {'team': 'WAS', 'positions': 'SF/PF', 'salary': 7800, 'id': 1242379, 'name': 'Kyle Kuzma', 'projection': 36.58}, {'salary': 8000, 'projection': 35.34, 'name': 'Miles Bridges', 'id': 1242377, 'team': 'CHA', 'positions': 'SF'}, {'positions': 'C', 'name': 'Brook Lopez', 'id': 1242389, 'projection': 35.11, 'salary': 7200, 'team': 'MIL'}, {'team': 'MIA', 'projection': 34.27, 'positions': 'SG', 'id': 1242385, 'name': 'Tyler Herro', 'salary': 7400}, {'projection': 33.26, 'salary': 7100, 'name': 'Bradley Beal', 'positions': 'SG/PG', 'team': 'PHO', 'id': 1242390}, {'id': 1242387, 'salary': 7300, 'positions': 'SG/SF', 'projection': 32.83, 'name': 'Khris Middleton', 'team': 'MIL'}, {'salary': 6900, 'id': 1242393, 'team': 'PHO', 'projection': 32.51, 'name': 'Jusuf Nurkic', 'positions': 'C'}, {'name': 'Jalen Duren', 'team': 'DET', 'positions': 'C', 'salary': 7200, 'id': 1242388, 'projection': 32}, {'positions': 'SG/PG', 'salary': 7500, 'name': 'Jaden Ivey', 'projection': 31.19, 'team': 'DET', 'id': 1242383}, {'id': 1242386, 'salary': 7300, 'projection': 30.6, 'name': 'Jerami Grant', 'positions': 'PF/SF', 'team': 'POR'}, {'salary': 7500, 'projection': 29.89, 'name': 'Malcolm Brogdon', 'positions': 'PG/SG', 'team': 'POR', 'id': 1242384}, {'salary': 5900, 'team': 'MEM', 'projection': 29.53, 'id': 1242416, 'name': 'Xavier Tillman', 'positions': 'C'}, {'salary': 6800, 'positions': 'PG', 'name': 'Tyus Jones', 'projection': 29.22, 'team': 'WAS', 'id': 1242394}, {'salary': 7000, 'positions': 'SG/SF', 'projection': 28.97, 'id': 1242392, 'name': 'Caris LeVert', 'team': 'CLE'}, {'id': 1242395, 'salary': 6800, 'team': 'MEM', 'positions': 'SF/SG', 'name': 'Vince Williams', 'projection': 28.81}, {'id': 1242400, 'salary': 6400, 'team': 'DET', 'name': 'Bojan Bogdanovic', 'projection': 28.7, 'positions': 'SF/PF'}, {'positions': 'C', 'projection': 28.07, 'team': 'WAS', 'id': 1242397, 'name': 'Daniel Gafford', 'salary': 6600}, {'projection': 27.86, 'name': 'Anfernee Simons', 'positions': 'SG/PG', 'team': 'POR', 'salary': 7700, 'id': 1242381}, {'team': 'MIN', 'positions': 'PG', 'id': 1242415, 'name': 'Mike Conley', 'salary': 5900, 'projection': 27.79}, {'team': 'HOU', 'name': 'Jabari Smith', 'positions': 'PF', 'projection': 27.79, 'salary': 6500, 'id': 1242399}, {'projection': 26.88, 'team': 'CHA', 'positions': 'SF', 'salary': 6700, 'name': 'Brandon Miller', 'id': 1242396}, {'projection': 26.71, 'team': 'WAS', 'id': 1242401, 'salary': 6400, 'name': 'Jordan Poole', 'positions': 'PG/SG'}, {'name': 'Jalen Green', 'positions': 'SG/PG', 'projection': 26.54, 'id': 1242406, 'team': 'HOU', 'salary': 6300}, {'salary': 6400, 'positions': 'SG/SF', 'projection': 26.17, 'name': 'Tim Hardaway', 'team': 'DAL', 'id': 1242403}, {'name': 'Grayson Allen', 'salary': 6000, 'positions': 'SG/SF', 'projection': 26.08, 'team': 'PHO', 'id': 1242410}, {'positions': 'PF/C', 'id': 1242407, 'team': 'CHA', 'salary': 6200, 'projection': 25.95, 'name': 'P.J. Washington'}, {'name': 'Deandre Ayton', 'projection': 25.66, 'salary': 7000, 'positions': 'C', 'id': 1242391, 'team': 'POR'}, {'projection': 25.6, 'salary': 6300, 'team': 'WAS', 'id': 1242405, 'positions': 'SF/PF', 'name': 'Deni Avdija'}, {'id': 1242418, 'positions': 'SF/PF', 'projection': 25.43, 'salary': 5800, 'name': 'Jabari Walker', 'team': 'POR'}, {'projection': 24.2, 'positions': 'C/PF', 'team': 'MIN', 'salary': 6000, 'id': 1242411, 'name': 'Naz Reid'}, {'name': 'Alec Burks', 'salary': 5600, 'id': 1242423, 'positions': 'PG/SG', 'team': 'DET', 'projection': 24.15}, {'projection': 23.93, 'team': 'DET', 'id': 1242409, 'positions': 'C/PF', 'salary': 6100, 'name': 'Isaiah Stewart'}, {'id': 1242422, 'projection': 23.82, 'name': 'Luke Kennard', 'positions': 'SG/SF', 'salary': 5700, 'team': 'MEM'}, {'team': 'DAL', 'salary': 6300, 'id': 1242404, 'projection': 23.78, 'name': 'Dereck Lively', 'positions': 'C'}, {'team': 'CHA', 'salary': 5100, 'projection': 23.46, 'name': 'Cody Martin', 'id': 1242437, 'positions': 'SG/PG'}, {'salary': 6100, 'projection': 23.26, 'team': 'MIA', 'id': 1242408, 'name': 'Jaime Jaquez', 'positions': 'SF'}, {'id': 1242412, 'salary': 6000, 'team': 'CHA', 'name': 'Nick Richards', 'projection': 21.9, 'positions': 'C'}, {'salary': 5100, 'name': 'Kyle Anderson', 'team': 'MIN', 'projection': 21.55, 'positions': 'SF/PF', 'id': 1242436}, {'projection': 20.81, 'name': 'Malik Beasley', 'team': 'MIL', 'salary': 4700, 'id': 1242447, 'positions': 'SF/SG'}, {'positions': 'PF/C', 'salary': 5500, 'projection': 20.73, 'name': 'Bobby Portis', 'id': 1242426, 'team': 'MIL'}, {'name': 'Scoot Henderson', 'projection': 20.65, 'salary': 5500, 'team': 'POR', 'positions': 'PG', 'id': 1242425}, {'salary': 5300, 'team': 'DET', 'name': 'Ausar Thompson', 'positions': 'SF/SG', 'id': 1242431, 'projection': 20.52}, {'salary': 5700, 'id': 1242420, 'team': 'CLE', 'projection': 20.29, 'positions': 'SG/SF', 'name': 'Max Strus'}, {'salary': 5500, 'positions': 'SG/SF', 'team': 'HOU', 'projection': 20.14, 'id': 1242427, 'name': 'Dillon Brooks'}, {'positions': 'PG', 'team': 'MIA', 'salary': 7700, 'name': 'Terry Rozier', 'projection': 20, 'id': 1242380}, {'team': 'MIN', 'positions': 'SF/PF', 'salary': 5200, 'id': 1242434, 'name': 'Jaden McDaniels', 'projection': 19.95}, {'team': 'CLE', 'salary': 5600, 'projection': 19.76, 'name': 'Sam Merrill', 'positions': 'SG', 'id': 1242424}, {'name': 'Georges Niang', 'positions': 'PF', 'id': 1242448, 'salary': 4700, 'team': 'CLE', 'projection': 19.41}, {'id': 1242430, 'salary': 5400, 'team': 'DAL', 'projection': 18.88, 'positions': 'SF/PF', 'name': 'Derrick Jones'}, {'team': 'DAL', 'projection': 18.34, 'name': 'Grant Williams', 'positions': 'PF', 'id': 1242456, 'salary': 4500}, {'salary': 4900, 'projection': 18.15, 'id': 1242442, 'name': 'Josh Green', 'team': 'DAL', 'positions': 'SF/SG'}, {'team': 'MIA', 'positions': 'SF/PF', 'id': 1242432, 'projection': 18.13, 'salary': 5200, 'name': 'Caleb Martin'}, {'salary': 5000, 'projection': 18.1, 'id': 1242439, 'positions': 'SF', 'team': 'HOU', 'name': 'Cam Whitmore'}, {'salary': 4900, 'id': 1242443, 'name': 'Isaac Okoro', 'projection': 17.5, 'team': 'CLE', 'positions': 'SF/SG'}, {'id': 1242444, 'team': 'WAS', 'positions': 'SF', 'name': 'Bilal Coulibaly', 'projection': 17.29, 'salary': 4800}, {'team': 'MEM', 'id': 1242438, 'positions': 'PF', 'projection': 16.99, 'name': 'GG Jackson', 'salary': 5000}, {'salary': 4500, 'id': 1242455, 'name': 'David Roddy', 'positions': 'SF/PF', 'team': 'MEM', 'projection': 16.79}, {'positions': 'PF/C', 'name': 'Kevin Love', 'team': 'MIA', 'salary': 4700, 'projection': 16.77, 'id': 1242449}, {'salary': 4900, 'name': 'Nickeil Alexander-Walker', 'projection': 16.41, 'team': 'MIN', 'id': 1242441, 'positions': 'SG/SF'}, {'projection': 16.41, 'salary': 5400, 'name': 'Duop Reath', 'id': 1242428, 'positions': 'C', 'team': 'POR'}, {'projection': 16.04, 'team': 'CLE', 'positions': 'PF/SF', 'salary': 4600, 'name': 'Dean Wade', 'id': 1242453}, {'positions': 'SF/PF', 'name': 'Kevin Knox', 'projection': 16.02, 'team': 'DET', 'id': 1242466, 'salary': 4200}, {'id': 1242446, 'name': 'John Konchar', 'salary': 4800, 'team': 'MEM', 'positions': 'SF', 'projection': 15.15}, {'name': 'Killian Hayes', 'projection': 15, 'id': 1242440, 'team': 'DET', 'positions': 'PG', 'salary': 4900}, {'salary': 4400, 'team': 'POR', 'positions': 'SF/PF', 'name': 'Toumani Camara', 'projection': 14.77, 'id': 1242459}, {'id': 1242462, 'positions': 'SF/SG', 'salary': 4300, 'team': 'MIA', 'name': 'Josh Richardson', 'projection': 14.71}, {'team': 'PHO', 'positions': 'SG/SF', 'projection': 14.7, 'id': 1242457, 'salary': 4500, 'name': 'Eric Gordon'}, {'team': 'MEM', 'projection': 14.49, 'positions': 'SF', 'salary': 4100, 'id': 1242470, 'name': 'Ziaire Williams'}, {'projection': 14.22, 'name': 'Amen Thompson', 'id': 1242398, 'team': 'HOU', 'salary': 6600, 'positions': 'PG/SG'}, {'name': 'Duncan Robinson', 'positions': 'SG/SF', 'projection': 14.18, 'salary': 5100, 'id': 1242435, 'team': 'MIA'}, {'positions': 'PG', 'name': 'Delon Wright', 'projection': 13.95, 'salary': 4700, 'id': 1242451, 'team': 'WAS'}, {'name': 'Marcus Sasser', 'salary': 4600, 'positions': 'PG', 'team': 'DET', 'projection': 13.88, 'id': 1242452}, {'positions': 'PF/SF', 'salary': 4300, 'name': 'Jae Crowder', 'team': 'MIL', 'projection': 13.62, 'id': 1242463}, {'id': 1242461, 'positions': 'PF', 'team': 'MIA', 'salary': 4300, 'projection': 13.59, 'name': 'Nikola Jovic'}, {'positions': 'PF/C', 'projection': 13.5, 'salary': 5900, 'team': 'WAS', 'name': 'Marvin Bagley', 'id': 1242413}, {'projection': 12.97, 'id': 1242464, 'salary': 4200, 'team': 'WAS', 'name': 'Corey Kispert', 'positions': 'SF'}, {'salary': 3800, 'team': 'CHA', 'projection': 12.31, 'name': 'Nick Smith', 'id': 1242485, 'positions': 'PG/SG'}, {'salary': 5900, 'name': 'Dante Exum', 'projection': 12.19, 'id': 1242414, 'team': 'DAL', 'positions': 'SG/PG'}, {'salary': 3800, 'projection': 12.17, 'id': 1242492, 'team': 'POR', 'name': 'Matisse Thybulle', 'positions': 'SF'}, {'name': 'Aaron Holiday', 'team': 'HOU', 'salary': 3900, 'positions': 'PG', 'projection': 11.95, 'id': 1242483}, {'id': 1242496, 'projection': 11.93, 'team': 'HOU', 'name': 'Jeff Green', 'positions': 'SF', 'salary': 3800}, {'positions': 'C', 'projection': 11.49, 'name': 'Mike Muscala', 'salary': 4100, 'team': 'DET', 'id': 1242473}, {'team': 'MIA', 'positions': 'PF/SF', 'id': 1242465, 'name': 'Haywood Highsmith', 'projection': 11.17, 'salary': 4200}, {'projection': 11.14, 'salary': 4100, 'team': 'WAS', 'positions': 'SG', 'id': 1242472, 'name': 'Landry Shamet'}, {'name': 'Pat Connaughton', 'id': 1242489, 'team': 'MIL', 'salary': 3800, 'positions': 'SF/SG', 'projection': 11.12}, {'salary': 3800, 'name': 'Andre Jackson', 'team': 'MIL', 'id': 1242487, 'projection': 10.95, 'positions': 'SG'}, {'positions': 'SF/PF', 'team': 'DET', 'projection': 10.89, 'salary': 3800, 'name': 'Danilo Gallinari', 'id': 1242494}, {'name': 'Drew Eubanks', 'positions': 'C/PF', 'salary': 4500, 'projection': 10.87, 'team': 'PHO', 'id': 1242458}, {'salary': 3900, 'id': 1242479, 'name': "Jae'Sean Tate", 'projection': 10.05, 'positions': 'SF/PF', 'team': 'HOU'}, {'team': 'CHA', 'name': 'JT Thor', 'projection': 9.46, 'positions': 'PF', 'id': 1242488, 'salary': 3800}, {'name': 'Jaden Hardy', 'projection': 9.36, 'positions': 'SG', 'salary': 5200, 'id': 1242433, 'team': 'DAL'}, {'team': 'MEM', 'projection': 9.23, 'id': 1242467, 'name': 'Jacob Gilyard', 'positions': 'PG', 'salary': 4200}, {'salary': 3900, 'projection': 9.21, 'positions': 'SF', 'id': 1242480, 'name': 'Josh Okogie', 'team': 'PHO'}, {'projection': 9.02, 'id': 1242445, 'team': 'CLE', 'positions': 'PG', 'salary': 4800, 'name': 'Craig Porter'}, {'positions': 'PF/C', 'salary': 4000, 'projection': 8.6, 'name': 'Maxi Kleber', 'id': 1242476, 'team': 'DAL'}, {'projection': 8.59, 'salary': 3900, 'id': 1242482, 'team': 'CHA', 'name': 'Ish Smith', 'positions': 'PG'}, {'positions': 'PF', 'name': 'Keita Bates-Diop', 'id': 1242501, 'projection': 8.55, 'salary': 3700, 'team': 'PHO'}, {'salary': 3600, 'team': 'WAS', 'positions': 'SF', 'projection': 8.52, 'name': 'Eugene Omoruyi', 'id': 1242516}, {'name': 'Cameron Payne', 'salary': 4200, 'id': 1242468, 'team': 'MIL', 'positions': 'PG/SG', 'projection': 8.25}, {'name': 'Theo Maledon', 'salary': 3500, 'id': 1242534, 'positions': 'PG', 'team': 'PHO', 'projection': 8.17}, {'salary': 4100, 'team': 'PHO', 'projection': 8.14, 'id': 1242471, 'name': 'Chimezie Metu', 'positions': 'C/PF'}, {'projection': 8.1, 'name': 'Jordan McLaughlin', 'salary': 4000, 'positions': 'PG', 'team': 'MIN', 'id': 1242474}, {'team': 'POR', 'salary': 3700, 'id': 1242506, 'projection': 7.86, 'positions': 'C', 'name': 'Ibou Badji'}, {'salary': 3700, 'team': 'CHA', 'projection': 7.6, 'id': 1242500, 'positions': 'C', 'name': 'Nathan Mensah'}, {'id': 1242499, 'name': 'Isaiah Livers', 'positions': 'PF', 'team': 'WAS', 'salary': 3700, 'projection': 7.31}, {'id': 1242486, 'team': 'POR', 'projection': 7.3, 'name': 'Kris Murray', 'positions': 'SF', 'salary': 3800}, {'salary': 3600, 'name': 'Justin Minaya', 'team': 'POR', 'projection': 6.52, 'positions': 'SF', 'id': 1242517}, {'salary': 4200, 'name': 'James Wiseman', 'id': 1242469, 'projection': 6.35, 'team': 'DET', 'positions': 'C'}, {'projection': 6.04, 'positions': 'SF', 'id': 1242493, 'salary': 3800, 'team': 'WAS', 'name': 'Patrick Baldwin'}, {'salary': 3800, 'projection': 6.01, 'id': 1242497, 'positions': 'C', 'team': 'HOU', 'name': 'Jock Landale'}, {'salary': 4000, 'team': 'DET', 'id': 1242478, 'name': 'Monte Morris', 'projection': 6, 'positions': 'PG'}, {'name': 'Greg Brown', 'projection': 5.88, 'team': 'DAL', 'id': 1242532, 'positions': 'PF', 'salary': 3500}, {'projection': 5.17, 'id': 1242498, 'salary': 3700, 'team': 'POR', 'positions': 'SG', 'name': 'Rayan Rupert'}, {'salary': 3800, 'name': 'Damian Jones', 'id': 1242490, 'team': 'CLE', 'projection': 5, 'positions': 'C'}, {'positions': 'PF', 'id': 1242508, 'team': 'DAL', 'salary': 3600, 'projection': 4.9, 'name': 'Olivier-Maxence Prosper'}, {'positions': 'SG', 'id': 1242503, 'projection': 4.86, 'salary': 3700, 'name': 'Bryce McGowens', 'team': 'CHA'}, {'salary': 3800, 'positions': 'PG', 'projection': 4.75, 'name': 'Shake Milton', 'id': 1242491, 'team': 'MIN'}, {'name': 'Leaky Black', 'projection': 4.63, 'id': 1242510, 'team': 'CHA', 'positions': 'SF', 'salary': 3600}, {'team': 'MEM', 'id': 1242537, 'name': 'Scotty Pippen', 'salary': 3500, 'positions': 'PG', 'projection': 4.57}, {'salary': 3800, 'id': 1242495, 'name': 'Jordan Goodwin', 'team': 'PHO', 'positions': 'PG', 'projection': 4.27}, {'positions': 'SF', 'salary': 3600, 'id': 1242513, 'team': 'PHO', 'name': 'Nassir Little', 'projection': 4.14}, {'id': 1242527, 'team': 'HOU', 'positions': 'SG', 'projection': 4.06, 'salary': 3500, 'name': 'Reggie Bullock'}, {'positions': 'SG', 'team': 'WAS', 'id': 1242528, 'salary': 3500, 'name': 'Jared Butler', 'projection': 3.97}, {'team': 'HOU', 'id': 1242507, 'positions': 'SG', 'projection': 3.93, 'salary': 3600, 'name': 'Nate Williams'}, {'projection': 3.58, 'name': 'Jermaine Samuels', 'id': 1242526, 'salary': 3500, 'team': 'HOU', 'positions': 'SF'}, {'id': 1242539, 'salary': 3500, 'name': 'AJ Green', 'projection': 3.38, 'team': 'MIL', 'positions': 'SG'}, {'positions': 'SF', 'team': 'MIL', 'projection': 3.09, 'salary': 3700, 'name': 'MarJon Beauchamp', 'id': 1242505}, {'team': 'DAL', 'projection': 3.08, 'id': 1242504, 'salary': 3700, 'positions': 'SG', 'name': 'A.J. Lawson'}, {'team': 'CLE', 'salary': 7900, 'positions': 'PG', 'projection': 0, 'name': 'Darius Garland', 'id': 1242378}, {'projection': 0, 'id': 1242382, 'salary': 7600, 'name': 'Evan Mobley', 'positions': 'PF/C', 'team': 'CLE'}, {'id': 1242402, 'salary': 6400, 'name': 'Shaedon Sharpe', 'positions': 'SF/SG', 'projection': 0, 'team': 'POR'}, {'team': 'CHA', 'name': 'Gordon Hayward', 'id': 1242417, 'salary': 5800, 'projection': 0, 'positions': 'SF/SG'}, {'name': 'Mark Williams', 'team': 'CHA', 'salary': 5800, 'id': 1242419, 'projection': 0, 'positions': 'C'}, {'projection': 0, 'positions': 'PF/C', 'name': 'Santi Aldama', 'team': 'MEM', 'salary': 5700, 'id': 1242421}, {'id': 1242429, 'positions': 'SF', 'name': 'Tari Eason', 'salary': 5400, 'team': 'HOU', 'projection': 0}, {'projection': 0, 'team': 'CHA', 'salary': 4700, 'name': 'Kyle Lowry', 'id': 1242450, 'positions': 'PG'}, {'salary': 4600, 'team': 'DAL', 'id': 1242454, 'projection': 0, 'positions': 'C/PF', 'name': 'Dwight Powell'}, {'projection': 0, 'positions': 'PG', 'name': 'Derrick Rose', 'team': 'MEM', 'salary': 4400, 'id': 1242460}, {'name': 'Orlando Robinson', 'positions': 'C', 'salary': 4000, 'projection': 0, 'id': 1242475, 'team': 'MIA'}, {'id': 1242477, 'salary': 4000, 'team': 'PHO', 'projection': 0, 'name': 'Bol Bol', 'positions': 'C'}, {'id': 1242481, 'name': 'Seth Curry', 'salary': 3900, 'team': 'DAL', 'projection': 0, 'positions': 'SG'}, {'positions': 'PG', 'salary': 3900, 'name': 'Frank Ntilikina', 'id': 1242484, 'projection': 0, 'team': 'CHA'}, {'name': 'Thomas Bryant', 'id': 1242502, 'team': 'MIA', 'positions': 'C', 'projection': 0, 'salary': 3700}, {'id': 1242509, 'positions': 'PG', 'projection': 0, 'team': 'MIA', 'salary': 3600, 'name': 'RJ Hampton'}, {'salary': 3600, 'name': 'Ty Jerome', 'projection': 0, 'team': 'CLE', 'id': 1242511, 'positions': 'PG'}, {'id': 1242512, 'name': 'Stanley Umude', 'positions': 'SG', 'salary': 3600, 'projection': 0, 'team': 'DET'}, {'id': 1242514, 'team': 'MIA', 'projection': 0, 'salary': 3600, 'name': 'Jamal Cain', 'positions': 'SF'}, {'salary': 3600, 'positions': 'C', 'name': 'Udoka Azubuike', 'projection': 0, 'team': 'PHO', 'id': 1242515}, {'salary': 3500, 'team': 'DET', 'projection': 0, 'id': 1242518, 'name': 'Malcolm Cazalon', 'positions': 'SG'}, {'id': 1242519, 'name': 'Leonard Miller', 'positions': 'SF', 'salary': 3500, 'team': 'MIN', 'projection': 0}, {'team': 'MIN', 'projection': 0, 'id': 1242520, 'name': 'Jaylen Clark', 'positions': 'SG', 'salary': 3500}, {'salary': 3500, 'id': 1242521, 'positions': 'SG', 'team': 'DET', 'name': 'Jared Rhoden', 'projection': 0}, {'team': 'POR', 'positions': 'C', 'projection': 0, 'salary': 3500, 'name': 'Moses Brown', 'id': 1242522}, {'team': 'CLE', 'positions': 'SF', 'salary': 3500, 'id': 1242523, 'projection': 0, 'name': 'Emoni Bates'}, {'team': 'CHA', 'id': 1242524, 'name': 'Amari Bailey', 'projection': 0, 'positions': 'PG', 'salary': 3500}, {'salary': 3500, 'positions': 'SF', 'team': 'MIL', 'id': 1242525, 'projection': 0, 'name': 'Chris Livingston'}, {'salary': 3500, 'team': 'MIN', 'positions': 'C', 'name': 'Luka Garza', 'projection': 0, 'id': 1242529}, {'salary': 3500, 'projection': 0, 'team': 'MEM', 'name': 'Marcus Smart', 'id': 1242530, 'positions': 'PG'}, {'name': 'James Bouknight', 'salary': 3500, 'team': 'CHA', 'id': 1242531, 'projection': 0, 'positions': 'SG'}, {'projection': 0, 'positions': 'C', 'name': 'Steven Adams', 'salary': 3500, 'team': 'MEM', 'id': 1242533}, {'salary': 3500, 'team': 'DAL', 'projection': 0, 'positions': 'PG', 'id': 1242535, 'name': 'Brandon Williams'}, {'id': 1242536, 'salary': 3500, 'team': 'WAS', 'name': 'Anthony Gill', 'projection': 0, 'positions': 'PF'}, {'team': 'MIL', 'salary': 3500, 'positions': 'C', 'name': 'Robin Lopez', 'id': 1242538, 'projection': 0}, {'projection': 0, 'name': 'Cole Swider', 'salary': 3500, 'id': 1242540, 'team': 'MIA', 'positions': 'SF'}, {'name': 'Tristan Thompson', 'salary': 3500, 'positions': 'C', 'projection': 0, 'team': 'CLE', 'id': 1242541}, {'salary': 3500, 'name': 'Markieff Morris', 'projection': 0, 'id': 1242542, 'team': 'DAL', 'positions': 'PF'}, {'positions': 'SF', 'projection': 0, 'name': 'Troy Brown', 'team': 'MIN', 'salary': 3500, 'id': 1242543}, {'id': 1242544, 'team': 'MIN', 'positions': 'PG', 'salary': 3500, 'projection': 0, 'name': 'Daishen Nix'}, {'salary': 3500, 'name': 'Hamidou Diallo', 'positions': 'SG', 'projection': 0, 'id': 1242545, 'team': 'WAS'}, {'id': 1242546, 'projection': 0, 'name': 'Robert Williams', 'team': 'POR', 'salary': 3500, 'positions': 'C'}, {'salary': 3500, 'projection': 0, 'id': 1242547, 'team': 'MEM', 'positions': 'PG', 'name': 'Jaylen Nowell'}, {'team': 'MEM', 'positions': 'PF', 'id': 1242548, 'name': 'Jake LaRavia', 'projection': 0, 'salary': 3500}, {'name': 'Johnny Davis', 'salary': 3500, 'team': 'WAS', 'id': 1242549, 'positions': 'SG', 'projection': 0}, {'salary': 3500, 'id': 1242550, 'team': 'PHO', 'name': 'Yuta Watanabe', 'projection': 0, 'positions': 'SF'}, {'name': 'TyTy Washington', 'positions': 'PG', 'id': 1242551, 'team': 'MIL', 'projection': 0, 'salary': 3500}, {'positions': 'SG', 'projection': 0, 'salary': 3500, 'id': 1242552, 'team': 'MIN', 'name': 'Wendell Moore'}, {'name': 'Jules Bernard', 'salary': 3500, 'id': 1242553, 'positions': 'SG', 'team': 'WAS', 'projection': 0}, {'salary': 3500, 'id': 1242554, 'name': 'Josh Minott', 'team': 'MIN', 'positions': 'SF', 'projection': 0}, {'salary': 3500, 'positions': 'PF', 'team': 'CLE', 'id': 1242555, 'name': 'Isaiah Mobley', 'projection': 0}, {'id': 1242556, 'positions': 'PG', 'name': 'Ja Morant', 'salary': 3500, 'team': 'MEM', 'projection': 0}, {'salary': 3500, 'team': 'MIL', 'projection': 0, 'id': 1242557, 'name': 'Thanasis Antetokounmpo', 'positions': 'SF'}, {'id': 1242558, 'name': 'Pete Nance', 'projection': 0, 'team': 'CLE', 'positions': 'PF', 'salary': 3500}, {'id': 1242559, 'positions': 'PF/C', 'projection': 0, 'salary': 3500, 'team': 'MEM', 'name': 'Brandon Clarke'}, {'team': 'MIA', 'positions': 'SG', 'name': 'Dru Smith', 'projection': 0, 'id': 1242560, 'salary': 3500}, {'name': 'Victor Oladipo', 'team': 'HOU', 'projection': 0, 'positions': 'SG', 'salary': 3500, 'id': 1242561}, {'team': 'HOU', 'salary': 3500, 'id': 1242562, 'name': 'Nate Hinton', 'projection': 0, 'positions': 'SG'}, {'projection': 0, 'name': 'Boban Marjanovic', 'team': 'HOU', 'salary': 3500, 'id': 1242563, 'positions': 'C'}, {'positions': 'C', 'projection': 0, 'name': 'Trey Jemison', 'salary': 3500, 'team': 'WAS', 'id': 1242564}, {'team': 'DAL', 'positions': 'C', 'salary': 3500, 'name': 'Richaun Holmes', 'projection': 0, 'id': 1242565}, {'projection': 0, 'positions': 'PG', 'id': 1242566, 'salary': 3500, 'name': 'Saben Lee', 'team': 'PHO'}, {'name': 'Desmond Bane', 'team': 'MEM', 'projection': 0, 'id': 1242567, 'positions': 'SG/SF', 'salary': 3500}, {'positions': 'SG', 'name': 'Taze Moore', 'id': 1242568, 'salary': 3500, 'projection': 0, 'team': 'POR'}, {'id': 1242569, 'positions': 'SG', 'name': 'Damion Lee', 'salary': 3500, 'team': 'PHO', 'projection': 0}, {'projection': 0, 'team': 'DET', 'id': 1242570, 'positions': 'SG', 'salary': 3500, 'name': 'Joe Harris'}]
   
    players = initPlayersDictionary(playerList)
    teams = initTeamList(list=players)
    
    
    # Variable constraint
    max_budget = 60000
    max_players_from_any_team = 4
    num_lineups = 10
    unique_players = 1
    Global_Ownership = 1
    num_players_to_stack = 4

    print("\n")
    lineups = []
    for lineup_num in range(num_lineups):
        # Create a linear programming problem
        prob = LpProblem(f"DFS_Lineup_Optimization_{lineup_num + 1}", LpMaximize)
        
        # Define decision variables
        player_vars = {(playerId): LpVariable(name=f"{playerId}", cat='Binary') for playerId in players.keys()}
        
        position_vars = {(playerId, position): LpVariable(name=f"{playerId}_{position}_var", cat='Binary') for playerId in players.keys() for position in players[playerId].positions}

        team_vars = {team: LpVariable(name=f"{team}_var", cat='Binary') for team in teams}


        # Objective function (maximize total projected points)
        prob += lpSum([players[playerId].projection * player_vars[playerId] for playerId in player_vars])

        # Budget constraint
        prob += lpSum([players[playerId].salary * player_vars[playerId] for playerId in player_vars]) <= max_budget

        #Team constraint
        for team in teams:
            prob += lpSum([player_vars[playerId] for playerId in player_vars if players[playerId].team == team]) <= max_players_from_any_team

        
        
        # Team constraint: At least 4 players from the same team in the lineup
        for team in teams:
            prob += lpSum(player_vars[playerId] for playerId in players.keys() if players[playerId].team == team) >= num_players_to_stack * team_vars[team]

        # Ensure that at least one team is selected
        prob += lpSum(team_vars.values()) >= 1


        # position Constraint
        position_limits = {'PG': 2, 'SG': 2, 'SF': 2, 'PF': 2, 'C': 1}
        for position, limit in position_limits.items():
            prob += lpSum(position_vars.get((playerId, position), 0) for playerId in players.keys()) == limit

        # Constraint 3: Each player is assigned to at most one position
        for playerId in players.keys():
            prob += lpSum(position_vars.get((playerId, position), 0) for position in players[playerId].positions) <= 1

        # Constraint 4: Link player and position variables
        for playerId in players.keys():
            for position in players[playerId].positions:
                prob += position_vars[(playerId, position)] <= player_vars[playerId]

        if lineup_num > 0:
            for playerId in players.keys():
                prob += (1 + players[playerId].ownership) * player_vars[playerId] <= Global_Ownership * num_lineups

            for lineup in lineups:
                #prev_lineup_players = [player for pos, mPlayers in lineupSlots.items() for player in mPlayers if player_vars[player, pos].value() == 1]
                prob += lpSum([player_vars[playerId] for playerId in player_vars if playerId not in lineup]) >= unique_players

      

        # Solve problem
        prob.solve(PULP_CBC_CMD(msg=0))

        # Print the results for each lineup
        positionDictionary = {}
        lineup = []
        print("Status:", prob.status)
        print(f"Optimal Lineup {lineup_num + 1}:")
        totalPoints = 0
        totalSalary = 0
        totalCount = 0
        for playerId in player_vars:
            for position in players[playerId].positions:
                if position_vars[playerId, position].value() == 1:
                    
                    totalPoints = totalPoints + players[playerId].projection
                    totalSalary = totalSalary + players[playerId].salary
                    totalCount = totalCount + 1
                    lineup.append(playerId)
                    positionDictionary[playerId] = position
                    players[playerId].ownership += 1
        
        
        orderedLineup = orderLineup(lineup=lineup,dictionary=positionDictionary)
        
        for playerId in orderedLineup:
            print(f"{players[playerId].name}, {players[playerId].team}")

        print("Total Projection: ", totalPoints, " Total Salary:  $", totalSalary, " Count: ", totalCount, "\n")

        lineups.append(orderedLineup)
    
    print("Ownership report")
    for playerId,player in players.items():
        if(player.ownership > 0):
            print(player.name + " - " + f"{float(100 * (player.ownership/num_lineups))}" + "%")
    


