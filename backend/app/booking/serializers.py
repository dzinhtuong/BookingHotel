import datetime
from rest_framework.exceptions import NotFound
from rest_framework import serializers
from booking.models import Booking, GuestReview, RatingType, Score, GuestViewRating
from hotel.models import Room, Hotel
from hotel.serializers import RoomReadSerializer
from rest_framework.generics import get_object_or_404
from django.db.models import Q

class BookingReadSerializer(serializers.ModelSerializer):
    rooms = RoomReadSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        exclude = ['guest_id']


class BookingWriteSerializer(serializers.ModelSerializer):
    rooms = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), many=True)
    hotel_id = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), many=False)

    class Meta:
        model = Booking
        read_only_fields = ['total_price', ]
        exclude = ['guest_id']

    def validate_room_availability(self, validated_data):
        is_available = Booking.objects.filter(check_in_date__lte=validated_data['check_out_date'],
                                            check_out_date__gte=validated_data['check_in_date'],
                                            status=Booking.BookingStatus.PENDING,
                                            rooms__in=validated_data['rooms']).exists()
        return is_available

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        _rooms = data['hotel_id'].room_set.all()
        for room_obj in data['rooms']:

            if room_obj not in _rooms:
                raise NotFound("room is not reside hotel")

        if self.validate_room_availability(data):
            raise NotFound("No available room")
        data['guest_id'] = self.context['request'].user

        return data


    def validate(self, data):
        check_in_date = data.get('check_in_date')
        if check_in_date:
            if check_in_date < datetime.date.today():
                raise serializers.ValidationError("Check-in date must be greater than today")

        check_out_date = data.get('check_out_date')
        if check_out_date:
            if check_out_date < datetime.date.today():
                raise serializers.ValidationError("Check-out date must be greater than today")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise serializers.ValidationError("Check-in date must be before check-out date")
        return data


class RatingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingType
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'


class GuestViewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestViewRating
        fields = ['rating_type_id', 'score_id']


class GuestViewRatingReadSerializer(serializers.ModelSerializer):
    rating_type = RatingTypeSerializer(source='rating_type_id', read_only=True)
    score = ScoreSerializer(source='score_id', read_only=True)

    class Meta:
        model = GuestViewRating
        fields = ['rating_type', 'score']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['rating_type'] = instance.rating_type_id.name
        data['score'] = instance.score_id.quality
        return data


class GuestReviewReadSerializer(serializers.ModelSerializer):
    guestviewrating_set = GuestViewRatingReadSerializer(many=True, read_only=True)

    class Meta:
        model = GuestReview
        fields = ('id', 'comment', 'guestviewrating_set')


class GuestReviewWriteSerializer(serializers.ModelSerializer):
    guestviewrating_set = GuestViewRatingSerializer(many=True)

    class Meta:
        model = GuestReview
        fields = ('comment', 'guestviewrating_set', 'id', 'booking_id')
        read_only_fields = ('id', 'booking_id')

    def create(self, validated_data):
        ratings_data = validated_data.pop('guestviewrating_set')
        booking_id = self.context['view'].kwargs.get('pk')
        booking_instance = get_object_or_404(Booking, pk=booking_id)

        guest_review = GuestReview.objects.create(booking_id=booking_instance, **validated_data)

        for rating_data in ratings_data:
            GuestViewRating.objects.create(guest_review_id=guest_review, **rating_data)
        return guest_review

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()

        ratings_data = validated_data.get('guestviewrating_set', [])
        for rating_data in ratings_data:
            rating_type_id = rating_data.get('rating_type_id', None)
            score_id = rating_data.get('score_id', None)

            if rating_type_id:
                rating, created = GuestViewRating.objects.get_or_create(guest_review_id=instance,
                                                                        rating_type_id=rating_type_id,
                                                                        defaults={'score_id': score_id})
                if not created:
                    rating.score_id = score_id
                    rating.save()

        return instance
