from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion

from booking.models import Booking
from .models import Hotel, Room, RoomType
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from .analysers import html_strip


@registry.register_document
class RoomDocument(Document):
    floor = fields.IntegerField()
    price = fields.DoubleField()

    room_number = StringField(
        analyzer=html_strip,
        fields={
            "raw": KeywordField(),
        }
    )

    # For extend fields
    hotel_id = fields.ObjectField(
        properties={
            "id": fields.LongField(),

            "name": StringField(
                analyzer=html_strip,
                fields={
                    "raw": KeywordField(),
                }
            ),

            "address": StringField(
                analyzer=html_strip,
                fields={
                    "raw": KeywordField(),
                }
            ),

            "city": StringField(
                analyzer=html_strip,
                fields={
                    "raw": KeywordField(),
                }
            ),

            "state": StringField(
                analyzer=html_strip,
                fields={
                    "raw": KeywordField(),
                }
            ),

            "country": StringField(
                analyzer=html_strip,
                fields={
                    "raw": KeywordField(),
                }
            )
        }
    )

    room_type_id = fields.ObjectField(
        properties={
            'total_capacity': fields.IntegerField(),

            'name': StringField(analyzer=html_strip,
                                fields={
                                    'raw': KeywordField(),
                                }, ),
            'feature_set': fields.NestedField(
                properties={
                    'value': StringField(
                        analyzer=html_strip,
                        fields={
                            'raw': KeywordField(),
                        },
                    ),
                    'classify_feature_id': fields.ObjectField(
                        properties={
                            'class_name': StringField(
                                fields={
                                    'raw': KeywordField()
                                }
                            )
                        }
                    )
                }
            )
        }
    )

    booking_set = fields.NestedField(
        properties={
            'status': StringField(
                analyzer=html_strip,
                fields={
                    'raw': KeywordField(),
                },
            ),
            'check_in_date': fields.DateField(),
            'check_out_date': fields.DateField()
        },
    )

    class Index:
        name = "rooms"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Room
        fields = ['id']
        related_models = [Booking, Hotel, RoomType]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Hotel):
            return related_instance.room_set.all()
        elif isinstance(related_instance, Booking):
            return related_instance.rooms.all()
        elif isinstance(related_instance, RoomType):
            return related_instance.room_set.all()
        return related_instance


@registry.register_document
class HotelDocument(Document):
    # ********************************************************************
    # ********************** Main data fields for search *****************
    # ********************************************************************

    id = fields.IntegerField()

    name = StringField(
        fields={
            "raw": KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    address = StringField(
        fields={
            "raw": KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    city = StringField(
        fields={
            "raw": KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    state = StringField(
        fields={
            "raw": KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    country = StringField(
        fields={
            "raw": KeywordField(),
            'suggest': fields.CompletionField(),
            'edge_ngram_completion': StringField(
                analyzer=edge_ngram_completion
            ),
        }
    )

    description = StringField()

    class Index:
        name = "hotels"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Hotel
        # fields = ['id']