from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import Q
from rest_framework.decorators import list_route
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp.MyProfile.models import Profile
from amspApp.QC.models import Finding, QCDocuments
from amspApp.QC.serializers.FindingSerializer import FindingSerializer
from amspApp.Sales.permissions.basePermissions import CanCruidSale
from amspApp._Share.ListPagination import DetailsPagination
from amspApp._Share.pdfPositionHandling import pdfPositionHandling
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class QCFindingViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = FindingSerializer
    queryset = Finding.objects.all().order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol, CanCruidSale)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("desc__Sharh",)

    # def readPDF(self, pdfFile):
    #     rsrcmgr = PDFResourceManager()
    #     retstr = StringIO()
    #     codec = 'utf-8'
    #     laparams = LAParams()
    #     device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    #
    #     interpreter = PDFPageInterpreter(rsrcmgr, device)
    #     password = ""
    #     maxpages = 0
    #     caching = True
    #     pagenos = set()
    #     for page in PDFPage.get_pages(pdfFile, pagenos, maxpages=maxpages, password=password, caching=caching,
    #                                   check_extractable=True):
    #         interpreter.process_page(page)
    #
    #     device.close()
    #     textstr = retstr.getvalue()
    #     retstr.close()
    #     return textstr

    @list_route(methods=["POST"])
    def parsPdf(self, request, *args, **kwargs):
        # return
        request.data["type"] = 1
        request.data["title"] = "Air Ops Easy Access Rules_Rev.08_March 2017 (Recovered 1).pdf"
        request.data["fileAddr"] = "D:/AO.pdf"
        qcDoc = QCDocuments(**request.data)
        qcDoc.save()
        pdf = pdfPositionHandling().parsepdf(qcDoc, request.data["fileAddr"], 0, 9999)
        pdfPositionHandling().getBookmarks(qcDoc, request.data["fileAddr"])

        return Response({})

    def get_queryset(self):
        # getting current position
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
        companyID = posInstance.companyID
        posID = posInstance.positionID

        self.queryset = self.queryset.filter(
            Q(currentPerformerPositionID=posInstance.positionID) |
            Q(followUpPosID=posInstance.positionID) |
            Q(positionID=posInstance.positionID)
        )

        return super(QCFindingViewSet, self).get_queryset()

    @list_route(methods=["POST"])
    def sendFinding(self, request, *args, **kwargs):
        dt = request.data
        positionInstance = PositionsDocument.objects.get(
            id=dt["recPositionID"]
        )
        findingInstance = Finding.objects.get(id=dt["findingID"])
        posDoc = PositionDocumentSerializer(instance=positionInstance).data
        # updating findingInstance
        performers = findingInstance.performers
        if not ("recievers" in performers):
            performers["recievers"] = []
        performers["recievers"].append({
            "position": posDoc,
            "dateOfSend": datetime.now(),
            "typeOf": dt["typeOf"]
        })
        rootCause = {}
        rootCause["position"] = posDoc
        rootCause["form"] = {}
        rootCause["files"] = {}
        rootCause["form"]["cause"] = ""
        rootCause["form"]["cap"] = ""
        fpositionInstance = PositionsDocument.objects.get(
            id=findingInstance.followUpPosID
        )
        fposDoc = PositionDocumentSerializer(instance=fpositionInstance).data
        followUp = {}
        followUp["position"] = fposDoc
        followUp["form"] = {}
        followUp["files"] = {}
        followUp["reason"] = ""

        findingSerial = self.serializer_class(
            instance=findingInstance,
            data={
                "type": dt["typeOf"],
                "currentPerformerPositionID": positionInstance.positionID,
                "performers": performers,
                "rootCause": rootCause,
                "followUp": followUp
            },
            partial=True
        )
        findingSerial.is_valid(raise_exception=True)
        findingSerial.save()

        return Response({"msg": "ok", "f": findingSerial.data})

    def retrieve(self, request, *args, **kwargs):
        result = super(QCFindingViewSet, self).retrieve(request, *args, **kwargs)

        posIns = PositionsDocument.objects.filter(
            positionID=result.data["positionID"],
            companyID=result.data["companyID"],
        )

        posIns = posIns[0]

        result.data["creatorAvatar"] = posIns.avatar
        result.data["creatorName"] = posIns.profileName
        result.data["creatorSemat"] = posIns.chartName

        return result

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID
            if "desc" in request.data:
                if "dateOf" in request.data["desc"]:
                    request.data["desc"]["dateOf"] = sh_to_mil(request.data["desc"]["dateOf"])

            if "dueDateStart" in request.data:
                request.data["dueDateStart"] = datetime.strptime(sh_to_mil(request.data["dueDateStart"]), "%Y/%m/%d")
            if "dueDateEnd" in request.data:
                request.data["dueDateEnd"] = datetime.strptime(sh_to_mil(request.data["dueDateEnd"]), "%Y/%m/%d")

        return super(QCFindingViewSet, self).initial(request, *args, **kwargs)

    def template_view_read(self, request):
        return render_to_response('QC/Finding/base.html', {}, context_instance=RequestContext(request))

    def template_view_open(self, request):
        return render_to_response('QC/Finding/openFinding.html', {}, context_instance=RequestContext(request))

    def template_view_post_read(self, request):
        return render_to_response('QC/Finding/post.html', {}, context_instance=RequestContext(request))

    def template_view_list_read(self, request):
        return render_to_response('QC/Finding/list.html', {}, context_instance=RequestContext(request))

    def template_qcmanual(self, request):
        return render_to_response('QC/Manual/base.html', {}, context_instance=RequestContext(request))

    def list(self, request, *args, **kwargs):
        result = super(QCFindingViewSet, self).list(request, *args, **kwargs)
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
        for d in result.data["results"]:
            positionDoc = PositionsDocument.objects.filter(
                positionID=d["positionID"],
                companyID=request.user.current_company_id,
            )
            d["isEditable"] = d["positionID"] == posInstance.positionID
            if d["positionID"] == posInstance.positionID:
                d["isEditable"] = not (bool(d["currentPerformerPositionID"]))

            if positionDoc.count() != 0:
                positionDoc = positionDoc[0]
                profileInstance = Profile.objects.get(userID=positionDoc.userID)
                d["positionName"] = positionDoc.profileName
                d["positionSemat"] = positionDoc.chartName
                d["avatar"] = profileInstance.extra["profileAvatar"]["url"]
            else:
                d["positionName"] = "حذف شده"
                d["positionSemat"] = "حذف شده"
                d["avatar"] = "/static/images/avatar_empty.jpg"
        return result
