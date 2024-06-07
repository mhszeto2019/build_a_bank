from fastapi import FastAPI,Request
import pandas as pd
import csv 

from app.ledger import get_ledger_balance
from app.transaction import get_transaction_balance

import os.path as path

app = FastAPI()

filename = './db/account.csv'

# helper functions to insert data into desired file - this can be reused in the future
def create_new_file(input_df, filename):
    with open(filename, 'w') as f:
        input_df.to_csv(filename, header=True, columns= ['account_id','account_name'],index=False)
    return True

def save_to_file(input_df, filename):
    
    if path.isfile(filename) == True:
        ### append only if not exists, to avoid churning
        try:
            return update_existing_file(input_df, filename)
        except Exception as e:
            return False
    else:
        return create_new_file(input_df, filename)

def update_existing_file(input_df, filename):
        existing_df = pd.read_csv(filename)  
        if len(input_df) == 0:
            return False
        # open the file in append mode
        with open(filename, 'a') as f:
            input_df.to_csv(f, header=False,index=False)

        return True


@app.get("/get_account_details_by_account_id/")
async def get_account_details_by_account_id(account_id: str):
    # any kind of further df manipulation can be done here
    try:
        df = pd.read_csv('../db/account.csv')
        print(df[df['account_id'] ==account_id])
        balance = get_ledger_balance(account_id) + get_transaction_balance(account_id)
        print(balance)
    except FileNotFoundError:
        fieldnames = None


@app.post("/add_account")
async def get_settlement_rates(request : Request):

    # row to be inserted into db
    row = await request.json()
    input_df = pd.DataFrame(row,index=[0])
    account_id = row['account_id']
    existing_df = pd.read_csv(filename)

    if account_id in existing_df['account_id'].values:
        raise ValueError("Account created")
    # append to db
    save_to_file(input_df,filename)
    
