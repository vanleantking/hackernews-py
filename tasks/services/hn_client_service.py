import requests as re
import json
from typing import List
from django.utils import timezone
from tasks.constants.constants import \
    ENDPOINT_ITEM, \
    ENDPOINT_BESTSTORIES, \
    ITEM_STATUS_PROCESS_TITLE
from core.models import HNItem


class HNClientService:
    __slots__ = ['base_url', 'api_version', 'api_format']

    def __init__(self, base_url: str, api_version: str, api_format: str):
        self.base_url = base_url
        self.api_version = api_version
        self.api_format = api_format

    def get_top_stories(self, method: str, params: dict, end_point: ENDPOINT_BESTSTORIES) -> List[int]:
        """
        Retrieve the top list of stories from api
        Args:
            end_point:
            method:
            params:

        Returns:

        """
        url_request = self.generate_url_request(end_point=end_point, item_id=0)
        result = []
        try:
            result = self.make_request(url_request=url_request, method=method, params=params)

        except Exception as exp:
            print('Oops, something happened when get top stories from request, ', exp)
            pass
        return result

    def get_item_detail(self, method: str, item_id: int) -> HNItem:
        """

        Args:
            method:
            item_id:

        Returns:

        """
        end_point = ENDPOINT_ITEM
        url_request = self.generate_url_request(end_point=end_point, item_id=item_id)
        item = {}
        try:
            item = self.make_request(url_request=url_request, method=method)
        except Exception as exp:
            print('Oops, something happened when get detail item from request, ', exp)
        if not item:
            return item
        if item:
            created_time = timezone.make_aware(
                timezone.datetime.fromtimestamp(item.get("time", 0)),
                timezone=timezone.get_current_timezone()
            )
            hn_item = HNItem(
                hn_item_id=item.get('id', 0),
                item_by=item.get("by", ""),
                descendants=item.get("descendants", 0),
                kids=item.get("kids", {}),
                item_score=item.get("score", 0),
                created_time=created_time,
                item_title=item.get("title", ""),
                item_type=item.get("type", ""),
                item_url=item.get("url", ""),
                item_content=item.get("text", ""),
                item_status=ITEM_STATUS_PROCESS_TITLE,
                updated_at=timezone.now(),
                created_at=timezone.now()
            )
            return hn_item

    @staticmethod
    def make_request(url_request: str, method: str, params=None) -> json:
        """
        Make a HTTP request into hacker news client
        Args:
            url_request:
            method:
            params:

        Returns:

        """
        method_request = getattr(re, method.lower())
        try:
            resp = method_request(url=url_request, data=params)
            resp.raise_for_status()
        except Exception as exp:
            raise Exception(f"Failed in make request on {url_request}, {exp}")
        return resp.json()

    def generate_url_request(self, end_point: str, item_id: int) -> str:
        """

        Args:
            end_point:
            item_id:

        Returns:

        """
        base_query = f"{self.base_url}/{self.api_version}/{end_point}"
        if end_point == ENDPOINT_ITEM:
            base_query = f"{base_query}/{item_id}"

        return f"{base_query}.{self.api_format}"
