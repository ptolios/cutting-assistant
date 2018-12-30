from django.db import models
from django.utils import timezone


def now():
    # since seconds and microseconds are not important
    #  we set them to zero for comparison purposes
    return timezone.now().replace(second=0, microsecond=0)


class OrderStatus:
    DRAFT = 1
    ACTIVE = 2
    APPROVED = 3
    IN_PROGRESS = 4
    COMPLETED = 5


class Order(models.Model):
    
    class Meta:
        verbose_name = "Παραγγελία"
        verbose_name_plural = "Παραγγελίες"

    STATUS_CHOICES = (
        (OrderStatus.DRAFT, "Πρόχειρη"),
        (OrderStatus.ACTIVE, "Ενεργή"),
        (OrderStatus.APPROVED, "Εγκεκριμένη"),
        (OrderStatus.IN_PROGRESS, "Εκτελείται"),
        (OrderStatus.COMPLETED, "Ολοκληρωμένη"),
    )
    customer = models.CharField(
        "Πελάτης", max_length=100, blank=False
    )
    placement_datetime = models.DateTimeField(
        "Ημερομηνία παραγγελίας", blank=True, default=now
    )
    delivery_date = models.DateField(
        "Ημερομηνία παράδοσης", blank=True, null=True
    )
    status = models.IntegerField(
        "Κατάσταση", choices=STATUS_CHOICES, null=False, blank=False, default=0
    )

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"
#TODO: (panos) Add the clean() method to validate the model fields.
# Check that delivery_date is always later than the placement_date
# see: https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model.clean


class OrderItem(models.Model):
    
    class Meta:
        verbose_name = "Στοιχείο Παραγγελίας"
        verbose_name_plural = "Στοιχεία Παραγγελίας"

    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    material = models.CharField("Υλικό", max_length=100, null=False, blank=False, default="")
    quantity = models.PositiveSmallIntegerField("Ποσότητα")
    x_dimension = models.DecimalField(
        "Διάσταση Χ", decimal_places=1, max_digits=5
    )
    y_dimension = models.DecimalField(
        "Διάσταση Υ", decimal_places=1, max_digits=5
    )

    def total_area(self):
        # Returns the area from the two dimanesions in square meters
        return self.quantity * self.x_dimension * self.y_dimension / 1000000

    def __str__(self):
        return f"{self.order._meta.verbose_name}_{self.order.id} {self._meta.verbose_name}_{self.id}"
