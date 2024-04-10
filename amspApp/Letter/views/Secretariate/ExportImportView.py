from datetime import datetime

from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer, \
    SecretariatSerializerPermission
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time
from amspApp.Letter.models import Inbox, Letter, SecTagItems
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp.Letter.serializers.LetterSerializer import LetterSerializer
from amspApp.Letter.serializers.SecTagsSerializer import SecTagItemSerializer
from amspApp._Share.ListPagination import DetailsPagination


class ExportImportViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = LetterSerializer
    queryset = Letter.objects.all()

    @list_route(methods=["post"])
    def resend(self, request, *args, **kwargs):
        request.data['selectedLetter']['letter']['id'] = request.data['selectedLetter']['id']
        letterInstance = Letter.objects.get(id=Inbox.objects.get(id=request.data['selectedLetter']['inboxId']).letter['id'])
        recs = request.data["persons"]

        for r in recs:
            r["desc"] = None

        exp = letterInstance.exp
        if "hameshRecievers" in exp["export"]:
            exp["export"]["hameshRecievers"] = exp["export"]["hameshRecievers"] + request.data["persons"]
        else:
            exp["export"]["hameshRecievers"] = request.data["persons"]
        letterSerial = LetterSerializer(instance=letterInstance, data={"exp": exp}, partial=True)
        letterSerial.is_valid(raise_exception=True)

        letterSerial.save()

        if len(recs) > 0:
            letterInstance.recievers = recs
            firstInbox = InboxSerializer().SaveToSentFolder(letterInstance)
            InboxSerializer().SendLetter(
                letterInstance=letterInstance,
                prevSenderInboxID=firstInbox.id,
                itemMode=1,
                itemType=10)

        return Response({'result':'ok'})

    # creatorPositionID
    # letterType
    # secretariatID
    def create(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        posDoc = PositionsDocument.objects.get(positionID=pos.id,
                                               companyID=self.request.user.current_company.id)
        request.data["creatorPositionID"] = pos.id
        request.data["creatorPosition"] = posDoc._data
        request.data["creatorPosition"]["id"] = str(request.data["creatorPosition"]["id"])
        secInstance = SecretariatsViewSet().GetDefaultSecretariatInstanceByPositionInstance(pos)
        request.data["secretariatID"] = secInstance.secretariat.id
        request.data["secretariat"] = SecretariatSerializer(instance=secInstance.secretariat).data
        request.data["secretariatPermissionID"] = secInstance.id
        request.data["secretariatPermission"] = SecretariatSerializerPermission(instance=secInstance).data

        # cheking cover page and adding it to letter body
        body = ""
        body = "<p>این نامه صادره توسط %s در دبیرخانه %s مورخه %s ثبت شده است</p>" % (
            request.data["creatorPosition"]["profileName"] + " - " + request.data["creatorPosition"]["chartName"],
            request.data['secretariat']['name'],
            mil_to_sh_with_time(datetime.now()))
        body += """<div><img src='%s' style='width:400px'></div><div><a onclick='downloadURL("%s")'>دانلود کاور</a></div>""" % (
            request.data['exp']['cover'], request.data['exp']['cover'])
        if "attachments" in request.data:
            if len(request.data["attachments"]):
                body += "<p>ضمائم نامه</p>"
                attsAddr = ""
                for at in request.data["attachments"]:
                    attsAddr += """
                    <div  class="pull-left well well-sm clearfix text-center ng-scope" style="width: 100px; height:  padding: 3px; margin: 3px; overflow: hidden;">
<span class="content_right_head ng-binding">%s</span>
<br>
<img style="max-width: 50px; max-height: 55px" src="%s">
<br>
<small class="ng-binding">
   %skb
</small><br>
<div class="btn-group btn-group-xs">
    <a class="btn btn-default btn-xs fa fa-arrow-circle-down" style="cursor:pointer;" tooltip=" دانلود" onclick="downloadURL('%s');"></a>
</div></div> """ % (
                        at["imgInf"]["name"],
                        at["imgLink"],
                        int(int(at["imgInf"]["size"]) / 1024),
                        "/api/v1/file/upload?q=" + at["imgInf"]["orgname"]
                    )
                body += attsAddr

        request.data["body"] = body

        request.data["letterType"] = 3

        result = super(ExportImportViewSet, self).create(request, *args, **kwargs)
        SecTagItems.objects.filter(letterID=result.data["id"]).delete()
        for tag in request.data["tags"]:
            dt = {
                "tag": tag["id"],
                "letterID": result.data["id"],
                "positionID": pos.id
            }
            tagSerial = SecTagItemSerializer(data=dt)
            tagSerial.is_valid(raise_exception=True)
            tagSerial.save()

        return result

    @detail_route(methods=["get"])
    def get_prev(self, request, *args, **kwargs):
        inboxInstance = Inbox.objects.get(
            id=request.query_params["id"])
        result = InboxSerializer(instance=inboxInstance)
        result = result.data
        if 'sign' in result['letter']:
            if 'generatedFileAddr' in result['letter']['sign']:
                result['letter']['sign']['generatedFileAddr'] = \
                    result['letter']['sign']['generatedFileAddr'].split("/")[
                        len(result['letter']['sign']['generatedFileAddr'].split("/")) - 1]
                result['letter']['sign']['generatedFileAddr'] = "/api/v1/file/upload?q=" + result['letter']['sign'][
                    'generatedFileAddr']

        # getting tags
        st = SecTagItems.objects.filter(letterID=result["letter"]["id"])
        resTags = []
        for s in st:
            resTags.append(
                {
                    "name": s.tag.name,
                    "id": str(s.id)
                }
            )
        result["tags"] = resTags
        result['letter']['body'] = result['letter']['body'].replace("&nbsp;", " ")
        return Response(result)
