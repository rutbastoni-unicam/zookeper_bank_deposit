# ZooKeeper Bank Deposit Simulation

This repository contains Docker configuration files to set up a distributed environment simulating multiple clients accessing and modifying a shared bank deposit value via ZooKeeper. The setup includes:

- A single ZooKeeper server instance
- An initial ZooKeeper node `/bank_deposit` with value `1000`
- Three Python clients (`Alice`, `Bob`, `Chuck`) that simulate customers performing deposit and withdrawal operations on the same deposit, in a concurrent and synchronized manner

The clients demonstrate mutual exclusion and data consistency using ZooKeeper's versioning system. They run in an infinite loop, randomly choosing to deposit or withdraw money, and handle conflicts via optimistic concurrency control.

---

## Architecture Overview

- **ZooKeeper Server**: Manages the shared state and provides versioned znodes for synchronization.
- **Initialization**: Uses `zkCli.sh` to create the `/bank_deposit` node with an initial value.
- **Clients**: Python scripts that:
  - Randomly deposit or withdraw funds
  - Use ZooKeeper's versioning to ensure safe concurrent updates
  - Implement retry logic upon version conflicts

---

## Prerequisites

- Docker Engine v28.3.2 or higher
- Docker Compose v2.38.2 or higher

---

## Setup Instructions

1. **Clone this repository:**

```bash
git clone https://github.com/rutbastoni-unicam/zookeper_bank_deposit.git
cd ookeper_bank_deposit
```

2. **Start the environment:**
```bash
docker compose up -d
```
This command will:

- Launch the ZooKeeper server
- Run the zkCli.sh to initialize the /bank_deposit node with the value 1000
- Start the three Python client containers (alice, bob, chuck)

3. **Verify the setup:**
You can check the logs:
```bash
docker compose logs -f
```
The clients will run indefinitely, simulating concurrent deposit/withdrawal operations.

## Notes

Feel free to modify the client scripts or extend the setup. This example demonstrates basic distributed synchronization and conflict resolution using ZooKeeper.

## License

This project is for educational purposes. Use and modify as needed.

