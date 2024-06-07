import requests
import uuid

add_acc_url = 'http://0.0.0.0:8000/add_account'
get_acc_url = 'http://0.0.0.0:8000/get_account_details_by_account_id'


transfer_url = 'http://0.0.0.0:8001/transfer'

ledger_deposit = 'http://0.0.0.0:8002/deposit'
ledger_withdraw = 'http://0.0.0.0:8002/withdraw'




# add account
# account_name = 'Bryan'
# account_id = 'abc'
# myobj = {'account_id':account_id,'account_name':account_name}
# x = requests.post(add_acc_url, json = myobj)
# print(x.text)

# account_name = 'Colin'
# account_id = 'abcd'
# myobj = {'account_id':account_id,'account_name':account_name}
# x = requests.post(add_acc_url, json = myobj)
# print(x.text)

# # get acccount
# query_params = {'account_id':'abcd'}
# x = requests.get(get_acc_url, params = query_params)
# print(x.text)

# query_params = {'account_id':'abc'}
# x = requests.get(get_sub_acc_url, params = query_params)

# print(x.text)



# transfer - abc sends abcd
transaction_id = str(uuid.uuid4())
query_params = {'transaction_id':transaction_id,'sender':'abc','receiver':'abcd','amount':500.23,'type':'transfer'}
y = requests.post(transfer_url, json = query_params)

# transfer - abcd sends abc
# transaction_id = str(uuid.uuid4())
# query_params = {'transaction_id':transaction_id,'sender':'abcd','receiver':'abc','amount':500.23,'type':'transfer'}
# y = requests.post(transfer_url, json = query_params)




# ledger - deposit
# ledger_id = str(uuid.uuid4())
# ledger_type  = 'deposit'
# account_id = 'abc'
# amount = 1000
# query_params = {'ledger_id':'ledger_'+ledger_id,'ledger_type':ledger_type,'account_id':account_id,'amount':amount}
# y = requests.post(ledger_deposit, json = query_params)

# ledger - withdraw 
# ledger_id = str(uuid.uuid4())
# ledger_type  = 'withdraw'
# account_id = 'abc'
# amount = 1000
# query_params = {'ledger_id':'ledger_'+ledger_id,'ledger_type':ledger_type,'account_id':account_id,'amount':amount}
# y = requests.post(ledger_withdraw, json = query_params)






