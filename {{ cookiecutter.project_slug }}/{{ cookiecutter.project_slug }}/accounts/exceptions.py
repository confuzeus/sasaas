class MultipleMemberships(Exception):
    """
    User is part of multiple membership groups.
    """


class NoMembership(Exception):
    """
    User isn't part of any memberships.
    """
