class ProjectExistsError(Exception):
    """Exception for already existing project folder"""

    def __init__(self, message):
        self.message = message


class ProjectFolderExistsError(Exception):
    """Exception for already existing project folder"""

    def __init__(self, message):
        self.message = message

class NoProjectsError(Exception):
    """Exception for already existing project folder"""

    pass
