from fastapi import FastAPI,Request
import pandas as pd
import os.path as path
import csv 

# from app.ledger import get_ledger_balance
# from app.transaction import get_transaction_balance

from app.util import create_new_file,save_to_file,update_existing_file,get_ledger_balance,get_transaction_balance


app = FastAPI()

filename = './db/account.csv'

# for now, it is just getting balance
@app.get("/get_account_details_by_account_id/")
async def get_account_details_by_account_id(account_id: str):
    # any kind of further df manipulation can be done here
    try:
        if path.isfile(filename) == True:
            df = pd.read_csv('./db/account.csv')
            if account_id not in df[df['account_id'] == account_id].values:
                raise ValueError("Account not found")

            balance = get_ledger_balance(account_id) + get_transaction_balance(account_id)
            return balance
        raise ValueError("Account not found")
    except ValueError as ve:
        return str(ve)


@app.post("/add_account")
async def get_settlement_rates(request : Request):
    try:
        # row to be inserted into db
        row = await request.json()
        input_df = pd.DataFrame(row,index=[0])
        account_id = row['account_id']
        if path.isfile(filename) == True:
            existing_df = pd.read_csv(filename)
            if account_id in existing_df['account_id'].values:
                raise ValueError("Account created")
        # append to db
        status = save_to_file(input_df,filename,['account_id','account_name'])
        return status

    except ValueError as ve:
        return str(ve)
