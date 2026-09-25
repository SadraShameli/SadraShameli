import click

from readme.card.builder import CardBuilder
from readme.photo.cropper import PhotoCropper
from readme.util.repository import UtilRepository


@click.group(
    invoke_without_command=True,
    help="Draw the profile README: every card, and README.md itself.",
)
@click.pass_context
def cli(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.invoke(build)


@cli.command(help="Draw every card into Assets/Readme and write README.md.")
def build() -> None:
    CardBuilder(repository=UtilRepository.locate()).run()


@cli.command(help="Crop the photos the cards embed into Images/Cards.")
def photos() -> None:
    PhotoCropper(repository=UtilRepository.locate()).run()
