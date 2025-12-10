"""Defines the Alert class to store insights about data."""


class Alert:
    """Stores insights about the data and it's criticity."""

    def __init__(self, message, level="info"):
        self.message = message
        self.level = level

    def __eq__(self, other):
        return self.message == other.message and self.level == other.level

    def __hash__(self):
        return hash((self.message, self.level))
