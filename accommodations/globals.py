__author__ = 'alexLenovo'

from accommodations.models import Dorm


def glob(request):
    camine = Dorm.objects.all()
    return {'camine': camine}

