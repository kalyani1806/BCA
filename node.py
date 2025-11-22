def receive_block(node, block):
   
    if not validate_block_header(block):
        return REJECT

    utxo_copy = node.utxo_set.copy()
    for tx in block.transactions:
        if not inputs_unspent(tx, utxo_copy):
            return REJECT  
        for inp in tx.inputs:
            owner_pk = utxo_copy[(inp.prev_tx_id, inp.prev_output_index)].owner_pubkey
            if not verify_signature(owner_pk, tx.id, inp.signature):
                return REJECT
        apply_tx_to_utxo(tx, utxo_copy)

    attach_block_to_chain(node, block, utxo_copy)
    remove_block_txs_from_mempool(node.mempool, block.transactions)
    return ACCEPT
