import logging
import os
from datetime import datetime

# Logger File
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # Here .log is an extension to save the datetime file

# Saving my log file
log_path=os.path.join(os.getcwd(),"logs") # getcwd means get current working directory
os.makedirs(log_path,exist_ok=True) # Creating a folder after giving a path

# Inside a logs folder we are creating a .log file
LOG_FILEPATH=os.path.join(log_path,LOG_FILE)

# Creating an object for logging
logging.basicConfig(level=logging.INFO, # It is not going to capture the information below the info
                    filename=LOG_FILEPATH,
                    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)


