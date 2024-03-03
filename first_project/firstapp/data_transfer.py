import sqlite3 as sq 
import pandas as pd 
#from .models import Stocks

def connect_sql():
    df = pd.read_csv(r"C:\Users\user\Videos\general-pos\first_project\firstapp\data.csv")
    return df

