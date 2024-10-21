from django.db import models


# Create your models here.
class HNItem(models.Model):
    hn_item_id = models.PositiveBigIntegerField(db_index=True, unique=True)
    deleted = models.BooleanField(null=True)
    item_type = models.CharField(max_length=20, null=True)
    item_by = models.CharField(max_length=200, null=True)
    created_time = models.DateTimeField(null=True)
    item_content = models.TextField(null=True)
    parent = models.PositiveBigIntegerField(null=True)
    kids = models.JSONField(null=True)
    item_url = models.TextField(null=True)
    item_score = models.IntegerField(null=True)
    category_id = models.PositiveBigIntegerField(null=True)
    item_title = models.TextField(null=True)
    descendants = models.PositiveBigIntegerField(null=True)
    label = models.CharField(max_length=20, null=True)
    item_status = models.IntegerField()
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'hn_item'

    # def __str__(self):
    #     return self.item_title
