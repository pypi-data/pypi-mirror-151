from trame.app import get_server

from . import engine, ui, assets

def main():
    server = get_server()
    server.cli.add_argument(
        "--input",
        help="directory to parflow template",
        dest="input",
        required=True,
    )
    server.cli.add_argument(
        "--output",
        help="directory to run parflow",
        dest="output",
        required=True,
    )
    server.cli.add_argument(
        '--auto-delete',
        help="Delete output directory at exit",
        dest="delete",
        action='store_true',
    )
    args = server.cli.parse_args()

    assets.initialize(server)
    engine.initialize(server, args.input, args.output, args.delete)
    ui.initialize(server)
    server.start()


if __name__ == "__main__":
    main()
