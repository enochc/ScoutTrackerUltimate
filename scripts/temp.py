
from applications.rank.models import Rank
from applications.requirement.models import Requirement
from applications.unit.models import UnitRequest
from utils.funcs import email

def run():
    req = UnitRequest.objects.all()
    for r in req:
        r.notify()