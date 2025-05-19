import re



def es_txid_valida(txid):
    return bool(re.fullmatch(r'[0-9a-f]{64}', txid))


print(es_txid_valida("c9435711f75903656f0b04d84b4058f2755403aa279774de212f75797c0t474f"))