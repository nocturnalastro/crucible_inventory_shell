from dataclasses import dataclass

@dataclass
class Node:
    name: str
    host: str
    vendor: str
    mac: str
    role: str = "master"
    SUPPORTED_VENDORS: list[str] = ('KVM', 'dell')
    ALLOWED_ROLES: list[str] = ('master', 'worker')


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
