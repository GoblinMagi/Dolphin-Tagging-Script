#! python3
# grabberscipt.py - Automatically tags images from log file created by Grabber and relocates them

import os, shutil, logging, re, subprocess
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

process_dir = Path.home() / 'Pictures' / 'grabber' / 'processing'
complete_dir = Path.home() / 'Pictures' / 'grabber' / 'complete'
logging.debug(f"Processing directory: {process_dir}")
logging.debug(f"Completed directory: {complete_dir}")

image_reg = re.compile(r".*[^.txt]$")
log_reg = re.compile(r".*(.txt)$")

if Path.is_dir(process_dir) == False:
	os.makedirs(str(process_dir))
	print(f"Created processing directory '{process_dir}'")
	print("Please ensure that your Grabber downloads images to this directory.\n")
	logging.debug(f"Created processing directory: {process_dir}")
if Path.is_dir(complete_dir) == False:
	Path.mkdir(complete_dir)
	print(f"Created complete directory '{complete_dir}'")
	print("Your tagged images will appear in this directory.\n")
	logging.debug(f"Created complete directory: {complete_dir}")

while True:
	process_contents = os.listdir(process_dir)
	logging.debug(f"Processing directory contains: {str(process_contents)}")
	working_log = ' '
	working_file = 'x'	
	for i in range(len(process_contents)):
		logging.debug(f"{process_contents[i]}")
		image_mo = image_reg.search(process_contents[i])	
		log_mo = log_reg.search(process_contents[i])
		if image_mo == None:
			if log_mo == None:
				break
			else:
				working_log = os.path.abspath(Path(process_dir / log_mo.group()))
				logging.debug(f"Log found: {working_log}")
		else:
			working_file = os.path.abspath(Path(process_dir / image_mo.group()))
			logging.debug(f"Image found: {working_file}")

	while working_file and working_log:
		if Path(working_file).stem == Path(working_log).stem:
			print(f"Log found: {working_log}")
			print(f"Image found: {working_file}")
			print("Found log and image match!")
			logging.debug("Found log and image match!")
			log_file = open(working_log, 'r')
			log_contents = log_file.read()
			logging.debug(f"Log contents: {log_contents}")
			subprocess.run(["setfattr", "-n", "user.xdg.tags", "-v", log_contents, working_file])
			os.unlink(working_log)
			print(f"Image {Path(working_file).stem} tagged succesfully.")
			working_log = ' '
			shutil.move(working_file, complete_dir)
			print("Image moved to completed folder.\n")
			break
		else:
			break
