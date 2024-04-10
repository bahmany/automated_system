from html.parser import HTMLParser

from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Letter.models import Inbox, Letter
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class InboxSocialViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = InboxSerializer
    queryset = Inbox.objects.all()

    """
    [{
        $match: {
            "currentPositionID": 710
        }
    },
    {
        $group: {
            _id: "$sender.positionID",
            count: { $sum: 1 },
            desc: { $last: "$sender" }
        }
    }
        ,
    {
        $sort: { "count": -1 }
    }]
    """

    @list_route(methods=["GET"])
    def get_users(self, request, *args, **kwargs):
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        defaultSecratriat = SecretariatsViewSet().GetDefaultSecretariatInstance(request)

        senders = Inbox.objects.aggregate(
            {"$match": {"currentPositionID": posiIns.positionID, }},
            {
                "$project": {
                    "sender": 1,
                    "currentPositionID": 1,
                    "seen": 1,
                    "itemMode": 1,
                    "itemPlace": 1,
                    "dateOfObservable": 1,
                    "letter.id": 1,
                }
            },
            {"$group": {
                "_id": "$sender.positionID",
                "count": {"$sum": 1},
                "dateOfObservable": {"$last": "$dateOfObservable"},
                "desc": {"$last": "$sender"},
                "inboxID": {"$last": "$_id"},
                "unseenCount": {"$sum": {"$cond": [{"$and": [
                    {"$eq": ["$seen", False]},
                    {"$eq": ["$itemMode", 1]},
                    {"$eq": ["$itemPlace", 1]},
                ]}, 1, 0]}}
            }},
            {"$sort": {"unseenCount": -1, "dateOfObservable": -1}})
        senders = list(senders)
        for s in senders:
            s["prevLetter"] = self.get_prev_summ(posiIns, s.get("inboxID"))

        return Response(senders)

    @detail_route(methods=["GET"])
    def get_prev_summ(self, positionInstance, inboxID):
        inbox = Inbox.objects.get(
            id=inboxID,
            currentPositionID=positionInstance.positionID,
        )
        letterInstance = Letter.objects.get(id=inbox.letter.get("id"))
        letterSumm = letterInstance.body
        letterSumm = strip_tags(letterSumm)
        letterSumm = letterSumm[0:50]
        return letterSumm

    @detail_route(methods=["GET"])
    def get_msg_list(self, request, *args, **kwargs):
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        inbox = Inbox._get_collection()
        pipline = """
        db.inbox.aggregate([
           
                {"$match":{
                    "itemMode":1, 
                    "itemPlace":1,
                    "currentPositionID":%d,
                    "sender.positionID":%d
                    }}
                ,
                {"$project": {
                "_id": 1,
                "sender.positionID":1,
                "currentPositionID":1,
                "letter.id":1
                }},
                {"$limit": 10},
                {"$skip": 0},
                {"$sort":{"_id": -1}}
                ])
        """ % (posiIns.positionID, int(kwargs.get("id")), )
        res = inbox.database.eval(pipline)["_batch"]

        # inbox.aggregate([
        #     {'$lookup': {
        #         "from": 'letter',
        #         "localField": 'letter.id',
        #         "foreignField": 'id',
        #         "as": 'letterDetails'
        #     }},
        #     {"$match": {
        #         "currentPositionID": posiIns.positionID,
        #         "sender.positionID": int(kwargs.get("id"))
        #     }},
        #     {"$project": {
        #         "_id": 1,
        #         "letterDetails": 1
        #     }},
        #     {"$limit": 10},
        #     {"$skip": 0}], cursor={})

        # queryset = Inbox.objects.filter(currentPositionID=posiIns.positionID,
        #                                 sender__positionID=int(kwargs.get("id"))).aggregate(
        #     {"$project": {"_id": 1}},
        #     {"$limit": 10},
        #     {"$skip": 0},
        #
        # )
        result = list(res)
        # result = self.list(request, *args, **kwargs)
        return Response(result)

    @detail_route(methods=["GET"])
    def get_msg_prev(self, request, *args, **kwargs):
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        inbox = Inbox.objects.get(
            id=kwargs.get("id"),
            currentPositionID=posiIns.positionID,
        )
        inbox.update(set__seen=True)
        letterInstance = Letter.objects.get(id=inbox.letter.get("id"))
        letterInstance._data["sign"]["letter"] = None  # maxinum recursion caused
        result = {
            "inbox": InboxSerializer(instance=inbox).data,
            "letter": letterInstance._data
        }

        return Response(result)

    def template_view(self, request, *args, **kwargs):
        return render_to_response(
            "letter/Preview/messages.html",
            {},
            context_instance=RequestContext(request)
        )
