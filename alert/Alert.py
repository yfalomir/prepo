class Alert:
    def __init__(self, message, level="info"):
        self.message = message
        self.level = level

    def __eq__(self, other):
        return self.message == other.message and self.level == other.level

    def __hash__(self):
        return hash((self.message, self.level))
