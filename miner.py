def mine_block(miner_node):
    while True:
        candidate_txs = select_transactions(miner_node.mempool)
        prev_block = miner_node.blockchain.best_block()
        block = Block(index=prev_block.index+1,
                      prev_hash=prev_block.hash,
                      transactions=candidate_txs,
                      timestamp=current_time())
        block.merkle_root = merkle_root(block.transactions)
                nonce = 0
        while True:
            block.nonce = nonce
            block_hash = sha256(serialize_block_header(block))
            if meets_difficulty(block_hash):
                block.hash = block_hash
                break
            nonce += 1
        broadcast_to_peers(miner_node.peers, "block", block)
