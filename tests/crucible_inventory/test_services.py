import sys
from crucible_inventory.services import AssistedInstaller


def test_assisted_installer():
    AssistedInstaller(host="localhost", hostname="mylocal.host.lab", port=8090)
