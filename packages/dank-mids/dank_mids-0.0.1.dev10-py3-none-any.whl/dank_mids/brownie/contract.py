
from typing import Optional

from brownie import Contract, network, web3
from brownie.network.contract import ContractCall, ContractTx
from web3 import Web3

from dank_mids.brownie_patch.call import _patch_call
from dank_mids.brownie_patch.tx import _patch_tx

def patch_contract(contract: Contract, w3: Optional[Web3]) -> Contract:
    assert w3 is not None or network.is_connected()
    if w3 is None:
        w3 = web3

    for key, value in contract.__dict__.items():
        if isinstance(value, ContractCall):
            _patch_call(value, w3)
        elif isinstance(value, ContractTx):
            _patch_tx(value, w3)
    return contract
