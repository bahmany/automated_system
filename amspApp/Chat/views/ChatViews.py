import mongoengine
from asq.initiators import query
from django.core.cache import cache
from django.utils import timezone
from django.views.generic import TemplateView
from mongoengine import Q
from rest_framework.decorators import list_route, detail_route
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from ws4redis.subscriber import RedisSubscriber

from amspApp.Chat.models import Chat, MutedPositions
from amspApp.Chat.serializers.ChatSerializer import ChatSerializer
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import FilterCompanyID, MongoSearchFilter
from amspApp._Share.ListPagination import DetailsPagination, PaginateRequest
from amspApp.amspUser.models import MyUser
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset

__author__ = 'mohammad'


class ChatViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = ChatSerializer
    queryset = Chat.objects.all().order_by('-dateOfPost').order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol,)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("body",)

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID
        return super(ChatViewSet, self).initial(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        result = super(ChatViewSet, self).create(request, *args, **kwargs)

        username = MyUser.objects.get(
            id=PositionsDocument.objects.filter(positionID=result.data['dest_positionID'])[0].userID
        )

        # dd = RedisSubscriber
        redis_publisher = RedisPublisher(facility='foobar', users=[username.username])
        # message = RedisMessage(result.data["body"])
        message = RedisMessage("1")
        redis_publisher.publish_message(message)

        # welcome = RedisMessage()  # create a welcome message to be sent to everybody
        # RedisPublisher(facility='foobar', users=[username.username]).publish_message(welcome)
        # RedisPublisher(facility='foobar', broadcast=True).publish_message(welcome)

        return result

    @list_route(methods=["GET"])
    def getUnreadChatsCount(self, request, *args, **kwargs):
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        unreadCounts = Chat.objects.filter(
            dest_positionID=posiIns.positionID,
            seen=False,
            positionID__nin=
            [
                x.mutedPositionID for x in MutedPositions.objects.filter(positionID=posiIns.positionID)
                ]

        ).count()
        return Response(dict(unreadCounts=unreadCounts, msg="ok"))

        """
        db.positions_document.aggregate([
        {$match:{"companyID":700,"userID":{$nin:[null]} }},
              {
                    $lookup :
                            {
                                from:'chat',
                                localField:'positionID',
                                foreignField:'positionID',
                                as:'chatsDetails'
                            }
               }
            ,
               {
                    $unwind:
                        {
                            path:'$chat',
                            preserveNullAndEmptyArrays: true
                         }
               }
             ,

               {
                   $project:{
                       avatar:1,
                       chartName:1,
                       profileName:1,
                       countUnSeen:1,
                       userID:1,
                       positionID:'$positionID',
                       latestChat:{$max:'$chatsDetails.dateOfPost'},



                       unseen:{$size:{
                           $filter:{
                               input:'$chatsDetails',
                               as:'unseen',
                               cond:{$eq:['$$unseen.seen', false]}
                               }}}




                       }
                   },
                   {$sort:{"latestChat": -1}}
                   ])

        """

    @list_route(methods=['GET'])
    def getRelatedChatters(self, request, *args, **kwargs):
        return Response({})
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        # positions = PositionsDocument.objects.filter(
        #     companyID=posiIns.companyID
        #     , userID__nin=[None]
        # ).skip(0).limit(20).values_list(
        #     'positionID', 'chartName',
        #     'profileName', 'avatar')

        # paginating counts
        pagination = PaginateRequest().paginate(request)

        filterStr = ""
        if "q" in request.query_params:
            if request.query_params["q"] != "undefined":
                filterStr = ', "profileName":{$regex : ".*' + request.query_params["q"] + '.*"}'

        pipline = """
        db.positions_document.aggregate([
        {$match:{
            "companyID":%s,
            "userID":{$nin:[null]}
            %s
             }},
              {
                    $lookup :
                            {
                                from:'chat',
                                localField:'positionID',
                                foreignField:'positionID',
                                as:'chatsDetails'
                            }
               }
            ,
               {
                    $unwind:
                        {
                            path:'$chat',
                            preserveNullAndEmptyArrays: true
                         }
               }
             ,
               {
                   $project:{
                       _id:0,
                       avatar:1,
                       chartName:1,
                       profileName:1,
                       countUnSeen:1,
                       userID:1,
                       positionID:'$positionID',
                       latestChat:{$max:'$chatsDetails.dateOfPost'},
                       unseen:{$size:{
                           $filter:{
                               input:'$chatsDetails',
                               as:'unseen',
                               cond:{ $and:[{$eq:['$$unseen.seen', false]},{$eq:['$$unseen.dest_positionID', %s]}] }
                               }}}
                       }
                   },
                   {$sort:{"latestChat": -1}},
                    { $limit: %s },
                    { $skip: %s }
                   ])
        """ % (posiIns.companyID, filterStr, posiIns.positionID, pagination['limit'], pagination['skip'])

        result = PositionsDocument.objects._collection_obj.database.eval(pipline)["_batch"]

        # paginating result

        for r in result:
            r['thisisyou'] = r["positionID"] == posiIns.positionID
        # poss = []
        # for p in positions:
        #     poss.append(dict(
        #         positionID=p[0],
        #         chartName=p[1],
        #         profileName=p[2],
        #         avatar=p[3],
        #     ))

        result.reverse()
        result = dict(results=result, )
        result.update(pagination)
        index = 0
        for r in result["results"]:
            index += 1
            r["rowID"] = index

            r["online"] = "dis"
            if cache.get('%s_lazy' % (r["userID"])):
                r["online"] = "lazy"
            if cache.get('%s_active' % (r["userID"])):
                r["online"] = "active"
            if cache.get('%s_idle' % (r["userID"])):
                r["online"] = "idle"

        return Response(result)

    @detail_route(methods=['GET'])
    def getSingleChat(self, request, *args, **kwargs):
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        Chat.objects.filter(positionID=kwargs['id'], dest_positionID=posiIns.positionID, seen=False).update(
            seen=True,
            dateOfSeen=timezone.now()
        )
        chats = Chat.objects.filter(
            Q(positionID=posiIns.positionID, dest_positionID=kwargs['id']) |
            Q(positionID=kwargs['id'], dest_positionID=posiIns.positionID)
        ).skip(0).limit(20).order_by('-id')
        lst1 = list(chats.distinct('positionID'))
        lst2 = list(chats.distinct('dest_positionID'))
        lst = lst1 + lst2
        lst = query(lst).distinct().to_list()

        positionDocs = PositionsDocument.objects.filter(positionID__in=lst, userID__nin=[None])

        p = []
        for po in positionDocs:
            p.append(dict(
                positionID=po.positionID,
                avatar=po.avatar
            ))

        chatsSerial = ChatSerializer(instance=chats, many=True).data
        # getting profiles
        # Chat.objects.filter(positionID=posiIns.positionID)


        for c in chatsSerial:
            # poss = Profile.objects.filter(positionID = c["positionID"])[0]
            q = query(p).where(lambda x: x['positionID'] == c["positionID"]).to_list()[0]
            c["positionAvatar"] = q["avatar"]
            c.pop('companyID')
            c.pop('chatType')
            c.pop('dest_groupID')
            c.pop('dest_pageID')
            c.pop('is_deleted')
            c["thisisyou"] = c["positionID"] == posiIns.positionID

        return Response(dict(msg="ok", results=chatsSerial[::-1]))

    @detail_route(methods=['GET'])
    def updateChats(self, request, *args, **kwargs):
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        Chat.objects.filter(positionID=kwargs['id'], dest_positionID=posiIns.positionID, seen=False).update(
            seen=True,
            dateOfSeen=timezone.now()
        )
        chats = Chat.objects.filter(
            (Q(positionID=posiIns.positionID, dest_positionID=kwargs['id']) |
            Q(positionID=kwargs['id'], dest_positionID=posiIns.positionID)) &
            Q(id__gt = request.query_params['li'])

        ).skip(0).limit(20).order_by('-id')
        lst1 = list(chats.distinct('positionID'))
        lst2 = list(chats.distinct('dest_positionID'))
        lst = lst1 + lst2
        lst = query(lst).distinct().to_list()

        positionDocs = PositionsDocument.objects.filter(positionID__in=lst, userID__nin=[None])

        p = []
        for po in positionDocs:
            p.append(dict(
                positionID=po.positionID,
                avatar=po.avatar
            ))

        chatsSerial = ChatSerializer(instance=chats, many=True).data
        # getting profiles
        # Chat.objects.filter(positionID=posiIns.positionID)


        for c in chatsSerial:
            # poss = Profile.objects.filter(positionID = c["positionID"])[0]
            q = query(p).where(lambda x: x['positionID'] == c["positionID"]).to_list()[0]
            c["positionAvatar"] = q["avatar"]
            c.pop('companyID')
            c.pop('chatType')
            c.pop('dest_groupID')
            c.pop('dest_pageID')
            c.pop('is_deleted')
            c["thisisyou"] = c["positionID"] == posiIns.positionID

        return Response(dict(msg="ok", results=chatsSerial[::-1]))
