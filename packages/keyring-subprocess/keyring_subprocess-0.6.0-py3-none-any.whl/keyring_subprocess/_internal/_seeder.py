"""Extensions for virtualenv Seeders to pre-install keyring-subprocess."""
import re
import abc
from virtualenv.seed.wheels import Version
from virtualenv.seed.embed.via_app_data.via_app_data import FromAppData

VERSION = Version.bundle


def pep503(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def normalize(name):
    return pep503(name).replace("-", "_")


def _get_embed_wheel(distribution, for_py_version):
    from virtualenv.seed.wheels.embed import BUNDLE_SUPPORT, BUNDLE_FOLDER, MAX
    from virtualenv.seed.wheels.util import Wheel

    wheels = BUNDLE_SUPPORT.get(for_py_version, {}) or BUNDLE_SUPPORT[MAX]
    wheel = wheels.get(distribution)

    if wheel is None:
        return None

    return Wheel.from_path(BUNDLE_FOLDER / wheel)


class ParserWrapper:
    def __init__(self, parser):
        self.parser = parser

    def __getattr__(self, item):
        return getattr(self.parser, item)

    def add_argument(self, *args, **kwargs):
        if "dest" in kwargs and (
            ("metavar" in kwargs and kwargs["metavar"] == "version")
            or any(
                arg for arg in args if isinstance(arg, str) and arg.startswith("--no-")
            )
        ):
            kwargs["dest"] = normalize(kwargs["dest"])

        self.parser.add_argument(*args, **kwargs)


class Normalize:
    def __enter__(self):
        KeyringSubprocessFromAppData.normalize = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        KeyringSubprocessFromAppData.normalize = False


class MetaClass(abc.ABCMeta):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "normalize"):
            cls.normalize = False


class KeyringSubprocessFromAppData(FromAppData, metaclass=MetaClass):
    """Mixed in keyring-subprocess into seed packages for app-data seeder."""

    def __init__(self, options):
        """Add the extra attributes for the extensions."""
        self.keyring_subprocess_version = options.keyring_subprocess
        self.no_keyring_subprocess = options.no_keyring_subprocess

        super(KeyringSubprocessFromAppData, self).__init__(options)

        import virtualenv.seed.wheels.bundle as bundle

        bundle.get_embed_wheel = _get_embed_wheel

    @classmethod
    def add_parser_arguments(cls, parser, interpreter, app_data):
        parser = ParserWrapper(parser)

        super(KeyringSubprocessFromAppData, cls).add_parser_arguments(
            parser, interpreter, app_data
        )

    @classmethod
    def distributions(cls):
        """Return the dictionary of distributions."""
        distributions = super(KeyringSubprocessFromAppData, cls).distributions()
        distributions["keyring-subprocess"] = VERSION

        if cls.normalize:
            distributions = {
                normalize(distribution): version
                for distribution, version in distributions.items()
            }

        return distributions

    def distribution_to_versions(self):
        with Normalize():
            return super(KeyringSubprocessFromAppData, self).distribution_to_versions()

    def __unicode__(self):
        with Normalize():
            return super(KeyringSubprocessFromAppData, self).__unicode__()
