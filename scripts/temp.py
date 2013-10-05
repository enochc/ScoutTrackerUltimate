from applications.rank.models import Rank
from applications.requirement.models import Requirement

def run():
    ranks = Rank.objects.all()
    for rank in ranks:
        print rank
        
        reqs = Requirement.objects.filter(rank=rank)
        for req in reqs:
            for req in reqs:
                rank.add_requiremnt(req, req.order, req.is_last)