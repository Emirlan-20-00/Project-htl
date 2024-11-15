from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

ROLE_CHOICES = (
    ('simpleUser', 'SimpleUser'),
    ('ownerUser', 'OwnerUser'),
)


class UserProfile(AbstractUser):
    user_role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='simpleUser')
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(70)], null=True, blank=True)


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=32, null=True, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    hotel_descriptions = models.TextField()
    country = models.CharField(max_length=32,  null=True, blank=True)
    city = models.CharField(max_length=32,  null=True, blank=True)
    address = models.CharField(max_length=32, null=True, blank=True)
    hotel_stars = models.IntegerField(choices=[(n, str(n)) for n in range(1, 6)], null=True, blank=True)
    hotel_video = models.FileField(upload_to='hotel_video/', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel_name} - {self.country} - {self.city}'


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    hotel_image = models.ImageField(upload_to='hotel_image/')


class Room(models.Model):
    room_number = models.PositiveSmallIntegerField()
    hotel_room = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    TYPE_CHOICES = (
        ('люкс', 'Люкс'),
        ('премиум', 'Премиум'),
        ('семейный', 'Семейный'),
        ('одноместный', 'Одноместный'),
        ('двухместный', 'Двухместный'),
    )
    room_type = models.CharField(max_length=12, choices=TYPE_CHOICES, null=True, blank=True)
    STATUS_CHOICES = (
        ('свободен', 'Свободен'),
        ('забранирован', 'Забранирован'),
        ('занят', 'Занят'),
    )
    room_status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='Свободен')
    room_price = models.PositiveIntegerField()
    all_inclusive = models.BooleanField(default=False)
    room_descriptions = models.TextField()

    def __str__(self):
        return f'{self.hotel_room} - {self.room_number} - {self.room_type}'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
    room_image = models.ImageField(upload_to='room_images/')


class Review(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(null=True, blank=True)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user_name} - {self.hotel} - {self.stars}'


class Booking(models.Model):
    hotel_book = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_books')
    room_book = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_book = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    total_price = models.PositiveIntegerField(default=0)
    STATUS_BOOK_CHOICES = (
        ('отменено', 'Отменено'),
        ('подтверждено', 'Подтверждено'),
    )
    status_book = models.CharField(max_length=16, choices=STATUS_BOOK_CHOICES)

    def __str__(self):
        return f'{self.user_book} - {self.hotel_book} - {self.room_book} - {self.status_book}'
