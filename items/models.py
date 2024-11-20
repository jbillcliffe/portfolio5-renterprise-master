from decimal import Decimal
from django.db import models

"""
Model structure initial concept from my own Portfolio 4 --
https://github.com/jbillcliffe/django-renterprise/tree/main/items/models.py
"""


class ItemType(models.Model):
    """
    Fields for the ItemType model, including the ImageField which
    contains a URL for it's data, which can then be linked to an image
    which is hosted online (local for debug)
    """
    name = models.CharField(max_length=60)
    sku = models.CharField(max_length=15, unique=True, default="MH-")
    category = models.CharField(max_length=50)
    cost_initial = models.DecimalField(max_digits=6, decimal_places=2)
    cost_week = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to=, null=True, blank=True)
    meta_tags = models.TextField(null=True, blank=True)

    # Order by category and then name to create the category separation
    # in the list view
    class Meta:
        ordering = ["category", "name"]

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

    # Creating word variables to integer values
    AVAILABLE = 0
    SCRAPPED = 1
    MISSING = 2
    SOLD = 3
    REPAIR = 4

    # Creating tuples under the STATUS variable where an integer has a
    # relation to a string
    STATUS = (
        (AVAILABLE, 'Available'),
        (SCRAPPED, 'Scrapped'),
        (MISSING, 'Missing'),
        (SOLD, 'Sold'),
        (REPAIR, 'Repair')
    )

    # Creating tuples under the CSS_STATUS variable where an integer has
    # a relation to a string
    CSS_STATUS = (
        (AVAILABLE, 'success'),
        (SCRAPPED, 'secondary'),
        (MISSING, 'danger'),
        (SOLD, 'primary'),
        (REPAIR, 'warning')
    )

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
    # For a possible future where items can be viewed with their own unique
    # photo rather than a generic picture by its type.
    unique_image_field = models.ImageField(null=True, blank=True)

    class Meta:
        # order by item_type name 0-9 then A-Z, then by serial number
        ordering = ["item_type", "item_serial"]

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
        Returning the css class to return to the template
        based on it's status value saved.
        """
        return self.CSS_STATUS[self.status][1]

    def __str__(self):
        """
        String representation of the item type object.
        """
        return self.item_type.name
