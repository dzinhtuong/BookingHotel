from django.urls import path

from .views import SearchArticles, SearchCategories, SearchUsers, HotelDocumentViewSet, SuggestDocumentViewSet

urlpatterns = [
    path("user/<str:query>/", SearchUsers.as_view()),
    path("category/<str:query>/", SearchCategories.as_view()),
    path("article/<str:query>/", SearchArticles.as_view()),
    path("hotel/", HotelDocumentViewSet.as_view({'get': 'list'})),
    path("suggest/", SuggestDocumentViewSet.as_view({'get': 'suggest'})),
]
