# build_a_bank
Setup:
1) Ensure Python is downloaded
2) Ensure in home directory, there is an 'environments' folder which has a virtual environment called cdc_env
3) We will use cdc_env as our virtual environment to ensure other packages are not conflicted. In order to do so, we enter "source ~/environments/cdc_env/bin/activate
4) enter into the build_a_bank folder and install the necessary packages. In order to do so, we enter "pip install -requirements.txt


 Thought process:
- There are 5 
- I believe that this program will be used to integrate with other aspects of the company. As such, I designed it in a way such that they are reusable APIs
- Double entry feature




Testing process:
Account - there will be accounts for users
1) Create account
2) Get accounts details
Ledger - withdrawal and deposit will be done in the ledger
3) Test Deposit
4) Test withdrawal - try withdraw a sufficient amount and then withdraw an insufficient amount 
5) try get balance of account
Transfer - transfers will be considered as a transaction
6) Test Transfer
7) try get balance of account