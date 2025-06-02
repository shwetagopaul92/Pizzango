from django.db import models


# Model for toppings for Pizza
class Topping(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.id} | Topping Name : {self.name}"


# Model for Addons for Subs
class Addon(models.Model):
    addons_name = models.CharField(max_length=32)
    addons_price = models.DecimalField(max_digits=6, decimal_places=2,
                                       default=0)

    def __str__(self):
        return f"{self.id} | Addon Name: {self.addons_name} | \
                 Addon Price : {self.addons_price}"


# Model to represent all the items
class Item(models.Model):
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
    size = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    toppings = models.ManyToManyField(Topping, blank=True,
                                      related_name="toppings")
    addons = models.ManyToManyField(Addon, blank=True, related_name="addons")

    def __str__(self):
        return f"{self.id} Item Category : {self.category} | \
                 Item name: {self.name} | Item type: {self.type} | \
                 Item size: {self.size} | Item price : {self.price}"


# Model to represent the orders a user makes
class Order(models.Model):
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
    size = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    toppings = models.CharField(max_length=32, blank=True)
    addons = models.CharField(max_length=32, blank=True)
    addons_price = models.DecimalField(max_digits=6, decimal_places=2,
                                       default=0)
    user_name = models.CharField(max_length=32)
    order_status = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f"{self.id} Order Status: {self.order_status} | Username : {self.user_name} | \
                Item name: {self.name} | Item type: {self.type} | \
                Item size: {self.size} | Topping : {self.toppings} | \
                Item price : {self.price} |Addon : {self.addons} | \
                Addon Price : {self.addons_price}"
