from . import exceptions as ex


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
                raise ex.Collision(
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
