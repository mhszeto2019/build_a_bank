import unittest
import requests
import os
import uuid

def remove_csv_files(folder_path):
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file ends with .csv extension
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            # Remove the file
            os.remove(file_path)
            print(f"Removed: {file_path}")

remove_csv_files('../db/')

class TestAPI(unittest.TestCase):

    ADD_ACC_URL = 'http://0.0.0.0:8000/add_account'
    GET_ACC_URL = 'http://0.0.0.0:8000/get_account_details_by_account_id'
    TRANSFER_URL = 'http://0.0.0.0:8001/transfer'

    LEDGER_DEPOSIT_URL = 'http://0.0.0.0:8002/deposit'
    LEDGER_WITHDRAWAL_URL = 'http://0.0.0.0:8002/withdraw'

    
    def test_add_account(self):
        account_name = 'Bryan'
        account_id = 'abc'
        myobj = {'account_id': account_id, 'account_name': account_name}
        
        response = requests.post(self.ADD_ACC_URL, json=myobj)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.strip('"'), "New file created")
    
    def test_add_duplicate_account(self):
        account_name = 'Bryan'
        account_id = 'abc'
        myobj = {'account_id': account_id, 'account_name': account_name}
        
        # Add the first account
        response = requests.post(self.ADD_ACC_URL, json=myobj)
        self.assertEqual(response.status_code, 200)

        # Attempt to add the duplicate account
        response = requests.post(self.ADD_ACC_URL, json=myobj)
        
        # Assert the response for adding a duplicate account
        self.assertEqual(response.status_code, 200)  # Assuming 200 is returned for duplicate
        self.assertEqual(response.text.strip('"'), "Account created")
    
    def test_add_another_account(self):

        account_name = 'Bryan'
        account_id = 'abc'
        myobj = {'account_id': account_id, 'account_name': account_name}

        account_name = 'Colin'
        account_id = 'abcd'
        myobj2 = {'account_id': account_id, 'account_name': account_name}
        
        # Add the first account
        response = requests.post(self.ADD_ACC_URL, json=myobj)
        self.assertEqual(response.status_code, 200)

        # Attempt to add the duplicate account
        response = requests.post(self.ADD_ACC_URL, json=myobj)
        
        # Assert the response for adding a duplicate account
        self.assertEqual(response.status_code, 200) 

        # Add Colin
        response = requests.post(self.ADD_ACC_URL, json=myobj2)
        self.assertEqual(response.text.strip('"'), "appended")


    def test_add_deposit(self):
        ledger_id = str(uuid.uuid4())
        ledger_type  = 'deposit'
        account_id = 'abc'
        amount = 2000
        myobj =  {'ledger_id':'ledger_'+ledger_id,'ledger_type':ledger_type,'account_id':account_id,'amount':amount}
        
        # Assuming the account already exists from the previous test
        response = requests.post(self.LEDGER_DEPOSIT_URL, json=myobj)
        
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.strip('"'),"Deposit Succesful")

    def test_withdraw(self):
        ledger_id = str(uuid.uuid4())
        ledger_type  = 'withdrawal'
        account_id = 'abc'
        amount = 1000
        myobj =  {'ledger_id':'ledger_'+ledger_id,'ledger_type':ledger_type,'account_id':account_id,'amount':amount}
        
        # Assuming the account already exists from the previous test
        response = requests.post(self.LEDGER_WITHDRAWAL_URL, json=myobj)
        
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.strip('"'),"Withdrawal Successful")
        

    def test_transfer_successful(self):
        transaction_id = str(uuid.uuid4())

        myobj = {'transaction_id':transaction_id,'sender':'abc','receiver':'abcd','amount':500,'type':'transfer'}
        
        # Assuming the account already exists from the previous test
        response = requests.post(self.TRANSFER_URL, json=myobj)
        
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.strip('"'),"Transfer from abc to abcd was Successful")
        
    def test_transfer_failure(self):
        transaction_id = str(uuid.uuid4())

        myobj = {'transaction_id':transaction_id,'sender':'abc','receiver':'abcd','amount':5000,'type':'transfer'}
        
        # Assuming the account already exists from the previous test
        response = requests.post(self.TRANSFER_URL, json=myobj)
        
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.strip('"'),"Sender does not have enough fund to transfer")
    
    def test_transfer_amount_negative(self):
        transaction_id = str(uuid.uuid4())  

        myobj = {'transaction_id':transaction_id,'sender':'abc','receiver':'abcd','amount':-5000,'type':'transfer'}
        
        # Assuming the account already exists from the previous test
        response = requests.post(self.TRANSFER_URL, json=myobj)
        
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.strip('"'),"Amount should be positive")


if __name__ == "__main__":
    unittest.main()
