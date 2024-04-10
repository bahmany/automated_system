from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.QC.models import QCDocumentsDetails, QCDocuments, QCDocumentsOulines
from amspApp.templatetags.translators import translate, translateToEn


class QCViewSet(viewsets.ModelViewSet):
    @list_route(methods=["GET"])
    def searchref(self, request):
        if "q" in request.query_params:
            if request.query_params["q"] != "":
                if request.query_params["q"] != "undefined":
                    if len(request.query_params["q"]) < 3:
                        return Response([])
                    en = translateToEn(request.query_params["q"])
                    odc = QCDocumentsDetails.objects._collection.aggregate([
                        {'$match': {"$text": {"$search": en}}},
                        {"$group": {"_id": "$pageIndex", "count": {"$sum": 1}}},
                        {"$sort": {"count": -1}},
                        {"$limit": 30}
                    ])["result"]

                    # for o in odc:

                    for o in odc:
                        f = QCDocumentsDetails.objects._collection.find_one(dict(pageIndex=o.get("_id") - 1))
                        d = QCDocuments.objects._collection.find_one(dict(_id=f.get("QCDocumentLink")))
                        s = list(QCDocumentsOulines.objects._collection.find(
                            dict(QCDocumentLink=f.get("QCDocumentLink"), page=o.get("_id"))))

                        o["img"] = f.get("fileAddr")
                        o["word"] = f.get("word")
                        o["img"] = f.get("fileAddr")
                        o["manualName"] = d.get("title").split(".")[0]
                        o["outlines"] = [{"title": x["title"], "desc": x["desc"]} for x in s]

                    return Response(odc)
        return Response([])

    def template_view_read(self, request):
        return render_to_response('QC/base.html', {}, context_instance=RequestContext(request))
