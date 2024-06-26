# ledger_type	sub_account_id	amount	currency	date

from fastapi import FastAPI,Request
import pandas as pd
# import csv 
import os.path as path
from app.util import create_new_file,save_to_file,update_existing_file, get_transaction_balance,get_ledger_balance
# from app.util import get_transaction_balance
app = FastAPI()

filename = './db/ledger.csv'

def is_enough_to_withdraw(account_id,amount):
    # amount - amount want to withdraw from account(account_id)
    existing_df = pd.read_csv(filename)
    amt_sum_of_sub_account = existing_df[existing_df['account_id'] == account_id]['amount'].sum()
    print(amt_sum_of_sub_account)
    if amount > amt_sum_of_sub_account:
        raise ValueError("Amount insffucient") 
    return True

# def get_ledger_balance(account_id):
#     if not path.exists(filename):
#         return 0.0
#     # amount - amount want to withdraw from account(account_id)
#     existing_df = pd.read_csv(filename)
#     sum_of_deposit_and_withdrawal = existing_df[existing_df['account_id'] == account_id]['amount'].sum()
#     return float(sum_of_deposit_and_withdrawal)

# update account - deposit
@app.post("/deposit/")
async def deposit(request: Request):
    try:
        data = await request.json()
        amt_int = int(data['amount'])
        if amt_int <= 0:
            raise ValueError("Amount should be positive")
        input_df = pd.DataFrame(data,index=[0])
        save_to_file(input_df,filename,['ledger_id','ledger_type','account_id','amount'])
        return "Deposit Succesful"
    except ValueError as ve:
        return str(ve)

# update account - withdraw
@app.post("/withdraw/")
async def withdraw(request: Request):
    try:
        data = await request.json()
        account_id = data['account_id']
        amt_int = int(data['amount'])
        if amt_int <= 0:
            raise ValueError("Amount should be positive")
        sum_of_deposit_withdrawal_transactions = get_ledger_balance(account_id) + get_transaction_balance(account_id)
        if amt_int > sum_of_deposit_withdrawal_transactions:
            raise ValueError("Amount insffucient") 
        data['amount'] = -amt_int
        input_df = pd.DataFrame(data,index=[0])
        save_to_file(input_df,filename,['ledger_id','ledger_type','account_id','amount'])
        return "Withdrawal Successful"
    except ValueError as ve:
        return str(ve)
