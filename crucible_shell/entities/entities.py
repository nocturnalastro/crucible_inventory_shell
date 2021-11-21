from dataclasses import dataclass, field
from nocturnal_shell import exceptions as ex


class UnsupportedVendor(ex.ActionException):
    pass


class UnsupportedRole(ex.ActionException):
    pass


class Collision(ex.UserException):
    pass


@dataclass
class Host:
    name: str
    host: str

    def _collides(self, comparison):
        return [
            self.name == comparison.name,
            self.host == comparison.host,
        ]

    def collides(self, comparison):
        return any(self._collides(comparison))


@dataclass
class Node(Host):
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

    def _collides(self, comparison):
        return super()._collides(comparison) + [
            self.mac == comparison.mac,
        ]


@dataclass
class VMHost(Host):
    pass


@dataclass
class Service(Host):
    pass


class Cluster:
    network: dict
    nodes: list
    services: list


class CrucibleInventory:
    def __init__(self, inventory_file=None):
        if inventory_file:
            raise NotImplementedError("Not implemented loading and inventory yet")

        self.nodes = []
        self.vm_hosts = []
        self.services = []

    def check_for_collisions(self, insert, current):
        # Check for collisions between the
        for comparison in current:
            if insert.collides(comparison):
                raise Collision(
                    f"{insert.__class__.__name__} collies with already existing hosts"
                )

    def add_node(self, node):
        self.check_for_collisions(node, self.nodes)
        self.nodes.append(node)

    def add_service(self, service):
        self.services.append(service)

    def add_vmhost(self, vmhost):
        self.vm_hosts.append(vmhost)

    @property
    def is_valid(self):
        # TODO: Checks on inventory...
        return False
