from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User

from sitechecker.models import Site

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Add a new site to the database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('username', type=str)
        # Optional args
        # parser.add_argument('--name', type=str)

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['username'])
        except ObjectDoesNotExist as e:
            raise CommandError("User does not exist: %s. %s" % (options['username'], e))
        except MultipleObjectsReturned as e:
            raise CommandError("Multiple users match username: %s. %s" % (options['username'], e))

        existing_match = Site.objects.filter(user=user, url=options['url'])
        if existing_match.exists():
            raise CommandError("Site already exists for user %s: %s" % (user.username, options['url']))

        new_site = Site(user=user, url=options['url'], description=options['description'])



        try:
            new_site.save()
            self.stdout.write(self.style.SUCCESS("Site added: %s - %s" % (options['url'], options['description'])))
        except Exception as e:
            raise CommandError("Error adding site: %s." % e)







