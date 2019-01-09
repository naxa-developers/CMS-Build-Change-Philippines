from core.models import Notification

def reports_list(request):
    rep_dict = {}
    rep_list = []
    try:
        notification = Notification.objects.filter(
            user=request.user, read=False
            ).order_by('-pk')[:5]
        if notification:
            for item in notification:
                rep_dict['notif'] = item
                rep_dict['pk'] = item.report_id
                rep_list.append(dict(rep_dict))
            count = notification.count()
    except:
        reports = None
        count = None

    return {'notifications': rep_list, 'count':count}
