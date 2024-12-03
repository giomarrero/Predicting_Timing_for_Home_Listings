import pandas as pd
import numpy as np
import tensorflow as tf
import sqlite3
import requests
from datetime import datetime
import logging

DIR_MAIN_FILE = '../../Data/data_lake_raw/RDC_Inventory_Core_Metrics_Zip_History.csv'


class Process_Data:
    def __init__(self, realtor_df_loc : str = DIR_MAIN_FILE, db_name = 'HOUSING.db') -> None:
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.df = pd.read_csv(DIR_MAIN_FILE)
        self.df['month_date_yyyymm'] = self.df['month_date_yyyymm'].astype(int)
    
    @staticmethod
    def dtype_to_sql(dtype):
        if pd.api.types.is_integer_dtype(dtype):
            return 'INTEGER'
        elif pd.api.types.is_float_dtype(dtype):
            return 'REAL'
        elif pd.api.types.is_object_dtype(dtype):
            return 'TEXT'
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return 'TIMESTAMP'
        else:
            return 'TEXT' 
        
    @classmethod
    def add_delta(self) -> None:
        self.cursor.execute("SELECT MAX(month_date_yyyymm) FROM realtor")
        max_date = self.cursor.fetchone()[0]
        if self.df.iloc[0,0] > max_date:
            df_cleaned = self.df[self.df['month_date_yyyymm']>max_date]
            
            df_cleaned.to_sql(
                    'Realtor',
                    self.conn,
                    if_exists='replace',
                    index=False,
                    dtype={col: self.dtype_to_sql(dtype) for col, dtype in zip(df_cleaned.columns, df_cleaned.dtypes)}
                )
            
        
        return
        
    
    
    
    def __del__(self) ->None:
        self.conn.close()
        self.cursor.close()
        

    
class Add_Ancilory_Data(Process_Data):
    def __init__(self, realtor_df_loc: str = DIR_MAIN_FILE, db_name='HOUSING.db', 
                 series_ids:list = ['CPIAUCSL', 'FEDFUNDS', 'UMCSENT', 'RSXFS', 'UNRATE', 'DGS10','M2','BOPGSTB','HOUST','PI'],
                 API_KEY:str = '6bf8895c846d89aeaec6a40b739746ce', endpoint:str = 'https://api.stlouisfed.org/fred/series/observations' ) -> None:
        super().__init__(realtor_df_loc, db_name)
        self.api_key = API_KEY
        self.endpoint = endpoint
        self.ids = series_ids
    
    @staticmethod
    def convert_date_format(date_str):
        return int(datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y%m'))
    
    @classmethod
    def add_other_tables(self) -> None:        

        for series_id in self.ids:
            response = requests.get(self.endpoint, params={
                'series_id': series_id,
                'api_key': self.api_key,
                'file_type': 'json'
            })
            data = response.json()
            
            df = pd.DataFrame(data['observations'])
            
            
            df['date'] = df['date'].apply(self.convert_date_format())
            
            self.cursor.execute(f"SELECT MAX(date) FROM {series_id}")
            max_date = self.cursor.fetchone()[0]
            
            max_df_date = df['date'].max()
            
            if max_df_date > max_date: 
                df_to_append = df[df['date']>max_date]
            
                df_to_append.to_sql(series_id, self.conn, if_exists='append', index=False, dtype={
                    'date': 'INTEGER',
                    'value': 'REAL'
                })
