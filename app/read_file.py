import pandas as pd
import chardet
from fastapi import UploadFile
import io

async def read_file_to_df(file: UploadFile):

    if file.filename.endswith('.csv'):
        file_contents = await file.read()
        result = chardet.detect(file_contents)
        file_encoding = result['encoding']
        loaded_df = pd.read_csv(io.BytesIO(file_contents), encoding=file_encoding)
     
    elif file.filename.endswith('.xlsx'):
        file_contents = await file.read()
        loaded_df = pd.read_excel(io.BytesIO(file_contents))
        
        polish_chars = "ąćęłńóźż"
        ascii_chars = "acelnozz"
        trans_table = str.maketrans(polish_chars + polish_chars.upper(), ascii_chars + ascii_chars.upper())
        loaded_df.columns = [col.translate(trans_table) for col in loaded_df.columns]

    else:
        raise ValueError("Unsupported file type")
    
    def replace_and_remove(value):
        if isinstance(value, str):
            return value.replace(' ', '_').replace('(', '').replace(')', '').replace('.', '')
        else:
            return value

    loaded_df = loaded_df.map(replace_and_remove)

    # replacing spaces with underscores and converting to lowercase
    loaded_df.columns = ['_'.join(col.split(' ')).lower() for col in loaded_df.columns]

    return loaded_df

