import string
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import Role
from booking.models import Score, RatingType
from hotel.models import Hotel, Room, RoomType, Feature, BedType, ClassificationFeature
import csv
import sys

DEFAULT_PASS = '123456'

SMALL_CONFIG = DEFAULT_CONFIG ={
    'user_size': 10,
    'hotel_size': 50
}

MEDIUM_CONFIG = {
    'user_size': 200,
    'hotel_size': 500
}

LARGE_CONFIG = {
    'user_size': 500,
    'hotel_size': 900
}


def print_status_bar(iteration, total, prefix='Progress:', suffix='Complete', length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    # sys.stdout.flush()


class Command(BaseCommand):
    help = "Populates the database with some testing data."

    def add_arguments(self, parser):
        # Define custom arguments and options for the command
        parser.add_argument('arg1', type=str, choices=['small', 'medium', 'large'],
                            help='Choose size: small, medium, large')

    def handle(self, *args, **options):
        size = options['arg1']

        if size == 'small':
            _config = SMALL_CONFIG
        elif size == 'medium':
            _config = MEDIUM_CONFIG
        elif size == 'large':
            _config = LARGE_CONFIG
        else:
            _config = DEFAULT_CONFIG

        self.stdout.write(self.style.SUCCESS("Started database population process..."))

        count = 1
        with open('booking/management/commands/init_db/score.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row.pop('id')
                score_obj = Score(**row)
                score_obj.save()
                print_status_bar(count, total=10, prefix='Progress score:', suffix='Complete',
                                 length=50)
                count += 1
        print("")

        count = 1
        with open('booking/management/commands/init_db/rating_type.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row.pop('id')
                rating_type_obj = RatingType(**row)
                rating_type_obj.save()
                print_status_bar(count, total=10, prefix='Progress rating type:', suffix='Complete',
                                 length=50)
                count += 1
        print("")

        count = 1
        with open('booking/management/commands/init_db/classification_feature.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row.pop('id')
                cls_feature_obj = ClassificationFeature(**row)
                cls_feature_obj.save()
                print_status_bar(count, total=30, prefix='Progress classify feature:', suffix='Complete',
                                 length=50)
                count += 1

        print("")
        count = 1
        features = []
        with open('booking/management/commands/init_db/feature.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                feature_obj = Feature(classify_feature_id=ClassificationFeature.objects.get(
                    id=row.get('classify_feature_id')),
                    value=str(row.get('value')))
                feature_obj.save()
                features.append(feature_obj)
                print_status_bar(count, total=100, prefix='Progress feature:', suffix='Complete', length=50)
                count += 1
        print("")
        count = 1
        bedtypes = []
        with open('booking/management/commands/init_db/bed_type.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bedtype_obj = BedType(name=str(row.get('name')),
                                      capacity=int(row.get('capacity')))
                bedtype_obj.save()
                bedtypes.append(bedtype_obj)
                print_status_bar(count, total=20, prefix='Progress bedtype:', suffix='Complete', length=50)
                count += 1

        # Create Role
        print("")
        count = 1
        roles = []
        for _role in Role.ROLE_CHOICES:
            role_obj = Role(name=_role[0])
            role_obj.save()
            roles.append(role_obj)
            print_status_bar(count, total=3, prefix='Progress role:', suffix='Complete', length=50)
            count += 1

        print("")
        users = []
        count = 1
        with open('booking/management/commands/init_db/user.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if count > _config.get('user_size'):
                    break
                user_obj = User.objects.create_user(username=row.get('username'),
                                                    password=DEFAULT_PASS,
                                                    first_name=row.get('first_name'),
                                                    last_name=row.get('last_name'),
                                                    email=row.get('email'))
                user_obj.save()
                users.append(user_obj)
                print_status_bar(count, total=_config.get('user_size'), prefix='Progress user:', suffix='Complete',
                                 length=50)
                count += 1

                user_obj.roles.add(roles[0])

        # Create some gest user and admin account
        u = User.objects.create_user(username='guest', password=DEFAULT_PASS)
        u.save()
        u.roles.add(roles[1])
        u = User.objects.create_superuser(username='admin', password=DEFAULT_PASS)
        u.save()
        u.roles.add(roles[2])

        print("")
        count = 1
        with open('booking/management/commands/init_db/hotel.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if count > _config.get('hotel_size'):
                    break
                # these field will not include, if needed, we can include again
                row.pop('id')
                row.pop('owners')

                hotel_obj = Hotel(**row)
                hotel_obj.save()
                hotel_obj.owners.add(random.choice(users))

                # Create room type:
                room_types = []
                for t in range(random.randint(10, 20)):
                    room_type_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                    room_type_obj = RoomType(
                        hotel_id=hotel_obj,
                        name=room_type_code,
                        description='leave this filed',
                        base_price=random.randint(10000, 1000000))
                    room_type_obj.save()

                    room_type_obj.feature_set.set(random.sample(features, k=10))

                    random_weight = random.choices([1, 2, 3, 4], [5, 1, 1, 1], k=1)[0]
                    room_type_obj.bedtype_set.set(random.sample(bedtypes, k=random_weight))

                    room_types.append(room_type_obj)

                # Create rooms
                prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
                for r in range(random.randint(10, 20)):
                    room_obj = Room(hotel_id=hotel_obj,
                                    room_type_id=random.choice(room_types),
                                    room_number=f'{prefix}{r:04d}',
                                    floor=random.randint(1, 100),
                                    price=random.randint(10000, 1000000),
                                    description='leave this field')
                    room_obj.save()

                print_status_bar(count, total=_config.get('hotel_size'), prefix='Progress hotel:', suffix='Complete',
                                 length=50)
                count += 1

        self.stdout.write(self.style.SUCCESS("Successfully populated the database."))

    def clean_data(self):
        pass
