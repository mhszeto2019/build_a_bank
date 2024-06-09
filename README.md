# build_a_bank
Setup:
1. Ensure Python is downloaded
2. Ensure that in home directory, there is an 'environments' folder which has a virtual environment called cdc_env created (~/environments/cdc_env.
3. We will use cdc_env as our virtual environment to ensure other packages are not conflicted. In order to do so, we enter "source ~/environments/cdc_env/bin/activate 
4. Enter into the build_a_bank folder and install the necessary packages. In order to do so, we enter "pip install -r requirements.txt

Thought process:
- I believe that this program will be used to integrate with other aspects of the company. As such, I designed it in a way such that they are reusable APIs
- For the responses, I return strings to show case how the APIs work in a readable manner instead of 200,400,500. In doing so, we can use POSTMAN to test the APIs and get a clearer picture of how it works

Testing process:
Stage one - unittest:
We use the test_api.py script to conduct unittests for simple cases 
1. Enter into the app directory
2. Run "python -m unittest test_api.py" 


Stage two - scenario based test:
Account - there will be accounts for users
1. Add account with the following json
json = {
  "account_id": "abc",
  "account_name": "Bryan"
}

2. Check account balance of bryan
query_params = {"account_id":"abc"}

From this, we can tell that Bryan has $0 in the bank

3. Add a second account 
json = {
  "account_id": "abcd",
  "account_name": "Colin"
}

4. Check account balance of Colin
query_params = {"account_id":"abcd"}

Similarly, we can tell that Colin has $0 in the bank


Ledger - withdrawal and deposit will be done in the ledger
5. Test withdrawal 
json = {
  "ledger_id": "ledger_123",
  "ledger_type": "withdraw",
  "account_id": "abc",
  "amount": 1
}

From this, we can tell that no money can be withdrawn from Bryan's account because he has $0

6. Test Deposit
{
  "ledger_id": "ledger_123",
  "ledger_type": "deposit",
  "account_id": "abc",
  "amount": 1000
}

We now proceed to add $1000 to Bryan's account

7. Check account balance of Bryan
query_params = {"account_id":"abc"}

We are able to see that Bryan account has $1000


Transfer - transfers will be considered as a transaction
8. Transfer from Bryan to Colin
json ={
  "transaction_id": "transfer_123",
  "sender": "abc",
  "receiver": "abcd",
  "amount": 200,
  "type":"transfer"
}

9. Check account balance of Colin and Bryan
query_params = {"account_id":"abcd"}

query_params = {"account_id":"abc"}

From these two checks, we are able to see that Colin has $200 and Bryan has $800 ($1000 - $200) after the transfer takes place

