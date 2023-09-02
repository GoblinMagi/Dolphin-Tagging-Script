#! python3
# grabberscipt.py - Automatically tags images from log file created by Grabber and relocates them

import os, shutil, logging, re, subprocess
from pathlib import Path

# Initiate logging. Comment out disable for logs.
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

# Define the "Processing" and "Completed" directories.
process_dir = Path.home() / 'Pictures' / 'grabber' / 'processing'
complete_dir = Path.home() / 'Pictures' / 'grabber' / 'complete'
logging.debug(f"Processing directory: {process_dir}")
logging.debug(f"Completed directory: {complete_dir}")

# Define regular expressions to identify image files and log files.
image_reg = re.compile(r".*[^.txt]$")
log_reg = re.compile(r".*(.txt)$")

# Create the required directories in user's "Pictures" directory if they do not already exist.
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

# Initiate the main program loop that will search the processing directory for files while running.
while True:

	# Collect the contents of the directory.
	process_contents = os.listdir(process_dir)
	logging.debug(f"Processing directory contains: {str(process_contents)}")
	
	# Empty variables at start of loop to avoid false matches.
	working_log = ' '
	working_file = 'x'	

	# Search each item and identify image files or log files.
	for i in range(len(process_contents)):
		logging.debug(f"{process_contents[i]}")
		
		# Create match object based on file type
		image_mo = image_reg.search(process_contents[i])	
		log_mo = log_reg.search(process_contents[i])

		if image_mo == None:
			if log_mo == None:
				break
			else:
				# Store the absolute path of the log file
				working_log = os.path.abspath(Path(process_dir / log_mo.group()))
				logging.debug(f"Log found: {working_log}")
		else:
			# Store the absolute path of the image file
			working_file = os.path.abspath(Path(process_dir / image_mo.group()))
			logging.debug(f"Image found: {working_file}")

	while working_file and working_log:

		# Once the appropriate files are defined, check that they match
		if Path(working_file).stem == Path(working_log).stem:
			print(f"Log found: {working_log}")
			print(f"Image found: {working_file}")
			print("Found log and image match!")
			logging.debug("Found log and image match!")

			# Obtain the contents of the log file
			log_file = open(working_log, 'r')
			log_contents = log_file.read()
			logging.debug(f"Log contents: {log_contents}")

			# Set the tags from the log contents
			subprocess.run(["setfattr", "-n", "user.xdg.tags", "-v", log_contents, working_file])
			
			# Remove the log file and move the tagged image
			os.unlink(working_log)
			print(f"Image {Path(working_file).stem} tagged succesfully.")
			shutil.move(working_file, complete_dir)
			print("Image moved to completed folder.\n")
			break

		else:
			break
