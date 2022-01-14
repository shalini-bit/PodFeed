# Standard Library
import logging

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Third Party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from podcasts.models import Episode


logger = logging.getLogger(__name__)


def save_new_episodes(feed):
    """Saves new episodes to the database.

    Checks the episode GUID agaist the episodes currently stored in the
    database. If not found, then a new `Episode` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]

    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid).exists():
            episode = Episode(
                title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                link=item.link,
                image=podcast_image,
                podcast_name=podcast_title,
                guid=item.guid,
            )
            episode.save()


def fetch_zero_episodes():
    """Fetches new episodes from RSS for the Real Python Podcast."""
    _feed = feedparser.parse("https://media.rss.com/braindumpdiaries/feed.xml")
    save_new_episodes(_feed)


def fetch_first_episodes():
    """Fetches new episodes from RSS for the Talk Python to Me Podcast."""
    _feed = feedparser.parse("https://media.rss.com/itscomplicated/feed.xml")
    save_new_episodes(_feed)

def fetch_second_episodes():
    """Fetches new episodes from RSS for the Talk Python to Me Podcast."""
    _feed = feedparser.parse("https://media.rss.com/greenskysocialwork/feed.xml")
    save_new_episodes(_feed)

def fetch_third_episodes():
    """Fetches new episodes from RSS for the Talk Python to Me Podcast."""
    _feed = feedparser.parse("https://media.rss.com/thefreshslatepodcast/feed.xml")
    save_new_episodes(_feed)

def fetch_fourth_episodes():
    """Fetches new episodes from RSS for the Talk Python to Me Podcast."""
    _feed = feedparser.parse("https://media.rss.com/mindthehealthgap/feed.xml")
    save_new_episodes(_feed)




def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)



class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")



        scheduler.add_job(
            fetch_zero_episodes,
            trigger="interval",
            minutes=2,
            id="Brain dump diaries",  # Each job MUST have a unique ID
            max_instances=1,
            # Replaces existing and stops duplicates on restart of the app.
            replace_existing=True,
        )
        logger.info("Added job: Brain dump diaries")

        scheduler.add_job(
            fetch_first_episodes,
            trigger="interval",
            minutes=2,
            id="Its complicated",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Its complicated.")

        scheduler.add_job(
            fetch_second_episodes,
            trigger="interval",
            minutes=2,
            id="Green sky social network",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Green sky social network.")

        scheduler.add_job(
            fetch_third_episodes,
            trigger="interval",
            minutes=2,
            id="The fresh slate podcast",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Fresh slate podcast.")

        scheduler.add_job(
            fetch_fourth_episodes,
            trigger="interval",
            minutes=2,
            id="mind the health gap",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Mind the health gap.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
