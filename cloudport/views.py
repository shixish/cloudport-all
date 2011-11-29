from django.http import HttpResponse

import datetime
def time(request):
    now = datetime.datetime.now()
    html = "<html><body>Hi everybody this the time and date today: %s</body>" %now
    return HttpResponse(html);

def test_date(request):
    return HttpResponse("hiiiiiiiiii")
