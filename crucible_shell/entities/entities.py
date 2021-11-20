from dataclasses import dataclass, field


@dataclass
class Node:
    name: field(type=str, required=True)
    host: field(type=str, required=True)
    vendor: field(type=str, required=True)
    mac: field(type=str, required=True)
    role: str = "master"

    


    @property
    def SUPPORTED_VENDORS(self):
        return ("KVM", "dell")

    @property
    def ALLOWED_ROLES(self):
        return ("master", "worker")


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
