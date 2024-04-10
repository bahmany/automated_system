from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets as me_viewsets

from amspApp.CompaniesManagment.DMSManagement.models import DMS, docModel, docZone, docFormat, docRelated, docType
from amspApp.CompaniesManagment.DMSManagement.serializers.DMSManagementSerializer import DMSManagementSerializer, \
    InboxDMSManagementSerializer, InboxUserDMSSerializer
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp.FileServer.models import File
from amspApp._Share.ListPagination import DetailsPagination


class DMSManagementViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = DMS.objects.all()
    serializer_class = DMSManagementSerializer
    pagination_class = DetailsPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)
    permission_name = "Can_edit_documents"
    permission_classes = (CanCruid,)

    def get_permissions(self):
        return get_permissions(self, DMSManagementViewSet)


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new = serializer.create(serializer.validated_data, request=request)

            return Response({}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors,
                         'status': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = instance.id
        self.perform_update(serializer)
        return Response(serializer.data)

    @list_route(methods=['GET'])
    def InboxList(self, request, *args, **kwargs):
        # posId = PositionsDocument.objects.get(userID=request.user.current_company.id)
        queryset = DMS.objects.filter(companyId=request.user.current_company.id).order_by('-postDate')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = InboxDMSManagementSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = InboxDMSManagementSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET'])
    def DMSListForUser(self, request, *args, **kwargs):
        # posId = PositionsDocument.objects.get(userID=request.user.current_company.id)
        queryset = DMS.objects.filter(companyId=request.user.current_company.id, visible=True).order_by('-docCode')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = InboxUserDMSSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = InboxUserDMSSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET'])
    def getDMSSettings(self, request, *args, **kwargs):
        posId = PositionsDocument.objects.get(userID=request.user.current_company.id,
                                              companyID=request.user.current_company.id)
        querdocModel = docModel.objects.filter(companyId=request.user.current_company.id)
        if querdocModel.count() <= 0:
            sampleDocModel = ['FO', 'BR']
            for itm in sampleDocModel:
                new = docModel(name=itm, position_id=posId.id, companyId=request.user.current_company.id)
                new.save()
            querdocModel = docModel.objects.filter(companyId=request.user.current_company.id)
        querdocZone = docZone.objects.filter(companyId=request.user.current_company.id)
        if querdocZone.count() <= 0:
            sampleDocZone = ['مستندات عمومی - PB',
                             'منابع انسانی - HR',
                             'سیستم ها و روش ها - MS',
                             'فنی و مهندسی - TC',
                             'فروش و بازاریابی - SA',
                             'خرید - PR',
                             'مالی - FI',
                             'نگهداری و تعمیرات - NT',
                             'کنترل کیفیت - QC',
                             'برنامه ریزی تولید و تولید - TO',
                             'سایر- OT',

                             ]
            for itm in sampleDocZone:
                new = docZone(name=itm, position_id=posId.id, companyId=request.user.current_company.id)
                new.save()
            querdocZone = docZone.objects.filter(companyId=request.user.current_company.id)
        querdocFormat = docFormat.objects.filter(companyId=request.user.current_company.id)
        if querdocFormat.count() <= 0:
            sampleDocFormat = ['A4', 'A3', 'A5']
            for itm in sampleDocFormat:
                new = docFormat(name=itm, position_id=posId.id, companyId=request.user.current_company.id)
                new.save()
            querdocFormat = docFormat.objects.filter(companyId=request.user.current_company.id)
        querdocRelated = docRelated.objects.filter(companyId=request.user.current_company.id)
        if querdocRelated.count() <= 0:
            sampleDocRelated = ['انبار',
                                'پشتیبانی تولید',
                                'حراست',
                                'کلیه فرآیندها',
                                'منابع انسانی']
            for itm in sampleDocRelated:
                new = docRelated(name=itm, position_id=posId.id, companyId=request.user.current_company.id)
                new.save()
            querdocRelated = docRelated.objects.filter(companyId=request.user.current_company.id)
        querdocType = docType.objects.filter(companyId=request.user.current_company.id)
        if querdocType.count() <= 0:
            sampleDocType = ['فرم', 'دستور عمل']
            for itm in sampleDocType:
                new = docType(name=itm, position_id=posId.id, companyId=request.user.current_company.id)
                new.save()
            querdocType = docType.objects.filter(companyId=request.user.current_company.id)

        res = {
            'docCode': [],
            'docType': [],
            'docZone': [],
            'docFormat': [],
            'docRelated': [],
            'docModel': []
        }
        for itm in querdocModel:
            res['docModel'].append({'id': str(itm.id), 'name': itm.name})
        for itm in querdocZone:
            res['docZone'].append({'id': str(itm.id), 'name': itm.name})
        for itm in querdocFormat:
            res['docFormat'].append({'id': str(itm.id), 'name': itm.name})
        for itm in querdocRelated:
            res['docRelated'].append({'id': str(itm.id), 'name': itm.name})
        for itm in querdocType:
            res['docType'].append({'id': str(itm.id), 'name': itm.name})

        return Response(res)

    @detail_route(methods=['GET'])
    def fileDet(self, request, *args, **kwargs):
        fileId = kwargs['id']
        fileObj = File.objects.get(decodedFileName=fileId)
        data = {
            'dir': fileObj.decodedFileName,
            'name': fileObj.originalFileName,
            'date': fileObj.dateOfPost,
            'size': fileObj.uploaderIP['fileSize'],
            'isCurr': 0
        }
        return Response(data)

    def template_page_base(self, request, *args, **kwargs):
        return render_to_response('companyManagement/BaseDMS.html', {},
                                  context_instance=RequestContext(request))

    def template_page_new(self, request, *args, **kwargs):
        return render_to_response('companyManagement/NewDMS.html', {},
                                  context_instance=RequestContext(request))

    def template_page_edit(self, request, *args, **kwargs):
        return render_to_response('companyManagement/EditDMS.html', {},
                                  context_instance=RequestContext(request))

    def template_page_list(self, request, *args, **kwargs):
        return render_to_response('DMS/DMSlist.html', {},
                                  context_instance=RequestContext(request))

    def dmsBase(self, request, *args, **kwargs):
        return render_to_response('DMS/baseIframe.html', {},
                                  context_instance=RequestContext(request))
