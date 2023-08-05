import requests
from pathlib import Path
import os.path as pa
import os
import templ8.programstate as ps

def login():
	loginpath = Path.home() / ".templ8rc"
	lines = open(loginpath, "r").readlines()
	return lines[0].rstrip()
	

def neo():
	state = ps.ProgramState()
	apikey = login()
	fl = {}
	for subdir, dirs, files in os.walk(state.output_folder):
		for file in files:
			if os.path.splitext(file)[1] != "":
				print(file)
				path = Path(pa.join(subdir, file))
				from_root = Path(*path.parts[1:])
				fl[str(from_root).replace(os.sep, '/')] = open(path, "rb").read()
	endpoint = f"https://neocities.org/api/upload"
	response = requests.post(
		endpoint,
		headers={"Authorization": f"Bearer {apikey}"},
		files=fl,
	)

	print("Response: ", response.status_code)
	print("Response: ", response.text)
	

			

