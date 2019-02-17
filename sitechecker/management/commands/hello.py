from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Just a test command that says hello.'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        # Optional args
        # parser.add_argument('--name', type=str)

    def handle(self, *args, **options):
        print("Hello.")
        self.stdout.write(self.style.SUCCESS('Hello, %s.' % options['name']))
        self.stdout.write(self.style.ERROR('Goodbye, %s.' % options['name']))
