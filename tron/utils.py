from decimal import Decimal

from tronpy import Tron


client = Tron()


def get_wallet_info(address: str):
    account = client.get_account(address)
    balance_sun = account.get("balance", 0)
    balance_trx = Decimal(balance_sun) / Decimal("1000000")

    resources = client.get_account_resource(address)
    bandwidth = resources.get("free_net_used", 0)
    energy = resources.get("energy_used", 0)

    wallet_info = {
        "address": address,
        "balance": balance_trx,
        "bandwidth": bandwidth,
        "energy": energy
    }

    return wallet_info
