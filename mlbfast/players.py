import pandas as pd
from pandas import json_normalize
import json
from mlbfast.dl_utils import download
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


def searchMlbPlayers(search="",isActive=""):
	"""
	Searches for an MLB player in the MLBAM API.
	
	Args:
	search (string):
		Inputted string of the player(s) the user is intending to search.
		If there is nothin inputted, nothing will be searched.
	
	isActive (string, optional):
		If called, it will specify if you want active players, or innactive players
		in your search.

		If you want active players, set isActive to "Y" or "Yes".

		If you want inactive players, set isActive to "N" or "No".
	"""
	pullCopyrightInfo()
	searchURL = "http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'"
	
	p_df = pd.DataFrame()
	main_df = pd.DataFrame()

	if len(isActive) == 0:
		#print('Searching for all MLB players.')
		print('')
	elif isActive.lower() == "y" or isActive.lower() == "yes":
		searchURL = searchURL + "&active_sw='Y'"
	elif isActive.lower() == "n" or isActive.lower() == "no":
		searchURL = searchURL + "&active_sw='N'"
	else:
		print('Improper input for the isActive input. \nIf you want active players, set isActive to "Y" or "Yes". \nIf you want inactive players, set isActive to "N" or "No".\n\nIn the meantime, your search will search for all players in MLB history.')

	if len(search) > 0:
		print(f"Searching for a player nammed \"{search}\".")
		
		searchURL= searchURL + f"&name_part='{search}%25'"
		
		
		#searchURL = urllib.parse.quote_plus(str(searchURL))
		resp = download(searchURL)

		
		resp_str = str(resp, 'UTF-8')
		#print(resp_str)

		resp_json = json.loads(resp_str)
		result_count = int(resp_json['search_player_all']['queryResults']['totalSize'])
		if result_count > 0:
			print(f'{result_count} players found,\nParsing results into a dataframe.')
			#players = resp_json['search_player_all']['queryResults']['row']
			for i in tqdm(resp_json['search_player_all']['queryResults']['row']):
				#print(i)
				#print(i['name_display_first_last'])
				#data = {
				#'player_id' : i['player_id']
				#,'team_id' : i['team_id']
				#,'name_full' : i['name_display_first_last']
				#,'name_first' : i['name_first']
				#,'name_last' : i['name_last']
				#,'position' : i['position']
				#,'college' : i['college']
				#,'height_feet' : i['height_feet']
				#,'height_inches' : i['height_inches']
				#,'height_feet_inches' : (i['height_feet'] + "\"" + i['height_inches'] + "\'")
				#,'weight' : i['weight']
				#,'name_display_roster' : i['name_display_roster']
				#,'sport_code' : i['sport_code']
				#,'bats' : i['bats']
				#,'throws' : i['throws']
				#,'team_code' : i['team_code']
				#,'birth_city' : i['birth_city']
				#,'birth_country' : i['birth_country']
				#,'sport_code' : i['sport_code']
				#,'pro_debut_date' : i['pro_debut_date']
				#,'team_full' : i['team_full']
				#,'team_abbrev' : i['team_abbrev']
				#,'birth_date' : i['birth_date']
				#,'birth_state' : i['birth_state']
				#,'name_display_last_first' : i['name_display_last_first']
				#,'position_id' : i['position_id']
				#,'high_school' : i['high_school']
				#,'name_use' : i['name_use']
				#,'service_years' : i['service_years']
				#,'active_sw' : i['active_sw']
				#}
				#p_df = pd.DataFrame(data, index=[0])
				#p_df = pd.DataFrame([data])
				
				p_df = json_normalize(resp_json['search_player_all']['queryResults']['row']) 
				main_df = pd.concat([p_df,main_df],ignore_index=True)
		else:
			print(f'No results found for {search}. \nTry a diffrient search for better results.')
		
		return main_df
		

	else:
		print("To search for MLB players in the MLBAM API, you must include text relating to the player you're searching for.")

def getPlayerInfo(playerID=0):
	'''
	Retrives the player info for an MLB player, given a proper MLBAM ID

	Args:
	
	playerID (int):
		Required paramater. If no playerID is provided, the function wil not work.
	'''
	pullCopyrightInfo()
	#p_df = pd.DataFrame()
	main_df = pd.DataFrame()
	
	searchURL = "http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id="

	if playerID < 1:
		print('You must provide a playerID. Without a proper playerID, this function will not work.')
		return None
	else:
		searchURL= searchURL + f"\'{playerID}\'%27"
		
		
		#searchURL = urllib.parse.quote_plus(str(searchURL))
		resp = download(searchURL)

		print(searchURL)
		resp_str = str(resp, 'UTF-8')
		print(resp_str)

		resp_json = json.loads(resp_str)
		try:
			result_count = int(resp_json['player_info']['queryResults']['totalSize'])
		except:
			result_count = 0

		if result_count > 0:
			print(resp_json['player_info']['queryResults']['row'])

			print(f'{result_count} players found,\nParsing results into a dataframe.')
			#players = resp_json['search_player_all']['queryResults']['row']
			main_df = json_normalize(resp_json['player_info']['queryResults']['row']) 
			print('Done')
		else:
			print(f'No results found for the provided playerID. \nTry a diffrient search for better results.')
		
		return main_df

def getPlayerTeams(playerID=0,season=0):
	'''
	Retrives the player info for an MLB player, given a proper MLBAM ID

	Args:
	
	playerID (int):
		Required paramater. If no playerID is provided, the function wil not work.
	'''
	pullCopyrightInfo()
	#p_df = pd.DataFrame()
	main_df = pd.DataFrame()
	
	searchURL = "http://lookup-service-prod.mlb.com/json/named.player_teams.bam?"

	if season >1 and season < 1860:
		print('Enter a valid season. Baseball wasn\'t really a thing in the year you spefified.')
	elif season > 1860:
		searchURL = searchURL + f'season=\'{season}\'&'
	else:
		print('Searching for all the teams this player has played on')

	if playerID < 1:
		print('You must provide a playerID. Without a proper playerID, this function will not work.')
		return None
	else:
		searchURL= searchURL + f"player_id=\'{playerID}\'"
		
		
		#searchURL = urllib.parse.quote_plus(str(searchURL))
		resp = download(searchURL)

		print(searchURL)
		resp_str = str(resp, 'UTF-8')
		print(resp_str)

		resp_json = json.loads(resp_str)
		try:
			result_count = int(resp_json['player_teams']['queryResults']['totalSize'])
		except:
			result_count = 0

		if result_count > 0:
			#print(resp_json['player_teams']['queryResults']['row'])

			print(f'{result_count} players found,\nParsing results into a dataframe.')
			#players = resp_json['search_player_all']['queryResults']['row']
			main_df = json_normalize(resp_json['player_teams']['queryResults']['row']) 
			print('Done')
		else:
			print(f'No results found for the provided playerID. \nTry a diffrient search for better results.')
		
		return main_df

def main():
	pullCopyrightInfo()

if __name__ == "__main__":
	main()