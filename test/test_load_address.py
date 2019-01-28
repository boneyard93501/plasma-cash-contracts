from fixtures.const import DEFAULT_PASSWORD, w3
from helpers import estimate_gas


# only owner can successfully load plasma address
def test_successful_load_plasma_address(setup_participate):
    accounts, deployed_contracts, coins = setup_participate
    gas = estimate_gas.loadAddress(deployed_contracts.plasma_instance.address)

    w3.personal.unlockAccount(w3.eth.accounts[0], '')
    load_address_on_ERC721 = deployed_contracts.erc721_instance.functions.loadPlasmaAddress(
        deployed_contracts.plasma_instance.address).transact(
        {'from': w3.eth.accounts[0], 'gas': gas}
    )
    tx_receipt = w3.eth.waitForTransactionReceipt(load_address_on_ERC721)

    assert tx_receipt.status == 1


# alice is not the owner so she fails to load plasma address
def test_unsuccessful_load_plasma_address(setup_participate):
    accounts, deployed_contracts, coins = setup_participate
    alice_addr = accounts[1].address

    gas = estimate_gas.loadAddress(deployed_contracts.plasma_instance.address)

    w3.personal.unlockAccount(alice_addr, DEFAULT_PASSWORD)
    load_address_on_ERC721 = deployed_contracts.erc721_instance.functions.loadPlasmaAddress(
        deployed_contracts.plasma_instance.address).transact(
        {'from': alice_addr, 'gas': gas}
    )
    tx_receipt = w3.eth.waitForTransactionReceipt(load_address_on_ERC721)

    assert tx_receipt.status == 0


# only validator can successfully load addresses on plasma
def test_successful_load_addresses_on_plasma(setup_participate):
    accounts, deployed_contracts, coins = setup_participate

    gas = estimate_gas.load_addresses_on_plasma(deployed_contracts)

    w3.personal.unlockAccount(w3.eth.accounts[0], '')
    tx = deployed_contracts.plasma_instance.functions.setAddresses(
        deployed_contracts.erc20_instance.address,
        deployed_contracts.erc721_instance.address,
        deployed_contracts.checks_instance.address

    ).transact(
        {'from': w3.eth.accounts[0], 'gas': gas}
    )
    tx_receipt = w3.eth.waitForTransactionReceipt(tx)

    assert tx_receipt.status == 1


# alice is not the validator so she fails to load addresses on plasma
def test_unsuccessful_load_addresses_on_plasma(setup_participate):
    accounts, deployed_contracts, coins = setup_participate
    alice_addr = accounts[1].address

    gas = estimate_gas.load_addresses_on_plasma(deployed_contracts)

    w3.personal.unlockAccount(alice_addr, DEFAULT_PASSWORD)
    tx = deployed_contracts.plasma_instance.functions.setAddresses(
        deployed_contracts.erc20_instance.address,
        deployed_contracts.erc721_instance.address,
        deployed_contracts.checks_instance.address
    ).transact(
        {'from': alice_addr, 'gas': gas}
    )
    tx_receipt = w3.eth.waitForTransactionReceipt(tx)

    assert tx_receipt.status == 0
