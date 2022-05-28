## Script: games.py
## Author: Joseph Armstrong (armstjc)

import pandas as pd
from pandas import json_normalize
import json
from mlbfast.dl_utils import download
from datetime import datetime
from tqdm import tqdm
from urllib.error import URLError, HTTPError, ContentTooShortError
import urllib.parse
import os

def pullCopyrightInfo(saveFile=False,returnFile=False):
	"""
	Displays the copyright info for the MLBAM API.

	Args:
	saveFile (boolean) = False
		If saveFile is set to True, the copyright file generated is saved.

	returnFile (boolean) = False
		If returnFile is set to True, the copyright file is returned.
	"""
	url = "http://gdx.mlb.com/components/copyright.txt"
	resp = download(url=url)

	l_string = str(resp, 'UTF-8')
	if resp is not None:
		with open("mlbam_copyright.txt","w+" ,encoding = "utf-8") as file:
			file.writelines(str(l_string))

		with open("mlbam_copyright.txt", "r" ,encoding = "utf-8") as file:
			mlbam = file.read()

		if saveFile == False:
			if os.path.exists("mlbam_copyright.txt"):
				os.remove("mlbam_copyright.txt")
			else:
				pass
		else:
			pass
		print(mlbam)

		if returnFile == True:
			return mlbam
		else:
			pass


	else:
		print('Could not connect to the internet. \nPlease fix this issue to be able to use this package.')


def getGamesInSeason(season=0,gameType="R"):
	'''
	Retrives the player info for an MLB player, given a proper MLBAM ID

	Args:
	
	playerID (int):
		Required paramater. If no playerID is provided, the function wil not work.
	'''
	pullCopyrightInfo()
	#p_df = pd.DataFrame()
	main_df = pd.DataFrame()
	
	searchURL = "http://lookup-service-prod.mlb.com/json/named.org_game_type_date_info.bam?current_sw='Y'&sport_code='mlb'&"

	if len(gameType) >1:
		print('Check your input for seasonType. Searching for regular season stats instead.')
		gameType = "R"
		searchURL = searchURL  + f'game_type=\'{gameType}\'&'
	else:
		searchURL = searchURL  + f'game_type=\'{gameType}\'&'

	now = datetime.now()
	if season < 1860:
		print('Please input a proper year. The search will continue with the current year instead.')
		season = int(now.year)
		searchURL = searchURL  + f'season=\'{season}\''
	elif int(now.year) < season:
		print('Please input a proper year. The search will continue with the current year instead.')
		season = int(now.year)
		searchURL = searchURL  + f'season=\'{season}\''
	else:
		searchURL = searchURL  + f'season=\'{season}\''

	resp = download(searchURL)

	print(searchURL)
	resp_str = str(resp, 'UTF-8')
	print(resp_str)

	resp_json = json.loads(resp_str)
	try:
		result_count = int(resp_json['org_game_type_date_info']['queryResults']['totalSize'])
	except:
		result_count = 0

	if result_count > 0:
		#print(resp_json['player_teams']['queryResults']['row'])

		print(f'{result_count} statlines found,\nParsing results into a dataframe.')
		#players = resp_json['search_player_all']['queryResults']['row']
		main_df = json_normalize(resp_json['org_game_type_date_info']['queryResults']['row']) 
		print('Done')
	else:
		print(f'No results found for the provided playerID. \nTry a diffrient search for better results.')
		
	return main_df