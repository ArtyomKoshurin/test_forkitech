from decimal import Decimal

from tronpy import Tron
from tronpy.exceptions import AddressNotFound


client = Tron()


def get_wallet_info(address: str):
    try:
        account = client.get_account(address)

        if not account:
            raise AddressNotFound("Account not found")

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

    except AddressNotFound:
        wallet_info = {
            "address": address,
            "balance": Decimal("0.0"),
            "bandwidth": 0,
            "energy": 0
        }

    except Exception as e:
        print(f"Error: {e}")
        wallet_info = {
            "address": address,
            "balance": Decimal("0.0"),
            "bandwidth": 0,
            "energy": 0
        }

    return wallet_info
