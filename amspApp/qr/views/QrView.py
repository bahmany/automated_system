from django.shortcuts import render_to_response
from django.template import RequestContext

# class QrViewSet(viewsets.ModelViewSet):
#     lookup_field = 'id'
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh
from amspApp.Letter.models import Inbox
from amspApp.Sales.models import HavalehForooshSigns, HavalehForooshApprove, ExitsSigns, Exits


def qr_template_view(request, ID):
    url = request.path
    url = url.split("/")[2]
    parsed_url = url.split("_")
    data = {}
    if parsed_url[0] == "1":
        inbox = Inbox.objects.get(id=parsed_url[1])
        data["subject"] = "امضا با مشخصات زیر مورد تایید است"
        data["body"] = """
        <h2>%s</h2>
        <h3>موضوع نامه %s</h3>
        <div>
        لینک نامه : 
        <a href='%s'>مرور نامه</a>
        
        </div>
        """ % (
            "امضا با مشخصات زیر مورد تایید است",
            inbox.letter['subject'],
            request.environ['wsgi.url_scheme'] + "://" + request.META[
                'HTTP_HOST'] + "/#!/dashboard/Letter/Inbox/" + str(inbox.id) + "/Preview",

        )

    if parsed_url[0] == "3":
        hfs = HavalehForooshSigns.objects.get(id=parsed_url[1])
        appr = HavalehForooshApprove.objects.get(id=hfs.HavalehForooshApproveLink)
        positionDoc = PositionsDocument.objects.filter(positionID=hfs.positionID).order_by("-id").first()
        data["subject"] = "امضا با مشخصات زیر مورد تایید است"
        data["body"] = """
        <h2>%s</h2>
        <div>
        صاحب امضا : 
        %s
        -
        تاریخ امضا : 
        %s
        </div>
        <h3>موضوع  %s</h3>
        <div>
        لینک حواله فروش : 
        <a href='%s'>مرور حواله فروش</a>

        </div>
        """ % (
            "امضا با مشخصات زیر مورد تایید است",
            positionDoc.profileName,
            mil_to_sh(hfs.dateOfPost),
            "حواله فروش ",
            request.environ['wsgi.url_scheme'] + "://" + request.META[
                'HTTP_HOST'] + "/SpecialApps/#!/home/Sales/hf/" + str(appr.havalehForooshLink) + "/details",
        )
    if parsed_url[0] == "2":
        hfs = ExitsSigns.objects.get(id=parsed_url[1])
        positionDoc = PositionsDocument.objects.filter(positionID=hfs.positionID).order_by("-id").first()
        data["subject"] = "امضا با مشخصات زیر مورد تایید است"
        data["body"] = """
        <h2>%s</h2>
        <div>
        صاحب امضا : 
        %s
        -
        تاریخ امضا : 
        %s
        </div>
        <h3>موضوع  %s</h3>
        <div>
        لینک حواله خروج : 
        <a href='%s'>مرور حواله خروج</a>

        </div>
        """ % (
            "امضا با مشخصات زیر مورد تایید است",
            positionDoc.profileName,
            mil_to_sh(hfs.dateOfPost),
            "حواله خروج ",
            request.environ['wsgi.url_scheme'] + "://" + request.META[
                'HTTP_HOST'] + "/SpecialApps/#!/home/Sales/kh/" + str(hfs.exitsLink.id) + "/details",
        )

    return render_to_response('qr/index.html', data, context_instance=RequestContext(request))
