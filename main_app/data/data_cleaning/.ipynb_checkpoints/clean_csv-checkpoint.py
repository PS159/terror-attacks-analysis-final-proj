import pandas as pd

from main_app.app_variables.variables import MAIN_CSV_DS_PATH


df = pd.read_csv(MAIN_CSV_DS_PATH, encoding='latin-1', low_memory=False)





