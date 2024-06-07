# ledger_type	sub_account_id	amount	currency	date

from fastapi import FastAPI,Request
import pandas as pd
# import csv 
import os.path as path


app = FastAPI()

filename = './db/ledger.csv'

# helper functions to insert data into desired file - this can be reused in the future
def create_new_file(input_df, filename):
    with open(filename, 'w') as f:
        input_df.to_csv(filename, header=True, columns= ['ledger_id','ledger_type','account_id','amount'],index=False)
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

def is_enough_to_withdraw(account_id,amount):
    # amount - amount want to withdraw from account(account_id)
    existing_df = pd.read_csv('../db/ledger.csv')
    amt_sum_of_sub_account = existing_df[existing_df['account_id'] == account_id]['amount'].sum()
    print(amt_sum_of_sub_account)
    if amount > amt_sum_of_sub_account:
        raise ValueError("Amount insffucient") 
        return False
    return True

def get_ledger_balance(account_id):
    # amount - amount want to withdraw from account(account_id)
    existing_df = pd.read_csv('../db/ledger.csv')
    amt_sum_of_sub_account = existing_df[existing_df['account_id'] == account_id]['amount'].sum()
    return amt_sum_of_sub_account

# update account - deposit
@app.post("/deposit/")
async def deposit(request: Request):
    data = await request.json()
    amt_int = int(data['amount'])
    if amt_int <= 0:
        raise ValueError("Amount should be positive")
    input_df = pd.DataFrame(data,index=[0])
    save_to_file(input_df,filename)

# update account - withdraw
@app.post("/withdraw/")
async def withdraw(request: Request):
    data = await request.json()
    account_id = data['account_id']
    amt_int = int(data['amount'])

    if amt_int <= 0:
        raise ValueError("Amount should be positive")
    existing_df = pd.read_csv(filename)
    amt_sum_of_sub_account = existing_df[existing_df['account_id'] == account_id]['amount'].sum()

    if amt_int > amt_sum_of_sub_account:
        raise ValueError("Amount insffucient") 
    data['amount'] = -amt_int
    input_df = pd.DataFrame(data,index=[0])
    save_to_file(input_df,filename)
    

# update account - trasnfer
# trasnfers consists of depositing into receiver and withdrawal of sender
@app.post("/transfer/")
async def withdraw(request: Request):
    data = await request.json()
    sender_acc_id = data['sender']
    amount = data['amount']
    if amount < 0:
        raise ValueError("Amount should be positive")
    
    if not is_enough_to_withdraw(sender_acc_id,amount):
        raise ValueError("Amount insufficient")
    
    data['amount'] = -amount
    
    # sender_account_id = data['sender']
    # receiver_id = data['sub_account_id']
    # amt_int = int(data['amount'])

    # if amt_int <= 0:
    #     raise ValueError("Amount should be positive")
    # existing_df = pd.read_csv(filename)
    # amt_sum_of_sender = existing_df[existing_df['sub_account_id'] == sender_account_id]['amount'].sum()
    # print(amt_sum_of_sender)
    # if amt_int > amt_sum_of_sender:
    #     raise ValueError("Amount insffucient") 

    # data['amount'] = -amt_int
    # print(data)
    # input_df = pd.DataFrame(data,index=[0])
    # save_to_file(input_df,filename)





# update account - withdrawal