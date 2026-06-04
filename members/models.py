from django.db import models

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)

class Court(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Under Maintenance'),
    ]
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    TYPE_CHOICES = [
        ('match', 'Match'),
        ('training', 'Training'),
        ('event', 'Event'),
    ]
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='training')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Membership(models.Model):
    TYPE_CHOICES = [
        ('junior', 'Junior'),
        ('adult', 'Adult'),
        ('vip', 'VIP'),
    ]
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='adult')
    expiry_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.member.firstname} - {self.type}"

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    important = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Payment(models.Model):
    PAYMENT_TYPE = [
        ('membership', 'Membership Fee'),
        ('court', 'Court Booking'),
    ]
    PAYMENT_METHOD = [
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
    ]
    STATUS = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.member} - {self.payment_type} - {self.status}"