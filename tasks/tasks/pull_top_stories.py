# Add this in your tasks.py or views.py
from tasks.constants.constants import ENDPOINT_TOPSTORIES
import asyncio


class HNTasks:
    __slots__ = ['hn_service']

    def __init__(self, hn_service):
        self.hn_service = hn_service

    def pull_top_stories(self, end_point=ENDPOINT_TOPSTORIES):
        """

        Args:
            end_point:

        Returns:

        """
        return asyncio.run(self.hn_service.pull_top_stories(end_point))

    def update_hn_items(self):
        """

        Returns:

        """
        asyncio.run(self.hn_service.update_items())


