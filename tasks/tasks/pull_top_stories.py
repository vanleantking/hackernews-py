# Add this in your tasks.py or views.py
from tasks.constants.constants import ENDPOINT_TOPSTORIES
import asyncio
import logging


class HNTasks:
    __slots__ = ['hn_service', 'logger']

    def __init__(self, hn_service, logger):
        self.hn_service = hn_service
        self.logger = logger

    def pull_top_stories(self, end_point=ENDPOINT_TOPSTORIES):
        """

        Args:
            end_point:

        Returns:

        """
        try:
            self.logger.info(f"logging for endpoint {end_point}")
            return asyncio.run(self.hn_service.pull_top_stories(end_point))
            self.logger.info(f"process endpoint success {end_point}")
        except Exception as exp:
            self.logger.info(f"oops something unexpected happened {exp}")

    def update_hn_items(self):
        """

        Returns:

        """
        try:
            self.logger.info(f"logging for process update items hn")
            asyncio.run(self.hn_service.update_items())
            self.logger.info(f"process update items success")
        except Exception as exp:
            self.logger.info(f"oops something unexpected happened on update_hn_items: {exp}")


