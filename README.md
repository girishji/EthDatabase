# Etherium Database: Basic Implementation

Curious about doing analytics or detectve work in Etherium? Having access to a full fledged database of the blockchain is a must. Although a few companies provide this type of access, I will demonstrate the basic steps to build your own private database of the blockchain.

Read the notebook EthDb.ipynb.

## Topics Covered:

- Database Design
  - Schema
- Description of Attributes
- Block Attributes
  - Transaction Attributes
  - Classes
- Exploratory Data Analysis (EDA)
  - How secure is Etherium blockchain from 51% attack?
  - How rewarding is it to mine a block?
  - Transactions per block
  - Eth value transferred per transaction
  - Wallet balance calculation

Optional: There is also a basic Bottle web application to query the database. Run it as 'python query.py'
and navigate to http://127.0.0.1:8080/query. The database file is not included since it is huge. You
can download the blocks from Alchemy by providing the url inside the ethdb.py file (which is just
the python code extracted from the notebook).

