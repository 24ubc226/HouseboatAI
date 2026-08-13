from django.db import models
from django.contrib.auth.models import User


# =========================================================
# PROFESSIONAL HOUSEBOAT DATASET
# =========================================================

class ProfessionalHouseboatDataset500Rows(models.Model):

    houseboatid = models.TextField(
        db_column="HouseboatID",
        primary_key=True
    )

    houseboatname = models.TextField(
        db_column="HouseboatName",
        blank=True,
        null=True
    )

    location = models.TextField(
        db_column="Location",
        blank=True,
        null=True
    )

    latitude = models.FloatField(
        db_column="Latitude",
        blank=True,
        null=True
    )

    longitude = models.FloatField(
        db_column="Longitude",
        blank=True,
        null=True
    )

    priceinr = models.IntegerField(
        db_column="PriceINR",
        blank=True,
        null=True
    )

    season = models.TextField(
        db_column="Season",
        blank=True,
        null=True
    )

    bedrooms = models.IntegerField(
        db_column="Bedrooms",
        blank=True,
        null=True
    )

    capacity = models.IntegerField(
        db_column="Capacity",
        blank=True,
        null=True
    )

    ac = models.TextField(
        db_column="AC",
        blank=True,
        null=True
    )

    luxury = models.TextField(
        db_column="Luxury",
        blank=True,
        null=True
    )

    rating = models.FloatField(
        db_column="Rating",
        blank=True,
        null=True
    )

    reviewcount = models.IntegerField(
        db_column="ReviewCount",
        blank=True,
        null=True
    )

    bookingcount = models.IntegerField(
        db_column="BookingCount",
        blank=True,
        null=True
    )

    food = models.TextField(
        db_column="Food",
        blank=True,
        null=True
    )

    wifi = models.TextField(
        db_column="WiFi",
        blank=True,
        null=True
    )

    tv = models.TextField(
        db_column="TV",
        blank=True,
        null=True
    )

    jacuzzi = models.TextField(
        db_column="Jacuzzi",
        blank=True,
        null=True
    )

    fishing = models.TextField(
        db_column="Fishing",
        blank=True,
        null=True
    )

    canoeing = models.TextField(
        db_column="Canoeing",
        blank=True,
        null=True
    )

    upperdeck = models.TextField(
        db_column="UpperDeck",
        blank=True,
        null=True
    )

    parking = models.TextField(
        db_column="Parking",
        blank=True,
        null=True
    )

    petfriendly = models.TextField(
        db_column="PetFriendly",
        blank=True,
        null=True
    )

    triptype = models.TextField(
        db_column="TripType",
        blank=True,
        null=True
    )

    suitablefor = models.TextField(
        db_column="SuitableFor",
        blank=True,
        null=True
    )

    availability = models.TextField(
        db_column="Availability",
        blank=True,
        null=True
    )

    imagefile = models.TextField(
        db_column="ImageFile",
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = "professional_houseboat_dataset_500_rows"


# =========================================================
# BOOKING
# =========================================================

class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    customer_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    houseboat = models.CharField(
        max_length=20,
        db_column="houseboat_id"
    )

    checkin = models.DateField()

    checkout = models.DateField()

    guests = models.IntegerField()
    STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
]

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="Pending"
)  

    def __str__(self):
        return f"{self.customer_name} - {self.houseboat}"


# =========================================================
# WISHLIST
# =========================================================

class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    houseboat = models.CharField(
        max_length=20,
        db_column="houseboat_id"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.houseboat}"


# =========================================================
# CONTACT MESSAGE
# =========================================================

class ContactMessage(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.name} - {self.subject}"


    