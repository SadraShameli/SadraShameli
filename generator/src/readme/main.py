import click

from readme import constants
from readme.command.cli import cli
from readme.exceptions import ReadmeError
from readme.logger.manager import configure_logger, get_logger

logger = get_logger()


def main() -> None:
    configure_logger()

    try:
        cli.main(standalone_mode=False)

    except click.exceptions.Abort:
        logger.info("Aborted.")

    except click.exceptions.ClickException as error:
        error.show()
        raise SystemExit(error.exit_code) from None

    except ReadmeError as error:
        click.ClickException(str(error)).show()
        raise SystemExit(constants.EXIT_CODE_FAILURE) from None
