import logging

from importlib import metadata


# Primary package version
__version__ = metadata.version(__name__)

# Sentinel to make sure we only initialize once.
__initialized = False

logger = logging.getLogger(__name__)


def setup():
    """
    Used to configure the settings for Division 2 DB so the app may run.
    This should be called before any settings are loaded as it handles all of
    the file loading, conditional settings, and settings overlays required to
    load Division 2 DB settings from anywhere using environment or config path.
    This pattern is inspired by `django.setup()`.
    """
    global __initialized

    if __initialized:
        logger.info("Division 2 DB NOT initialized (because it already was)!")
        return

    from division.core import cli
    from division.core.runner import configure_app

    configure_app(
        project="division",
        default_config_path=cli.DEFAULT_CONFIG_PATH,
        default_settings=cli.DEFAULT_SETTINGS,
        settings_initializer=cli.generate_settings,
        settings_envvar=cli.SETTINGS_ENVVAR,
        initializer=cli._configure_settings,
    )
    logger.info("division build server initialized!")

    __initialized = True
