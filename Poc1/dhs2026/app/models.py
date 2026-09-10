from django.db import models

class Speaker(models.Model):
    name = models.CharField(max_length=150)
    image_url = models.URLField(max_length=500)

    designation = models.CharField(
        max_length=255,
        help_text="e.g. 'Co-founder and Group CEO, Fractal'",
    )

    company_img_url = models.URLField(max_length=500)
    linkedin_url = models.URLField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def has_keynote_session(self):
        return self.sessions.filter(type="Keynote").exists()

    @property
    def session_type_slugs(self):
        from django.utils.text import slugify
        types = self.sessions.values_list("type", flat=True).distinct()
        return " ".join(slugify(t) for t in types)




class Sponsor(models.Model):
    class Type(models.TextChoices):
        POWER = "Power Sponsor", "Power Sponsor"
        INNOVATION = "Innovation Sponsor", "Innovation Sponsor"
        PIONEER = "Pioneer Sponsor", "Pioneer Sponsor"
        HACKDAY = "HackDay Sponsor", "HackDay Sponsor"
        LUMINARY = "AV Luminary Awards Sponsor", "AV Luminary Awards Sponsor"
        COMMUNITY = "Community Sponsor", "Community Sponsor"

    name = models.CharField(max_length=150)

    logo_url = models.URLField(max_length=500)

    type = models.CharField(
        max_length=100,
        choices=Type.choices,
        default=None
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Workshop(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=250)
    image = models.CharField(max_length=100, blank=True, null=True)
    is_sold_out = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(default=0)

    description = models.TextField(
        blank=True
    )

    instructors = models.ManyToManyField(Speaker, related_name="workshops", blank=True)


    @property
    def final_price(self):
        return self.price - ((self.price*self.discount)/100.0)

    def __str__(self):
        return self.name

class Session(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=100)
    image = models.CharField(max_length=100, blank=True, null=True)
    speakers = models.ManyToManyField(Speaker, related_name="sessions", blank=True)
    moderator = models.ForeignKey(Speaker, related_name="moderator", on_delete=models.CASCADE, blank=True, null=True)


class DownloadDetail(models.Model):
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    workshops = models.ManyToManyField(
        Workshop,
        blank=True
    )

    amount = models.IntegerField()

    payment_type = models.CharField(
        max_length=50,
        blank=True
    )  # Conference, Workshop

    status = models.CharField(
        max_length=50,
        default="Created"
    )  # Created, Success, Failed

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.razorpay_order_id