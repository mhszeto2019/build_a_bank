import os.path as path
import pandas as pd

# helper functions to insert data into desired file - this can be reused in the future
def create_new_file(input_df, filename,columns):
    try:
        with open(filename, 'w') as f:
            input_df.to_csv(filename, header=True, columns= columns,index=False)
        return "New file created"
    except Exception as e:
        return f"Failed to create new file: {str(e)}"

def save_to_file(input_df, filename,columns):
    if path.isfile(filename) == True:
        ### append only if not exists, to avoid churning
        try:
            return update_existing_file(input_df, filename,columns)
        except Exception as e:
            return f"Failed to save to file: {str(e)}"
    else:
        return create_new_file(input_df, filename,columns)

def update_existing_file(input_df, filename,columns):
        
        try: 
            existing_df = pd.read_csv(filename)  
            if len(input_df) == 0:
                return False
            # open the file in append mode
            with open(filename, 'a') as f:
                input_df.to_csv(f, header=False,index=False)
            return "appended"

        except Exception as e:
            return f"Failed to update to file: {str(e)}"


def get_transaction_balance(account_id):
    filename = './db/transaction.csv'
    if not path.exists(filename):
       return 0.0

    existing_df = pd.read_csv(filename)
    sum_of_transfers = existing_df[existing_df['receiver'] == account_id]['amount'].sum() - existing_df[existing_df['sender'] == account_id]['amount'].sum()
    return float(sum_of_transfers)

def get_ledger_balance(account_id):
    filename = './db/ledger.csv'

    if not path.exists(filename):
        return 0.0
    # amount - amount want to withdraw from account(account_id)
    existing_df = pd.read_csv(filename)
    sum_of_deposit_and_withdrawal = existing_df[existing_df['account_id'] == account_id]['amount'].sum()
    return float(sum_of_deposit_and_withdrawal)