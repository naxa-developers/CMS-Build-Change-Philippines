from core.models import SubstepReport

def reports_list(request):
    try:
        reports = SubstepReport.objects.all().order_by('-pk')[:5]
        count = SubstepReport.objects.all().count()
    except:
        reports = None
        count = None

    return {'reports': reports, 'count':count}
