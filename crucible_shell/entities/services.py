from .registry import Registry
from dataclasses import dataclass

__all__ = ("service_registry",)

service_registry = Registry()


@dataclass
class Service:
    host: str


@service_registry.add_class
@dataclass
class AssistedInstaller(Service):
    hostname: str
    port: int = 8090


@service_registry.add_class
@dataclass
class HTTPStore(Service):
    pass


@service_registry.add_class
@dataclass
class Registry(Service):
    registry_fqdn: str
    registry_port: str
    cert_country: str
    cert_locality: str
    cert_organization: str
    cert_organizational_unit: str
    cert_shell: str
    registry_container_image: str
    REGISTRY_HTTP_SECRET: str
    disconnected_registry_user: str
    disconnected_registry_password: str


@service_registry.add_class
@dataclass
class DNSMasq(Service):
    pass


@service_registry.add_class
@dataclass
class Chrony(Service):
    pass
