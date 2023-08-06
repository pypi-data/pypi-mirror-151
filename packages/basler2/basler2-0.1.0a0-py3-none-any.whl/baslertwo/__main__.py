"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """BaslerTwo."""
    print("Hello from basler2")
    print("Hello 2")


if __name__ == "__main__":
    main(prog_name="basler2")  # pragma: no cover
