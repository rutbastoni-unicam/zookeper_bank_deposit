import os
import time
import random
from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
from kazoo.exceptions import BadVersionError

client_name = os.getenv('CLIENT_NAME', 'client')

print(f"{client_name} trying to connect to ZooKeeper...")
zk = KazooClient(hosts='zookeeper:2181')



# Wait until ZooKeeper is ready
while True:
    try:
        zk.start(timeout=5)  # 5 seconds timeout to connect
        print(f"{client_name} connected to ZooKeeper")
        break
    except KazooTimeoutError:
        print(f"{client_name} connection refused, retrying in 2 seconds...")
        time.sleep(2)

print(f"{client_name} started and checking for node init...")

# Wait for /bank_deposit creation
while not zk.exists('/bank_deposit'):
    print(f"{client_name} waiting for /bank_deposit node...")
    time.sleep(2)

data, stat = zk.get('/bank_deposit')
data_str = data.decode('utf-8')
value = float(data_str)
print(f"'{client_name}' starts managing a bank deposit of {value:,.2f}$")

while True:
    # Sleep random between 1 and 10 seconds
    delay = random.randint(1, 15)
    print(f"{client_name} is going to be busy for {delay} seconds")

    time.sleep(delay)

    # random choice of operation
    amount = 0.0
    newdeposit = value
    action = random.choice(["withdraw", "deposit"])

    if action == "withdraw":
        # withdraw between 0 and current deposit
        amount = random.uniform(0.01, value)
        newdeposit = value - amount
        print(f"{client_name} is going to withdraw {amount:.2f}$ from deposit of {value:.2f}$, new amount should be {newdeposit:.2f}$")

    elif action == "deposit":
        # deposit between 0 and 1000
        amount = random.uniform(0.01, 1000)
        newdeposit = value + amount
        print(f"{client_name} is going to deposit {amount:.2f}$ in addition to {value:.2f}$, new amount should be {newdeposit:.2f}$ for version {stat.version}")

    # try to update the node - until it gets right version
    try:
        zk.set('/bank_deposit', str(newdeposit).encode('utf-8'), version=stat.version)

        # Read again node to update version
        _, new_stat = zk.get('/bank_deposit')
        print(f"{client_name} updated deposit amount. New version: {new_stat.version}\n")
        stat = new_stat
        value = newdeposit
    except  BadVersionError:
        # does not immediatly retry because it could lead to inconsistencies like withdrawing more money than available
        print(f"{client_name}: version conflict! Someone else changed amount. Get updated information and retry on next loop...\n")

        # read new value to stay updated
        new_data, new_stat = zk.get('/bank_deposit')
        new_data_str = new_data.decode('utf-8')
        value = float(new_data_str)
        stat = new_stat

    # Read the node
#     data, stat = zk.get('/bank_deposit')
#     print(f"'{client_name}' reads value: {data.decode('utf-8')} - version: {stat.version}")
