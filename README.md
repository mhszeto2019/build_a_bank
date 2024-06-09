# build_a_bank
### Setup:
1. Before proceeding to test locally, I have deployed the application on an EC2 instance on AWS and the postman file can be found below.
OR
1. Ensure python3 is downloaded
2. Ensure that in home directory, there is an 'environments' folder which has a virtual environment called cdc_env created. E.g. (~/environments/cdc_env)
3. We will use cdc_env as our virtual environment to ensure other packages are not conflicted. In order to do so, we enter "source ~/environments/cdc_env/bin/activate in the terminal to activate the environment
4. Enter into the build_a_bank folder (~/build_a_bank) and install the necessary packages. In order to do so, we enter "pip install -r requirements.txt
5. After installing the necessary packages, we can and run the applications by using the "start_all.sh" script.
6. When all the tmux sessions are up, the application can be tested.


### Thought process:
- This program is designed for integration with other aspects of the company, so the APIs are designed to be reusable.
- API responses return strings for better readability and easier testing with tools like POSTMAN, rather than using standard HTTP status codes (200, 400, 500).
- The program includes three CSV files:
  - `account.csv` to store account information.
  - `ledger.csv` to record withdrawals and deposits.
  - `transaction.csv` to record transfers.
- The distinction between `ledger.csv` and `transaction.csv` is that a ledger entry involves only one account, while a transaction involves two accounts.

### Testing process:
#### Stage one - unittest:
We use the test_api.py script to conduct unittests for simple cases 
1. Enter into the app directory
2. Run "python -m unittest test_api.py" 


#### Stage two - scenario based test:
##### For the scenario-based test,  I use POSTMAN to test the APIs and verify the updates in the respective CSV files. The POSTMAN collection can be found in the `build_a_bank` directory (`~/build_a_bank/postman_file`). The application is deployed on an AWS server, and the POSTMAN test cases are directed to that server.

Account - we will be able to create accounts for users and can be seen in account.csv
1. Add account with the following json
json = {
  "account_id": "abc",
  "account_name": "Bryan"
}

We will be able to see Bryan being stored into the account.csv located at '~/build_a_bank/db/account.csv'

2. Check account balance of Bryan
query_params = {"account_id":"abc"}

From this, we can tell that Bryan has $0 in the bank. This can be found in the ledger.csv located at '~/build_a_bank/db/ledger.csv'

3. Add a second account 
json = {
  "account_id": "abcd",
  "account_name": "Colin"
}

We will be able to see Colin being stored into the account.csv located at '~/build_a_bank/db/account.csv'

4. Check account balance of Colin
query_params = {"account_id":"abcd"}

Similarly, we can tell that Colin has $0 in the bank.

Ledger - withdrawal and deposit will be done in the ledger and can be found in the ledger.csv

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

Transfer - transfers will be considered as a transaction and be found in the transaction.csv 
8. Transfer from Bryan to Colin
json ={
  "transaction_id": "transfer_123",
  "sender": "abc",
  "receiver": "abcd",
  "amount": 200,
  "type":"transfer"
}

9. Check account balance of Colin and Bryan
- query_params = {"account_id":"abcd"}
- query_params = {"account_id":"abc"}

From these two checks, we are able to see that Colin has $200 and Bryan has $800 ($1000 - $200) after the transfer takes place

