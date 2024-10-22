
from django.utils import timezone
from asgiref.sync import sync_to_async

from core.models import HNItem
from tasks.constants.constants import \
    ITEM_STATUS_NEW, \
    ITEM_CATEGORY_DEFAULT, \
    ENDPOINT_TOPSTORIES
from typing import List, Generator
from itertools import islice
from time import sleep


class HNAPIStoryService:
    __slots__ = ['hn_api']

    def __init__(self, hn_api):
        self.hn_api = hn_api

    async def pull_top_stories(self, end_point: str = ENDPOINT_TOPSTORIES) -> None:
        """
        pull_top_stories
        Args:
            end_point:

        Returns:

        """

        top_stories_id = self.hn_api.get_top_stories(
            end_point=end_point,
            method='GET',
            params=None)

        top_story_entities = self.convert_entities_from_list(top_stories_id)
        await self.bulk_create(lst=top_story_entities)

    async def update_items(self) -> None:
        """
        update item detail on each item id by HNClient API
        @TODO: apply asynchronous for run concurrent update item implement with Redis client
        Returns:

        """
        items = await sync_to_async(
            lambda: list(HNItem.objects.filter(item_status=ITEM_STATUS_NEW).values('id', 'hn_item_id')))()
        print('length need to process, ', len(items))
        item_detail_lists = (self.hn_api.get_item_detail(method='GET', item_id=item.get('hn_item_id', 0)) for item in
                             items)

        await self.bulk_create(
            lst=item_detail_lists,
            batch_size=100,
            update_fields=[
                'item_by',
                'descendants',
                'kids',
                'item_score',
                'created_time',
                'item_title',
                'item_content',
                'item_type',
                'item_url',
                'item_status',
                'updated_at',
            ],
            unique_fields=['hn_item_id'])

    async def bulk_create(
        self,
        lst: Generator[HNItem, None, None],
        batch_size: int = 100,
        update_fields=['item_title', 'item_score', 'updated_at'],
        unique_fields=['hn_item_id']
    ) -> None:
        """
        bulk_create: upsert list of models into db
        Args:
            unique_fields:
            update_fields:
            lst:
            batch_size:

        Returns:

        """
        while True:
            batch = list(islice(lst, batch_size))
            if not batch:
                break
            await self.async_bulk_upsert(batch, update_fields, unique_fields)

    async def async_bulk_upsert(self, batch, update_fields, unique_fields) -> None:
        """

        Args:
            batch:
            update_fields:
            unique_fields:

        Returns:

        """
        sleep(5)
        await HNItem.objects.abulk_create(
            batch,
            update_conflicts=True,
            update_fields=update_fields,
            unique_fields=unique_fields)

    @staticmethod
    def convert_entities_from_list(ids: List[int]) -> Generator[HNItem, None, None]:
        """

        Args:
            ids:

        Returns:

        """
        now = timezone.now()
        return (HNItem(
            hn_item_id=item_id,
            item_status=ITEM_STATUS_NEW,
            updated_at=now,
            created_at=now,
            category_id=ITEM_CATEGORY_DEFAULT) for item_id in ids)
