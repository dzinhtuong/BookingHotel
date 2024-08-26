from rest_framework import serializers

from booking.models import Booking
from .models import Hotel, Room, RoomType, Feature, ClassificationFeature, BedType


class FeatureReadSerializer(serializers.ModelSerializer):
    classify_feature = serializers.CharField(source='classify_feature_id.class_name', read_only=True)

    class Meta:
        model = Feature
        exclude = ['room_types', 'classify_feature_id']


class FeatureWriteSerializer(serializers.ModelSerializer):
    classify_feature_id = serializers.PrimaryKeyRelatedField(queryset=ClassificationFeature.objects.all(),
                                                             many=False)

    class Meta:
        model = Feature
        fields = '__all__'


class ClassificationFeatureReadSerializer(serializers.ModelSerializer):
    feature_set = FeatureReadSerializer(many=True, read_only=True)

    class Meta:
        model = ClassificationFeature
        fields = '__all__'


class ClassificationFeatureWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassificationFeature
        fields = '__all__'


class BedTypeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedType
        exclude = ['room_types']


class BedTypeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedType
        exclude = ['room_types']


class RoomReadSerializerOfRoomType(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['hotel_id']


class RoomTypeReadSerializer(serializers.ModelSerializer):
    feature_set = FeatureReadSerializer(many=True, read_only=True)
    bedtype_set = BedTypeReadSerializer(many=True, read_only=True)
    room_set = RoomReadSerializerOfRoomType(many=True, read_only=True)
    total_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = RoomType
        fields = '__all__'


class RoomTypeWriteSerializer(serializers.ModelSerializer):
    feature_set = serializers.PrimaryKeyRelatedField(queryset=Feature.objects.all(),
                                                     many=True)
    bedtype_set = serializers.PrimaryKeyRelatedField(queryset=BedType.objects.all(),
                                                     many=True)

    class Meta:
        model = RoomType
        fields = '__all__'
        read_only_fields = ['hotel_id']

    def to_internal_value(self, data):
        data = super(RoomTypeWriteSerializer, self).to_internal_value(data)
        hotel_id = self.context['view'].kwargs.get('pk')
        instance = Hotel.objects.get(pk=hotel_id)
        data['hotel_id'] = instance
        return data


class RoomTypeDetailWriteSerializer(serializers.ModelSerializer):
    feature_set = serializers.PrimaryKeyRelatedField(queryset=Feature.objects.all(),
                                                     many=True)
    bedtype_set = serializers.PrimaryKeyRelatedField(queryset=BedType.objects.all(),
                                                     many=True)

    class Meta:
        model = RoomType
        fields = '__all__'
        read_only_fields = ['hotel_id']


class BookingNoNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['rooms']


class RoomReadSerializer(serializers.ModelSerializer):
    room_type_id = serializers.IntegerField(source='room_type_id.id', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['hotel_id']


class RoomWriteSerializer(serializers.ModelSerializer):
    room_type_id = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all(), many=False)

    def validate_room_type_id(self, value):
        hotel_id = self.context['view'].kwargs.get('pk')
        if value.hotel_id.id != hotel_id:
            raise serializers.ValidationError("Can not assign a room type to non-owner hotel")
        return value

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['hotel_id']

    def to_internal_value(self, data):
        data = super(RoomWriteSerializer, self).to_internal_value(data)
        hotel_id = self.context['view'].kwargs.get('pk')
        instance = Hotel.objects.get(pk=hotel_id)
        data['hotel_id'] = instance
        return data


class RoomDetailWriteSerializer(serializers.ModelSerializer):
    room_type_id = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all(), many=False)

    def validate_room_type_id(self, value):
        hotel_id = self.context['view'].kwargs.get('hotel_id')
        if value.hotel_id.id != hotel_id:
            raise serializers.ValidationError("Can not assign a room type to non-owner hotel")
        return value

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['hotel_id']


class HotelReadSerializer(serializers.ModelSerializer):
    rooms = RoomReadSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        exclude = ['owners']


class HotelSerializer(serializers.ModelSerializer):
    # If you want to append nested room in Hotel, change name to room_set
    rooms = RoomReadSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'
