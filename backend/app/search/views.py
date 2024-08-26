import abc

from django.http import HttpResponse
from elasticsearch_dsl import Q, A
from rest_framework.filters import BaseFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.documents import ArticleDocument, UserDocument, CategoryDocument
from blog.serializers import ArticleSerializer, UserSerializer, CategorySerializer
from hotel.documents import HotelDocument, RoomDocument
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_GEO_DISTANCE,
    LOOKUP_FILTER_GEO_POLYGON,
    LOOKUP_FILTER_GEO_BOUNDING_BOX,
    SUGGESTER_COMPLETION, LOOKUP_FILTER_TERM, FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
    FUNCTIONAL_SUGGESTER_COMPLETION_MATCH, SUGGESTER_TERM, SUGGESTER_PHRASE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    GeoSpatialFilteringFilterBackend,
    GeoSpatialOrderingFilterBackend,
    NestedFilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend, FunctionalSuggesterFilterBackend, CompoundSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)

from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from .serializers import HotelDocumentSerializer, RoomDocumentSerializer
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f"Found {response.hits.total.value} hit(s) for query: '{query}'")

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)


# views


class SearchUsers(PaginatedElasticSearchAPIView):
    serializer_class = UserSerializer
    document_class = UserDocument

    def generate_q_expression(self, query):
        return Q("bool",
                 should=[
                     Q("match", username=query),
                     Q("match", first_name=query),
                     Q("match", last_name=query),
                 ], minimum_should_match=1)


class SearchCategories(PaginatedElasticSearchAPIView):
    serializer_class = CategorySerializer
    document_class = CategoryDocument

    def generate_q_expression(self, query):
        return Q(
            "multi_match", query=query,
            fields=[
                "name",
                "description",
            ], fuzziness="auto")


class SearchArticles(PaginatedElasticSearchAPIView):
    serializer_class = ArticleSerializer
    document_class = ArticleDocument

    def generate_q_expression(self, query):
        return Q(
            "multi_match", query=query,
            fields=[
                "title",
                "author",
                "type",
                "content"
            ], fuzziness="auto")


class AvailableRoomFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        """
        Return a filtered queryset.
        """

        params = request.query_params.copy()
        checkin_date = params.get('checkin_date')
        checkout_date = params.get('checkout_date')
        number_of_adults = params.get('number_of_adults')
        number_of_children = params.get('number_of_children')

        if checkout_date and checkin_date and number_of_children and number_of_adults:
            total_person = int(number_of_children) + int(number_of_adults)

            q = Q(
                'bool',
                must_not=[
                    Q('nested',
                      path='booking_set',
                      query=Q("bool",
                              must=[
                                  Q("range", **{"booking_set.check_in_date": {"lte": checkout_date}}),
                                  Q("range", **{"booking_set.check_out_date": {"gte": checkin_date}}),
                                  Q("match", **{"booking_set.status": "PENDING"})
                              ]
                              )
                      )
                ]
            )

            aggs_query = {'aggs': {
                "hotel_gr": {
                    "terms": {
                        "field": "hotel_id.id"
                    },
                    "aggs": {
                        "total_capacity_filter": {
                            "sum": {
                                "field": "room_type_id.total_capacity"
                            }
                        },
                        "filtered_hotels": {
                            "bucket_selector": {
                                "buckets_path": {
                                    "totalCapacity": "total_capacity_filter"
                                },
                                "script": f"params.totalCapacity >= {total_person}"
                            }
                        }
                    }
                }
            }
            }
            queryset = queryset.query(q)
            queryset = queryset.update_from_dict(aggs_query)
            print(queryset.to_dict())

            return queryset
        else:
            aggs_query = {'aggs': {
                "hotel_gr": {
                    "terms": {
                        "field": "hotel_id.id"
                    }
                }
            }
            }
            queryset = queryset.update_from_dict(aggs_query)

            return queryset


class HotelDocumentViewSet(DocumentViewSet):
    """The HotelDocumentViewSet view.
        This replaces other service methods with other methods.
        The flow set:
        1. Query the hotel basic ( location, name, description) by Elasticsearch. it's stronger for filter
        2. After getting list of relate hotel, pass it to available hotel room

    """

    document = RoomDocument
    serializer_class = RoomDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        AvailableRoomFilterBackend,
        NestedFilteringFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]
    pagination_class = LimitOffsetPagination

    # Define search fields
    search_fields = (
        'hotel_id.state',
        'hotel_id.city',
        'hotel_id.country',
    )

    # Define filtering fields
    filter_fields = {
        'features': {
            'field': 'room_type_id.feature_set.value.raw',
            'lookups': [
                LOOKUP_QUERY_IN
            ]
        },
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
            ],
        },
        'hotel_id': {
            'field': 'hotel_id.id',
            'lookups': [
                LOOKUP_FILTER_TERM,
                # LOOKUP_FILTER_TERMS,
                # LOOKUP_FILTER_PREFIX,
                # LOOKUP_FILTER_WILDCARD,
                # LOOKUP_QUERY_IN
            ],
        },
        'name': {
            'field': 'hotel_id.name.raw',
            'lookups': [
                LOOKUP_FILTER_TERM,
                # LOOKUP_FILTER_TERMS,
                # LOOKUP_FILTER_PREFIX,
                # LOOKUP_FILTER_WILDCARD,
                # LOOKUP_QUERY_IN
            ],
        },
        'address': {
            'field': 'hotel_id.address.raw',
            'lookups': [
                LOOKUP_FILTER_TERM,
                # LOOKUP_FILTER_TERMS,
                # LOOKUP_FILTER_PREFIX,
                # LOOKUP_FILTER_WILDCARD,
                # LOOKUP_QUERY_IN
            ],
        },
        'state': {
            'field': 'hotel_id.state.raw',
            'lookups': [
                LOOKUP_FILTER_TERM,
                # LOOKUP_FILTER_TERMS,
                # LOOKUP_FILTER_PREFIX,
                # LOOKUP_FILTER_WILDCARD,
            ],
        },
        'city': {
            'field': 'hotel_id.city.raw',
            'lookups': [
                LOOKUP_FILTER_TERM,
                # LOOKUP_FILTER_TERMS,
                # LOOKUP_FILTER_PREFIX,
                # LOOKUP_FILTER_WILDCARD,
                # LOOKUP_QUERY_IN
            ],
        },
        'country': {
            'field': 'hotel_id.country.raw',
            'lookups': [
                LOOKUP_FILTER_TERM,
                # LOOKUP_FILTER_TERMS,
                # LOOKUP_FILTER_PREFIX,
                # LOOKUP_FILTER_WILDCARD,
                # LOOKUP_QUERY_IN
            ],
        },
        'price': {
            'field': 'price',
            'lookups': [
                LOOKUP_FILTER_RANGE
            ],
        },
    }
    # Define ordering fields
    ordering_fields = {
        'name': None,
        'city': 'hotel_id.city',
        'state': 'hotel_id.state',
        'country': 'hotel_id.country',
    }

    nested_filter_fields = {
        'features': {
            'field': 'room_type_id.feature_set.value.raw',
            'path': 'room_type_id.feature_set',
            'lookups': [
                LOOKUP_FILTER_TERM,
                LOOKUP_FILTER_TERMS
            ],
        },
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        res = queryset.execute()
        print(queryset.to_dict())
        hotel_ids = [item.key for item in res.aggregations.hotel_gr.buckets]

        queryset = HotelDocument.search().filter("terms", id=hotel_ids)
        # queryset = s.execute()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = HotelDocumentSerializer(page, many=True)
            # serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HotelDocumentSerializer(queryset, many=True)
        # serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class SuggestDocumentViewSet(DocumentViewSet):
    """
    Support auto-complete search for multiple fields
    usage: address_suggest=A&city_suggest=B...
    """

    document = HotelDocument
    serializer_class = HotelDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        SuggesterFilterBackend,
        FunctionalSuggesterFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,

    ]
    pagination_class = LimitOffsetPagination

    # Define search fields
    search_fields = (
        'name',
        'address',
        'city',
        'state',
        'country',
    )

    # Define filtering fields
    filter_fields = {
        'id': None,
        'name': 'name.raw',
        'city': 'city.raw',
        'state': 'state.raw',
        'country': 'country.raw',
    }

    # Define ordering fields
    ordering_fields = {
        'id': None,
        'name': None,
        'city': None,
        'country': None,
    }

    # Specify default ordering
    ordering = ('id', 'name',)

    # Suggester fields
    suggester_fields = {
        'name_suggest': {
            'field': 'name.suggest',
            'suggesters': [
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,
                SUGGESTER_COMPLETION,
            ],
            'default_suggester': SUGGESTER_COMPLETION,
        },
        'address_suggest': {
            'field': 'address.suggest',
            'suggesters': [
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,
                SUGGESTER_COMPLETION,
            ],
            'default_suggester': SUGGESTER_COMPLETION,
        },
        'city_suggest': {
            'field': 'city.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },

        'state_suggest': {
            'field': 'state.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'default_suggester': SUGGESTER_COMPLETION,
        },

        'country_suggest': {
            'field': 'country.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'default_suggester': SUGGESTER_COMPLETION,
        },
    }

    # Functional suggester fields
    functional_suggester_fields = {
        'name_suggest': {
            'field': 'name.raw',
            'suggesters': [
                FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            ],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
        },
        'name_match_suggest': {
            'field': 'name',
            'suggesters': [
                FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
            ],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
        },
        'city_suggest': {
            'field': 'city.raw',
            'suggesters': [
                FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            ],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
        },
        'state_suggest': {
            'field': 'state.suggest',
            'suggesters': [
                FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            ],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
        },
        'country_suggest': {
            'field': 'country.raw',
            'suggesters': [
                FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            ],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
        },
    }
