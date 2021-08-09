from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import CommandParser
from django.conf import settings

try:
  import autopep8
except ImportError as error:
  raise CommandError('autopep8 package not installed') from error


class Command(BaseCommand):
  help = 'Apply pep8 format each python file.'

  def add_arguments(self, parser: CommandParser):
    parser.add_argument('--file', '-f',
                        help='Use when you want to apply format this file')

  def handle(self, *args, **options):
    basedir = Path(settings.BASE_DIR)

    if not basedir.is_dir():
      raise CommandError(f'Invalid project directory: {basedir}')

    autopep8.DEFAULT_INDENT_SIZE = 2

    paths = ([options['file']] if options['file'] else basedir.glob('**/*.py'))

    for path in paths:
      autopep8.main(('autopep8', '-i', '-a', '-a', str(path)))
