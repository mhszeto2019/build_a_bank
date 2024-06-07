
from fastapi import FastAPI,Request
import pandas as pd
# import csv 
import os.path as path

from app.ledger import get_ledger_balance

app = FastAPI()

filename = './db/transaction.csv'

# helper functions to insert data into desired file - this can be reused in the future
def create_new_file(input_df, filename):
    with open(filename, 'w') as f:
        input_df.to_csv(filename, header=True, columns= ['transaction_id','sender','receiver','amount','type'],index=False)
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

def get_transaction_balance(account_id):
    if not path.exists(filename):
       return 0.0

    existing_df = pd.read_csv(filename)
    sum_of_transfers = existing_df[existing_df['receiver'] == account_id]['amount'].sum() - existing_df[existing_df['sender'] == account_id]['amount'].sum()
    return float(sum_of_transfers)

# update account - deposit
# @app.post("/deposit/")
# async def deposit(request: Request):
#     data = await request.json()
#     amt_int = int(data['amount'])
#     if amt_int <= 0:
#         raise ValueError("Amount should be positive")
#     input_df = pd.DataFrame(data,index=[0])
#     save_to_file(input_df,filename)

# # update account - withdraw
# @app.post("/withdraw/")
# async def withdraw(request: Request):
#     data = await request.json()
#     amt_int = int(data['amount'])
#     if amt_int <= 0:
#         raise ValueError("Amount should be positive")

#     data['amount'] = -amt_int
#     input_df = pd.DataFrame(data,index=[0])
#     save_to_file(input_df,filename)

# transfer
@app.post("/transfer/")
async def transfer(request: Request):
    data = await request.json()
    amount = data['amount']
    # amt_int = int(data['amount'])
    sender = data['sender']
    if amount <= 0:
        raise ValueError("Amount should be positive")
    # amount_left = ledger_balance + sum of all transfers of the sender (we do this because we want to check if the sender has sufficient amount) 
    # sum of all transfers is the total amount received and total amount sent out
    ledger_balance = get_ledger_balance(sender)
    if path.isfile(filename) == True:
        existing_df = pd.read_csv(filename)
        sum_of_transfers = existing_df[existing_df['receiver'] == sender]['amount'].sum() - existing_df[existing_df['sender'] == sender]['amount'].sum()

        amount_left = ledger_balance + sum_of_transfers
        print(amount_left)
        if amount_left < amount:
            raise ValueError("Sender does not have enough fund to transfer")
   
    input_df = pd.DataFrame(data,index=[0])
    save_to_file(input_df,filename)


