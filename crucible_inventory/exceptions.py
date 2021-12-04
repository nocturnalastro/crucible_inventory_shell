from nocturnal_shell import exceptions as ex


class UnsupportedVendor(ex.ActionException):
    pass


class UnsupportedRole(ex.ActionException):
    pass


class Collision(ex.UserException):
    pass
