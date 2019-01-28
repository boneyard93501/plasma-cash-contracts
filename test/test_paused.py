import pytest

from fixtures.const import ETHER_NAME, COIN_DENOMINATION, w3
from helpers import participate, erc20


def test_paused(setup):
    accounts, deployed_contracts = setup
    alice_addr = accounts[1].address

    plasma_instance = deployed_contracts.plasma_instance

    w3.personal.unlockAccount(w3.eth.accounts[0], '')
    pause_tx = plasma_instance.functions.pause(True).transact(
        {'from': w3.eth.accounts[0]}
    )
    w3.eth.waitForTransactionReceipt(pause_tx)

    erc20.transfer(alice_addr, w3.toWei(5000000, ETHER_NAME))
    erc20.approve(plasma_instance.address, alice_addr, w3.toWei(5000000, ETHER_NAME))

    # it should throw
    # Plasma is paused so no one can participate
    with pytest.raises(Exception):
        participate.participate(alice_addr, 2, COIN_DENOMINATION)

    w3.personal.unlockAccount(w3.eth.accounts[0], '')
    pause_tx = plasma_instance.functions.pause(False).transact(
        {'from': w3.eth.accounts[0]}
    )
    w3.eth.waitForTransactionReceipt(pause_tx)

    # Plasma now is not paused so every one can participate
    participate.participate(alice_addr, 2, COIN_DENOMINATION)
