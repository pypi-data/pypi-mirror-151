import sys

from ceader.ports.cli import Cli


# just main entry point
def run_cli() -> int:
    args = sys.argv[1:]
    cli_app = Cli.new_cli_app(args)
    return cli_app.run()


def main() -> int:
    # start = datetime.now()
    # print(f"Creating headers started @ {start}")
    exit_code = run_cli()
    # end = datetime.now()
    # print(f"Creating headers finished @ {end}")
    # print(f"Creating headers took: {end-start}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
