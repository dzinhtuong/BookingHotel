from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from hotel.documents import HotelDocument, RoomDocument


class HotelDocumentSerializer(DocumentSerializer):
    """Serializer for hotel document."""

    class Meta:
        document = HotelDocument
        fields = (
            'id',
            "name",
            "address",
            "city",
            "state",
            "country",
            "description"
        )


class RoomDocumentSerializer(DocumentSerializer):
    """Serializer for room document."""

    class Meta:
        document = RoomDocument
        fields = '__all__'
