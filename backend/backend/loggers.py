import logging
import os

project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_directory = os.path.join(project_directory, 'backend', 'logs')

if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
log_file_path = os.path.join(logs_directory, 'my_logs.log')


my_logger = logging.getLogger(__name__)
my_logger.setLevel(logging.INFO)


file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)


my_logger.addHandler(file_handler)
logging.root.handlers = []
logging.basicConfig(level=logging.WARNING)