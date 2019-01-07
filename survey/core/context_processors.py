from core.models import Notification

def reports_list(request):
    try:
        notification = Notification.objects.all().order_by('-pk')[:5]
        rep_dict = {}
        rep_list = []
        for item in notification:
            rep_dict['notif'] = item
            rep_dict['pk'] = item.report_id
            rep_list.append(dict(rep_dict))
        count = Notification.objects.all().count()
    except:
        reports = None
        count = None

    return {'notifications': rep_list, 'count':count}
