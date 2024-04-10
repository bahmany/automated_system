from datetime import datetime
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
import pytz
from rest_framework.response import Response
from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil, mil_to_sh, mil_to_sh_with_time


def set_timezone(request):
    if request.user.is_active == False:
        return HttpResponse(json.dumps({}),
                        content_type="application/json"
                        )

    if request.method == 'POST':
        bb = json.loads(request.body.decode("utf-8"))
        request.user.timezone = bb['timezone']
        request.user.save()
        request.session['django_timezone'] = bb['timezone']
        # print("set_timezone redirected")

        return redirect('/')
    else:
        return render(request, 'forms/Infrustructure/Timezone/template.html',
                      {'timezones': pytz.common_timezones,
                       "value":datetime.now()
                      })
def get_timezone(request):
    if request.user.is_active == False:
        return HttpResponse(json.dumps({"timezone":"Asia/Tehran"}),
                        content_type="application/json"
                        )
    return HttpResponse(json.dumps({"timezone":request.user.timezone}),
                        content_type="application/json"
                        )

def get_time(request):
    res = {}
    dateMil = datetime.now().strftime("%Y-%m-%d %H:%M")
    currentDay = mil_to_sh_with_time( dateMil )
    res["currentDatetime"] = currentDay
    if request.user.timezone != "Asia/Tehran":
        res["currentDatetime"] = dateMil
    return HttpResponse(json.dumps(res),
                        content_type="application/json"
                        )

