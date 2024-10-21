import os
import django
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from django.core.management.base import BaseCommand
from tasks.tasks.pull_top_stories import HNTasks
from tasks.services.hn_client_service import HNClientService
from tasks.services.hn_top_stories import HNAPIStoryService
from decouple import config

# Set up Django settings module for the scheduler
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackerNews.settings")
django.setup()


class Command(BaseCommand):
    help = "Starts the APScheduler"

    def handle(self, *args, **kwargs):
        # implement tasks
        hn_api = HNClientService(
            base_url=config('HN_BASEURL'),
            api_version=config('HN_VERSION'),
            api_format=config('HN_FORMAT_API'))
        hn_service = HNAPIStoryService(hn_api=hn_api)
        tasks = HNTasks(hn_service=hn_service)
        scheduler = self.setup_executors()

        # Add job to scheduler
        scheduler.add_job(tasks.pull_top_stories, 'interval', seconds=3600)  # Adjust timing as needed
        scheduler.add_job(tasks.update_hn_items, 'interval', seconds=1800)  # Adjust timing as needed

        # Start the scheduler
        scheduler.start()

        print("Scheduler started. Press Ctrl+C to exit.")

        try:
            # Keep the script running
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            print("Scheduler shut down.")

    @staticmethod
    def setup_executors() -> BackgroundScheduler:
        """
        Set up the executors and job defaults for the APScheduler's BackgroundScheduler.
        Returns:
            BackgroundScheduler: Configured instance of BackgroundScheduler.

        """
        # Initialize the scheduler
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 10,
        }
        return BackgroundScheduler(executors=executors, job_defaults=job_defaults)
