from django.db import models
from decimal import Decimal
"""
Model structure initial concept from my own Portfolio 4 --
https://github.com/jbillcliffe/django-renterprise/tree/main/items/models.py
"""


class ItemType(models.Model):
    """
    Fields for the ItemType model, including the CloudinaryField which
    uses a URL for it's data, which can then be linked to an image
    which is hosted online
    """
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    cost_initial = models.DecimalField(max_digits=6, decimal_places=2)
    cost_week = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    # order by name 0-9 then A-Z
    class Meta:
        ordering = ["name"]

    # so the name will replace "ItemType Object" in all instances
    def __str__(self):
        """
        String representation of the item type object.
        """
        return self.name


class Item(models.Model):
    """
    Fields for the Item model, this is the storage of stock, to it
    is a list of ItemTypes with a serial number attached to it.
    The status is also important as it will determine the availability
    of it to hire.
    """
    AVAILABLE = 0
    SCRAPPED = 1
    MISSING = 2
    SOLD = 3
    REPAIR = 4
    STATUS = (
        (AVAILABLE, 'Available'),
        (SCRAPPED, 'Scrapped'),
        (MISSING, 'Missing'),
        (SOLD, 'Sold'),
        (REPAIR, 'Repair'),
    )

    """
    (AVAILABLE, 'Available', 'success-subtle white-text'),
        (SCRAPPED, 'Scrapped', 'secondary-subtle white-text'),
        (MISSING, 'Missing', 'danger-subtle white-text'),
        (SOLD, 'Sold', 'primary-subtle white-text'),
        (REPAIR, 'Repair', 'warning-subtle'),
        """

    item_type = models.ForeignKey(
        ItemType, on_delete=models.CASCADE, related_name="item_type"
    )
    item_serial = models.CharField(max_length=200)
    delivery_date = models.DateField(null=True, blank=True)
    collect_date = models.DateField(null=True, blank=True)
    repair_date = models.DateField(null=True, blank=True)
    income = models.DecimalField(max_digits=6,
                                 decimal_places=2,
                                 default=Decimal('0.00'))
    status = models.IntegerField(choices=STATUS, default=AVAILABLE)

    class Meta:
        # order by item_type name 0-9 then A-Z
        ordering = ["item_type", "status", "item_serial"]

    # return a formatted string for the name of the item type
    def item_type_name(self):
        """
        Returning the item_type.name as a seperate entity as it is referred to
        frequently and is in a different model
        """
        return self.item_type.name

    def item_type_category(self):
        """
        Returning the category as a seperate entity as it is referred to
        frequently and is in a different model
        """
        return self.item_type.category

    def status_str(self):
        """
        Returning the human readable version of status
        """
        return self.STATUS[self.status][1]

    def item_css_status(self):
        """
        Returning the css ready version of status (noteably
        in lower case).
        """
        # status_name = str(self.STATUS[self.status][1]).replace('/', '_').lower()
        
        if self.STATUS[self.status][1] == "warning"
            

        if self.STATUS != REPAIR:
            
        return self
         (AVAILABLE, 'Available', 'success-subtle white-text'),
        (SCRAPPED, 'Scrapped', 'secondary-subtle white-text'),
        (MISSING, 'Missing', 'danger-subtle white-text'),
        (SOLD, 'Sold', 'primary-subtle white-text'),
        (REPAIR, 'Repair', 'warning-subtle'),
    )

    def __str__(self):
        """
        String representation of the item type object.
        """
        return self.item_type.name
