from core.models import Notification

def reports_list(request):
    rep_dict = {}
    rep_list = []
    count = 0
    try:
        notification = Notification.objects.filter(read=False, user=request.user).order_by('-pk')[:5]
        if notification:
            for item in notification:
                rep_dict['notif'] = item
                rep_dict['pk'] = item.report_id
                rep_list.append(dict(rep_dict))
            count = notification.count()

    except:
        reports = None

    return {'notifications': rep_list, 'count':count}
