=======================
Site checker
=======================

Django application with management commands that are called
via cron job.

Example cron job (crontab -e)::

  # Cron entry - check every 1 minute
  */1 *  *   *   * /home/nanodano/django-cli/djangocli/sitechecker/cron/check_sites.sh

