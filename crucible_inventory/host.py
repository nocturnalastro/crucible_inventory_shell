from dataclasses import dataclass
from . import exceptions as ex


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
            raise ex.UnsupportedVendor(
                f"Vendor ({self.vendor}) is not in supported "
                f"vendors ({supported_vendors})"
            )

        if self.role not in (allowed_roles := self.get_allowed_roles()):
            raise ex.UnsupportedRole(
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
