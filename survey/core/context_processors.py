from core.models import SubstepReport

def reports_list(request):
    try:
        reports = SubstepReport.objects.all().order_by('-pk')[:5]
    except:
        reports = None

    return {'reports': reports}
