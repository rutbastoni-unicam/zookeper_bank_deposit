#!/bin/sh

echo "Waiting for ZooKeeper ready..."

# Retry until it is ready
while ! echo ruok | nc zookeeper 2181 | grep imok > /dev/null; do
  echo "ZooKeeper still not ready, retry in 2 seconds..."
  sleep 2
done

echo "ZooKeeper ready! Init bank deposit node..."

zkCli.sh -server zookeeper:2181 <<EOF
create /bank_deposit 1000
ls /
EOF

tail -f /dev/null