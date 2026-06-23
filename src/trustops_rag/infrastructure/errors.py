class InfrastructureError(Exception):
    pass


class ConfigurationError(InfrastructureError):
    pass


class RepositoryConflictError(InfrastructureError):
    pass
