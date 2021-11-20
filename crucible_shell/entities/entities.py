from dataclasses import dataclass, field
from nocturnal_shell.shell import ActionException


class UnsupportedVendor(ActionException):
    pass


class UnsupportedRole(ActionException):
    pass


@dataclass
class Node:
    name: str
    host: str
    vendor: str
    mac: str
    role: str = "master"

    def __post_init__(self):

        if self.vendor not in (supported_vendors := self.get_supported_vendors()):
            raise UnsupportedVendor(
                f"Vendor ({self.vendor}) is not in supported "
                f"vendors ({supported_vendors})"
            )

        if self.role not in (allowed_roles := self.get_allowed_roles()):
            raise UnsupportedRole(
                f"Role ({self.role}) is not in supported " f"roles ({allowed_roles})"
            )

    @staticmethod
    def get_supported_vendors():
        return ["KVM", "dell"]

    @staticmethod
    def get_allowed_roles():
        return ["master", "worker"]


class VMHost:
    pass


class Cluster:
    network: dict
    nodes: list
    services: list


class CrucibleInventory:
    def __init__(self, inventory_file=None):
        if inventory_file:
            raise NotImplementedError("Not implemented loading and inventory yet")

        self._nodes = []
        self._vm_hosts = []
        self._services = []

    def add_node(self, node):
        self._nodes.append(node)

    def add_service(self, service):
        self._services.append(service)

    def add_vmhost(self, vmhost):
        self._vm_hosts.append(vmhost)

    @property
    def is_valid(self):
        # TODO: Checks on inventory...
        return False
