import sys
from argparse import ArgumentParser

from .utils import f


def main():
    parser = ArgumentParser(description="Generate toggleable xmodmap bindings")
    print(f(2))


if __name__ == "__main__":
    main()
