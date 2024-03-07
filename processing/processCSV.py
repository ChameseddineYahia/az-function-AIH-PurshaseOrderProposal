import pandas as pd
import json
import logging      
import math
from config import flow_config






class ProcessCSV():
    def __init__(self):
        pass
        
    def format_columns(self,columns):
        date_columns = flow_config["date_fields"]
        columns = ', '.join(
                        ':' + key if key not in date_columns  else
                            f'TO_DATE(:{key}, \'DD-MON-YY HH24:MI:SS\')'
                            for key in columns
                            )
        
        return columns
    def replace_nan_with_none(self,value):
        return None if isinstance(value, float) and math.isnan(value) else value
   

    def process(self, element):
        df = pd.read_csv(element,sep=';')
        autogenerated_columns = [col for col in df.columns if col.startswith('Unnamed:')]
        if 'STATUS' in [column.upper() for column in df.columns]:
        # Drop the 'status' column
            df = df.drop('Status', axis=1)
        df = df.drop(columns=autogenerated_columns, errors='ignore')
        df = df.applymap(self.replace_nan_with_none)
        
        columns_normal = df.columns.tolist()

        json_string = df.to_json(orient='records')
        rows = json.loads(json_string)  
        columns = self.format_columns(columns_normal)

        return { "columns_formatted":columns, "columns_normal":columns_normal, "rows":rows , "df" : df }