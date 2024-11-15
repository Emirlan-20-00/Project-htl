from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name']


class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'country', 'city', 'hotel_stars', 'created_date']


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room_image']


class RoomSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'hotel_room', 'room_number', 'room_price', 'room_status',
                  'all_inclusive', 'room_descriptions', 'room_images']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateTimeField(format='%d-%m-%Y - %H:%M')
    check_out = serializers.DateTimeField(format='%d-%m-%Y - %H:%M')

    class Meta:
        model = Booking
        fields = '__all__'


class HotelDetailSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    hotel_images = HotelImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    owner = UserProfileSimpleSerializer()
    hotel_books = BookingSerializer(many=True, read_only=True)
    created_date = serializers.DateField(format='%d-%m-%Y',)

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'owner', 'hotel_descriptions', 'country', 'city', 'address', 'hotel_stars',
                  'hotel_video', 'created_date', 'rooms', 'hotel_images', 'reviews', 'hotel_books']