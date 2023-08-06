from importlib.metadata import version


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(version("cookiemonster"))
        sys.exit()
