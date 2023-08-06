__version__ = "0.4.2"

__all__ = [
    "AWResourcesClient",
    "AWJobsClient",
    "AWCacheStoreClient",
    "MethodsClient",
]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .resource_client import AWResourcesClient
    from .cache_store_client import AWCacheStoreClient
    from .job_client import AWJobsClient
    from .methods_client import MethodsClient
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
