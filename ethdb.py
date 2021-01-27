# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Etherium Database
# 
# %% [markdown]
# xxx describe each attribute
# %% [markdown]
# ### Database Design
# 
# #### Schema 
# 
# Database schema consists of two tables, named Block and Transaction. *blockHash* is the primary key of Block. *txHash* is the primary key of Transaction. Transaction table also has *blockHash*, which serves as foreign key to index into Block table. In addition, *blockHash* of Block table indexes rows of Transaction table for quick lookup. 
# 
# The relation between Block and Transaction is 1:Many, specifically, 1:greater_than_1. Each block contains a list of transaction hashes. However these hashes are not stored in Block table since it causes redundancy. Instead, indexing is used to achieve the effect of quick lookup of transaction hashes given a *blockHash*. Each transaction is retrieved separately and attributes specific to transaction are stored in Transaction table.
# 
# **Table Name:** Block    
# **Primary Key:** blockNumber   
# **Foreign Key:** none 
# 
# Block(**blockNumber**, blockHash, difficulty, extraData, gasLimit, gasUsed, logsBloom, miner, mixHash, nonce, parentHash, receiptsRoot, sha3Uncles, size, stateRoot, timestamp, totalDifficulty, transactionsRoot, uncles)
# 
# **Table Name:** Transaction    
# **Primary Key:** txHash    
# **Foreign Key:** blockNumber    
# 
# Transaction(**txHash**, *blockNumber*, blockHash, txFrom, gas, gasPrice, input, nonce, r, s, txTo, transactionIndex, v, value)
# 
# #### Entity Relationship Diagram
# 
# ERD illustrates the schema with the help of one-to-many relation.
# 
# 
# %% [markdown]
# ```
# +--------------------+                        +--------------------+              
# | Block              |                        | Transaction        |
# |--------------------|                        |--------------------|
# | *blockNumber*      |                        | *txHash*           |
# | blockHash          |            x           | blockHash          |
# | difficulty         |          /   \         | txFrom             |
# | extraData          |        /       \       | gas                |
# | gasLimit           |  1   /           \  n /| gasPrice           |
# | gasUsed            |-||--|  contains   |----| input              |
# | logsBloom          |      \           /    \| nonce              |
# | miner              |        \       /       | blockNumber
# | mixHash            |          \   /         | r                  |
# | nonce              |            v           | s                  |  
# | parentHash         |                        | txTo               |
# | receiptsRoot       |                        | transactionIndex   |
# | sha3Uncles         |                        | v                  |
# | size               |                        | value              |
# | stateRoot          |                        +--------------------+
# | timestamp          |                       
# | totalDifficulty    |                       
# | transactionsRoot   |                       
# | uncles             |                       
# +--------------------+                       
# ```                                  
# %% [markdown]
# ### Define Classes
# 
# XXX: More info. Transaction and block information are returned in a dictionary.
# 

# %%
from web3 import Web3
import sqlite3 as sq3


# %%
class Database:
    """Implemented using sqlite3"""

    Block_Count = 1000   # number of blocks to put into the database 
    Db_File = 'ethblockchain.db'
    conn = None
    #conn = sq3.connect(':memory:') # connection object to in-memory db

    def __init__(self):
        """Create and populate the database if one does not exist."""
        create_db = False
        try:
            self.conn = sq3.connect('file:' + self.Db_File + '?mode=ro',
                 uri=True) # read-only
            # check if database is empty (no tables)
            c = self.conn.cursor()
            t = c.execute('SELECT * FROM sqlite_master WHERE type=?', 
                        ('table',))
            if t.fetchone() is None: 
                create_db = True
        except sq3.OperationalError:
            create_db = True
        if create_db:
            # create the database
            self.conn = sq3.connect(self.Db_File)
            self._create_db() # create tables and populate data
            self.conn.commit()  
            self.conn.close()
            self.conn = sq3.connect('file:' + self.Db_File + '?mode=ro',
                 uri=True) # read-only

    def cursor(self):
        """Return a cursor to perform SQL queries"""
        return(self.conn.cursor())

    def _create_db(self):
        c = self.conn.cursor()
        # check if tables exist; if not, create tables and index
        t = c.execute('SELECT * FROM sqlite_master WHERE type=?', 
                        ('table',))
        if t.fetchone() is None: 
            self._create_tables()
            self._create_index()
            self._populate_db()
        

    def _create_tables(self):
        block = """
            CREATE TABLE IF NOT EXISTS Block (
                blockNumber INTEGER PRIMARY KEY,               
                extraData TEXT,
                gasLimit INTEGER,
                gasUsed INTEGER,
                blockHash TEXT,
                logsBloom TEXT,
                miner TEXT,
                mixHash TEXT,
                nonce TEXT,
                parentHash TEXT,
                receiptsRoot TEXT,
                sha3Uncles TEXT,
                size INTEGER,
                stateRoot TEXT,
                timestamp INTEGER,
                totalDifficulty TEXT,
                transactionsRoot TEXT, 
                uncles INTEGER); """
        
        tx = """
            CREATE TABLE IF NOT EXISTS Tx (
                txHash TEXT PRIMARY KEY,
                blockHash TEXT,
                blockNumber INTEGER,
                txFrom TEXT,
                gas INTEGER,
                gasPrice INTEGER,
                txInput TEXT,
                nonce INTEGER,
                r TEXT,
                s TEXT,
                txTo TEXT,
                transactionIndex INTEGER,
                v INTEGER,
                value TEXT);"""

        c = self.conn.cursor()
        c.execute(block)
        c.execute(tx)

    def _create_index(self):
        # Make it easy to search for all transactions inside a block
        c = self.conn.cursor()
        c.execute("CREATE INDEX Idx1 ON Tx(blockNumber);")

    def _blockTuple(self, bl):
        """Return a tuple of dictionary values"""
        tup = (
                bl.number, 
                bl.extraData.hex(), 
                bl.gasLimit, 
                bl.gasUsed, 
                bl.hash.hex(), 
                bl.logsBloom.hex(), 
                bl.miner, 
                bl.mixHash.hex(), 
                bl.nonce.hex(), 
                bl.parentHash.hex(), 
                bl.receiptsRoot.hex(), 
                bl.sha3Uncles.hex(), 
                bl.size, 
                bl.stateRoot.hex(), 
                bl.timestamp, 
                str(bl.totalDifficulty), 
                bl.transactionsRoot.hex(), 
                len(bl.uncles)
                )
        return(tup)

    def _txTuple(self, t):
        tup = (
                t.hash.hex(),
                t.blockHash.hex(),
                t.blockNumber,
                t.get('from'),
                t.gas,
                t.gasPrice,
                t.input,
                t.nonce,
                t.r.hex(),
                t.s.hex(),
                t.get('to'),
                t.transactionIndex,
                t.v,
                str(t.value),
                )
        return(tup)

    def _populate_db(self):
        c = self.conn.cursor()
        for bl in EthernetNode.blocks(self.Block_Count):
            c.execute(
                'INSERT INTO Block VALUES '
                + '(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                self._blockTuple(bl))
            for tx in bl.transactions:
                try:
                    c.execute(
                        'INSERT INTO Tx VALUES '
                        + '(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                        self._txTuple(tx)) 
                except OverflowError:
                    print(tx)
                    raise


# %%
from alchemy import getUrl 

class EthernetNode:
    """Since hosting a ethernet node locally is resource intensive, I will
        use a public node (like Alchemy) to get blockchain information""" 

    @classmethod
    def blocks(cls, blockCount):
        """A generator to return blockCount number of 
            consecutive blocks in the blockchain, starting with 
            the latest block."""
        blockNumber = -1
        web3 = Web3(Web3.HTTPProvider(getUrl()))
        for i in range(blockCount): 
            block = None 
            if blockNumber == -1:
                block = cls.web3.eth.getBlock('latest', True)
                blockNumber = block.number
            else:
                blockNumber -= 1
                if (blockNumber > 0):
                    block = cls.web3.eth.getBlock(blockNumber, True)
            yield block    


