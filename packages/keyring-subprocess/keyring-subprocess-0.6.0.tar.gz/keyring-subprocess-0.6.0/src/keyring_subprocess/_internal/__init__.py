try:
    import keyring
except ImportError:
    import sys
    from ._loader import KeyringSubprocessFinder

    sys.meta_path.append(KeyringSubprocessFinder())

try:
    import virtualenv
    from ._seeder import KeyringSubprocessFromAppData
except ImportError:
    pass


def sitecustomize() -> None:
    pass
