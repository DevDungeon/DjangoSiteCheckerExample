# Perform an HTTP HEAD request to see if a site is up and returns
# a 200 OK message
import concurrent
from concurrent.futures import ThreadPoolExecutor

from django.contrib.sites import requests
from django.core.management.base import BaseCommand, CommandError
import requests
from django.utils import timezone

from djangocli import settings
from sitechecker.models import Site, Check


def check_site(site):
    print("Starting to check site: %s" % site.url)
    return requests.head(site.url, allow_redirects=True)


class Command(BaseCommand):
    help = 'Checks all sites'

    def store_response(self, site, response):
        site.last_response_code = str(response.status_code)
        site.last_time_checked = timezone.now()
        try:
            site.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR("Error updating site: %s - %s" % (e, site)))

        try:
            new_check_entry = Check(site=site, response_code=str(response.status_code))
            new_check_entry.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR("Error adding check: %s - %s" % (e, new_check_entry)))

    def handle(self, *args, **options):
        self.stdout.write("[*] Checking all sites....")

        with ThreadPoolExecutor(max_workers=settings.MAX_SITE_CHECKER_THREADS) as executor:
            future_to_responses = {executor.submit(check_site, site): site for site in Site.objects.all()}
            for future in concurrent.futures.as_completed(future_to_responses):
                site = future_to_responses[future]
                response = future.result()
                self.stdout.write("Response for %s: %s" % (site.url, response.status_code))
                self.store_response(site, response)

