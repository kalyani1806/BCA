def inputs_unspent(tx, utxo_set):
    for inp in tx.inputs:
        key = (inp.prev_tx_id, inp.prev_output_index)
        if key not in utxo_set:
            return False
    return True

def apply_tx_to_utxo(tx, utxo_set):
    for inp in tx.inputs:
        del utxo_set[(inp.prev_tx_id, inp.prev_output_index)]
    for idx, out in enumerate(tx.outputs):
        utxo_set[(tx.id, idx)] = out