
from fastapi import FastAPI,Request
import pandas as pd
import os.path as path
from app.ledger import get_ledger_balance
from app.util import create_new_file,save_to_file,update_existing_file

app = FastAPI()

filename = './db/transaction.csv'

def get_transaction_balance(account_id):
    if not path.exists(filename):
       return 0.0

    existing_df = pd.read_csv(filename)
    sum_of_transfers = existing_df[existing_df['receiver'] == account_id]['amount'].sum() - existing_df[existing_df['sender'] == account_id]['amount'].sum()
    return float(sum_of_transfers)


# transfer
@app.post("/transfer/")
async def transfer(request: Request):
    try:
        data = await request.json()
        amount = data['amount']
        # amt_int = int(data['amount'])
        sender = data['sender']
        if amount <= 0:
            raise ValueError("Amount should be positive")
        # amount_left = ledger_balance + sum of all transfers of the sender (we do this because we want to check if the sender has sufficient amount) 
        # sum of all transfers is the total amount received and total amount sent out
        ledger_balance = get_ledger_balance(sender)
        sum_of_transfers = 0
        if path.isfile(filename) == True:
            existing_df = pd.read_csv(filename)
            sum_of_transfers = existing_df[existing_df['receiver'] == sender]['amount'].sum() - existing_df[existing_df['sender'] == sender]['amount'].sum()

        amount_left = ledger_balance + sum_of_transfers
        print(amount_left)
        if amount_left < amount:
            raise ValueError("Sender does not have enough fund to transfer")
    
        input_df = pd.DataFrame(data,index=[0])

        save_to_file(input_df,filename,['transaction_id','sender','receiver','amount','type'])
        
    except ValueError as ve:
        raise ve


