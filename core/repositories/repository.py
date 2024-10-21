from itertools import islice
from django.db import models

from typing import List


class BaseRepository:
    __slots__ = ['model']

    def __init__(self, model):
        self.model = model

    def bulk_create(self, lst: List[models.Model], batch_size=100):
        """
        bulk_create: upsert list of models into db
        Args:
            lst:
            batch_size:

        Returns:

        """
        while True:
            batch = list(islice(lst, batch_size))
            if not batch:
                break
            self.model.objects.bulk_create(batch, batch_size)
