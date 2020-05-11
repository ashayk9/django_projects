from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('S','Shirts'),
    ('SW','SportsWear'),
    ('OW','Outwear'),
)
LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail",kwargs={'slug':self.slug})

    def get_add_to_cart_url(self):
        return reverse("add_to_cart",kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart",kwargs={'slug':self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity*self.item.price

    def get_total_discount_item_price(self):
        return self.quantity*self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price()-self.get_total_discount_item_price()

    def get_total_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_final_price(self):
        total=0
        for order_item in self.items.all():
            total+=order_item.get_total_price()
        return total


class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)