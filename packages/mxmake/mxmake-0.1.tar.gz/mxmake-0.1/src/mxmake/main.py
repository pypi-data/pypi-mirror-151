from mxmake.templates import template
from mxmake.utils import list_value
from mxmake.utils import ns_name
import argparse
import logging
import mxdev
import sys
import typing


logger = logging.getLogger('mxmake')


def read_configuration(tio: typing.TextIO) -> mxdev.Configuration:
    hooks = mxdev.load_hooks()
    configuration = mxdev.Configuration(tio=tio, hooks=hooks)
    state = mxdev.State(configuration=configuration)
    mxdev.read(state)
    mxdev.read_hooks(state, hooks)
    return configuration


def clean_files(configuration: mxdev.Configuration) -> None:
    logger.info('mxmake: clean generated files')
    templates = list_value(configuration.settings.get(ns_name('templates')))
    if not templates:
        logger.info('mxmake: No templates defined')
    else:
        for name in templates:
            factory = template.lookup(name)
            instance = factory(configuration)
            if instance.remove():
                logger.info(f'mxmake: removed "{instance.target_name}"')


def main() -> None:
    mxdev.setup_logger(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--configuration',
        help='mxdev configuration file',
        nargs="?",
        type=argparse.FileType('r'),
        required=True
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Remove generated files'
    )
    args = parser.parse_args()
    if args.clean:
        configuration = read_configuration(args.configuration)
        clean_files(configuration)
        sys.exit(0)
    logger.info('mxmake: no action given')
    sys.exit(1)
