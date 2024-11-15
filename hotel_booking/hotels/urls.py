from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'hotels', HotelListViewSet, basename='hotel_list'),
router.register(r'hotel_detail', HotelDetailViewSet, basename='hotel_detail')
router.register(r'users', UserProfileViewSet, basename='user_list')
router.register(r'room', RoomListViewSet, basename='room_list')
router.register(r'room_detail', RoomDetailViewSet, basename='room_detail')
router.register(r'review', ReviewViewSet, basename='review_list')
router.register(r'booking', BookingViewSet, basename='booking_list')

urlpatterns = [
    path('', include(router.urls))
]
