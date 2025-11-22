def create_and_broadcast_tx(inputs, outputs, private_key, node):
    tx = Transaction(inputs=inputs, outputs=outputs)
    tx.id = sha256(serialize(tx))

    for inp in tx.inputs:
        inp.signature = sign(private_key, tx.id)

    node.receive_transaction(tx)

def receive_transaction(node, tx):
    if not well_formed(tx):
        return REJECT

    if not inputs_unspent(tx, node.utxo_set):
        return REJECT  

    for inp in tx.inputs:
        owner_pubkey = node.utxo_set[(inp.prev_tx_id, inp.prev_output_index)].owner_pubkey
        if not verify_signature(owner_pubkey, tx.id, inp.signature):
            return REJECT

    node.mempool.add(tx)
    broadcast_to_peers(node.peers, "tx", tx)
    return ACCEPT
