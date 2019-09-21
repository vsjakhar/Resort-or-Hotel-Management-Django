"""auragoa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from tastypie.api import Api
from jakhar.api import UserResource,DatesResource
from country.api import CountryResource, StateResource
from Guest.api import GuestResource, GworkResource, GotherResource, Guest_detailResource, Guest_fullResource, GuestgroupResource 
from management.api import StaffResource
from Room.api import Room_typeResource, RoomResource, Room_detailResource
from booking.api import SourceResource, BookingResource, Booking_detailResource, TravelResource, Room_availResource, DaybookingResource, RangebookingResource, BookingguestResource, BookingguestjsonResource, Room_room_typeResource, Booking_full_detailResource
from payment.api import PaymentResource, FolioResource
from restaurant.api import CategoryResource, MenuResource, CuisineResource, TableResource, OrderResource, Order_historyResource
from spa.api import Spa_typeResource, EquipmentResource, SpaResource, ServiceResource, Service_historyResource


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(DatesResource())
v1_api.register(CountryResource())
v1_api.register(StateResource())
v1_api.register(GuestResource())
v1_api.register(GworkResource())
v1_api.register(GotherResource())
v1_api.register(Guest_detailResource())
v1_api.register(Guest_fullResource())
v1_api.register(GuestgroupResource())
v1_api.register(StaffResource())
v1_api.register(Room_typeResource())
v1_api.register(RoomResource())
v1_api.register(Room_detailResource())
v1_api.register(SourceResource())
v1_api.register(BookingResource())
v1_api.register(Booking_detailResource())
v1_api.register(TravelResource())
v1_api.register(Room_availResource())
v1_api.register(Room_room_typeResource())
v1_api.register(DaybookingResource())
v1_api.register(RangebookingResource())
v1_api.register(BookingguestResource())
v1_api.register(BookingguestjsonResource())
v1_api.register(Booking_full_detailResource())
v1_api.register(PaymentResource())
v1_api.register(FolioResource())
v1_api.register(CategoryResource())
v1_api.register(MenuResource())
v1_api.register(CuisineResource())
v1_api.register(TableResource())
v1_api.register(OrderResource())
v1_api.register(Order_historyResource())
v1_api.register(Spa_typeResource())
v1_api.register(EquipmentResource())
v1_api.register(SpaResource())
v1_api.register(ServiceResource())
v1_api.register(Service_historyResource())


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Aura Goa | The Yoga and Spa Resort - Goa'
admin.site.site_title = 'Aura Goa | The Yoga and Spa Resort - Goa'
