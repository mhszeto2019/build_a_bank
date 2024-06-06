from fastapi import FastAPI,Request
import pandas as pd
import csv 

app = FastAPI()

filename = '../db/account.csv'



# helper functions to insert data into desired file - this can be reused in the future
def create_new_file(input_df, filename):
    with open(filename, 'w') as f:
        input_df.to_csv(filename, header=True, columns= ['ledger_id','ledger_type','sub_account_id','amount'],index=False)
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
async def get_account_details_by_account_id(account_id: int):
    # any kind of further df manipulation can be done here
    try:
        df = pd.read_csv(file_name) 
        print(df[df['account_id'] == account_id])
        # df of all the accounts with account id


        account_df = df[df['account_id'] == account_id]
        if account_id not in account_df.values:
            raise ValueError("Account ID not found")

        print(account_df)
        account_sub_account_arr = account_df['sub_account_id'].values
        account_balance = account_df['balance'].sum()
        print(account_sub_account_arr,account_balance)


    except FileNotFoundError:
        fieldnames = None

    

@app.get("/get_sub_account_details_by_sub_account_id/")
async def get_account_details_by_account_id(sub_account_id: str):
    # any kind of df manipulation can be done here
    df = pd.read_csv(file_name) 
    sub_account = df[df['sub_account_id'] == sub_account_id]
    print(sub_account)
    




@app.post("/add_account")
async def get_settlement_rates(request : Request):

    # row to be inserted into db
    row = await request.json()
    # append to db
    append_dict_to_csv(file_name,row)
    
