from django.contrib import admin

from .models import Hotel, RoomType, Room, Feature, ClassificationFeature

admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Feature)
admin.site.register(ClassificationFeature)
