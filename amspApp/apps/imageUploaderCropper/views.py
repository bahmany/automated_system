from django.shortcuts import render_to_response
from django.template import RequestContext

from amspApp.CompaniesManagment.CompanyProfile.models import CompanyProfile
from amspApp.CompaniesManagment.CompanyProfile.serializers.CompanyProfileSerializers import CompanyProfileSerializer


def home(request):
    # getting current company instance
    # if not request.user.is_active:
    #     return redirect("/login")
    if not request.user.is_active:
        return render_to_response('authentication/logins/returnToLogin.html', {},
                                  context_instance=RequestContext(request))

    companyInstance = CompanyProfile.objects.get(companyID=request.user.current_company_id)
    companySerial = CompanyProfileSerializer(instance=companyInstance).data
    msg = companySerial["extra"]["biefIntroduction"]

    return render_to_response('apps/ImageUploaderCropper/base.html', {'msg': msg}, context_instance=RequestContext(request))