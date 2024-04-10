import io
import xml.etree.ElementTree as ET

from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import Q
from rest_framework import status
from rest_framework.decorators import list_route, detail_route
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets as me_viewsets

from amspApp.BPMSystem.MyEngine.Validator import Validator
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp.CompaniesManagment.Processes.validators.BPMNValidator import BPMNValidator
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp._Share.ListPagination import DetailsPagination


class BpmnViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Bpmn.objects.all().order_by('-id')
    serializer_class = BpmnSerializer
    pagination_class = DetailsPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)
    permission_name = "Can_edit_BPMS"
    permission_classes = (CanCruid,)

    # def get_permissions(self):
    #     return get_permissions(self, BpmnViewSet)



    def get_queryset(self):

        currentCompanyInstance = Company.objects.get(id=self.kwargs["companyID_id"])
        self.queryset = self.queryset.filter(company_id=currentCompanyInstance.id)

        if "q" in self.request.query_params:
            if self.request.query_params["q"] != "":
                if self.request.query_params["q"] != "undefined":
                    self.queryset = self.queryset.filter(Q(name__icontains=self.request.query_params["q"]) |
                                                         Q(description__icontains=self.request.query_params["q"]))

        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        result = super(BpmnViewSet, self).retrieve(self, request, *args, **kwargs)
        if "form" in result.data:
            if result.data["form"]:
                for r in result.data["form"]:
                    if "schema" in r:
                        if "fields" in r["schema"]:
                            for field in r["schema"]["fields"]:
                                if "type" in field:
                                    field["type"] = field["type"].replace("amf", "mrb")
        bpmnInstance = self.get_object()
        res = result.data["form"]

        bpmnInstance.update(set__form = res)
        return result

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by('-postDate').exclude('form',
                                                                    'processObjs',
                                                                    'publishedUsers',
                                                                    'publishedUsersDetail',
                                                                    'userTasks',
                                                                    'xml')
        result = super(BpmnViewSet, self).list(request, *args, **kwargs)
        return result

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            bpmn = serializer.validated_data['xml']
            bpmn = ET.parse(io.StringIO(bpmn))
            validator = Validator(bpmn)
            if (len(validator.validate_diagram()) == 0):
                serializer.validated_data['is_valid_form'] = True
            else:
                serializer.validated_data['is_valid_form'] = False

            serializer.create(serializer.validated_data, request=request)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'message': serializer.errors,
            'status': 'Bad request',
        }, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['patch'])
    def UpdateCallActivity(self, request, *args, **kwargs):
        instance = self.get_object()
        bindingMap = request.data['bindingMap']
        stepId = request.data['stepId']
        instance.bindingMap[str(stepId)] = {'bpmnSelected': request.data['bpmnSelected'], 'fields': bindingMap}
        instance.save()
        return Response(instance.bindingMap)

    @detail_route(methods=['patch'])
    def PublishBpmn(self, request, *args, **kwargs):
        instance = self.get_object()
        publishedUsers = request.data['publishedUsers']
        publishedUsersDetail = request.data['publishedUsersDetail']
        instance.publishedUsers = publishedUsers
        instance.publishedUsersDetail = publishedUsersDetail
        instance.save()
        return Response({})

    @detail_route(methods=['get'])
    def validateBpmn(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.userTasks:
            instance.userTasks = []
            instance.save()
        validatoreObj = BPMNValidator(instance.xml, instance.form, instance.userTasks)
        errorList = validatoreObj.validate()
        return Response(errorList)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        bpmn = serializer.validated_data['xml']
        bpmn = ET.parse(io.StringIO(bpmn))
        validator = Validator(bpmn)
        if (len(validator.validate_diagram()) == 0):
            serializer.validated_data['is_valid_form'] = True
        else:
            serializer.validated_data['is_valid_form'] = False

        self.perform_update(serializer)
        return Response(serializer.data)

    def template_view_new(self, request, *args, **kwargs):

        return render_to_response('companyManagement/BPMN/newbpmn.html', {},
                                  context_instance=RequestContext(self.request))

    def template_view_setup(self, request, *args, **kwargs):

        return render_to_response('companyManagement/BPMN/designer/SetupBpmnElements.html', {},
                                  context_instance=RequestContext(self.request))

    def template_view_publish(self, request, *args, **kwargs):

        return render_to_response('companyManagement/BPMN/PublishBpmn.html', {},
                                  context_instance=RequestContext(self.request))

    def template_view_validate(self, request, *args, **kwargs):

        return render_to_response('companyManagement/BPMN/validateBpmn.html', {},
                                  context_instance=RequestContext(self.request))

    def template_view(self, request, *args, **kwargs):
        gt_datas_title = [
            'name',
            'description',
        ]

        gt_datas_dbtitle = [
            'name',
            'description',
        ]

        gt_buttons = [
            {'type': 'danger fa fa-trash', 'func': 'bpmnDelete(obj.id)', 'is_toggle_func': 's', 'is_toggle': 0,
             'tooltip': 'خذف فرایند'},
            {'type': 'primary fa fa-file-text', 'type2': ' disabled fa fa-lock', 'is_toggle_func': 'is_valid_form',
             'func': 'buildForm(obj.id)', 'title': '',
             'is_toggle': 1, 'tooltip': 'طراحی فرم ها'},
            {'type': 'warning fa fa-check', 'type2': ' disabled fa fa-lock', 'is_toggle_func': 'is_valid_form',
             'func': 'bpmnPublish(obj.id)', 'is_toggle': 1, 'tooltip': 'انتشار فرایند'},

            {'type': 'primary fa fa-edit', 'func': 'bpmnEdit(obj.id)', 'is_toggle_func': 's', 'is_toggle': 0,
             'tooltip': 'ویرایش فرایند'},
            {'type': 'warning fa fa-files-o', 'func': 'bpmnCopy(obj.id)', 'is_toggle_func': 's', 'is_toggle': 0,
             'tooltip': 'کپی فرایند'},
            {'type': 'success fa fa-magic', 'func': 'bpmnValidate(obj.id)', 'is_toggle_func': 's', 'is_toggle': 0,
             'tooltip': 'صحت سنجی'},

        ]

        gm_aresure_buttons = [
            {'type': 'success fa fa-check', 'func': 'yes()', 'title': ''},
            {'type': 'danger fa fa-times', 'func': 'no()', 'title': ''},
        ]

        # gt_ means GenericTable
        # gm_ means GenericModal

        data = {'gm_items': [
            {
                'gm_modal_title': 'areyuosure',
                'gm_modal_id': 'GenericModalAreYouSure.html',
                'gm_form': 'areusure',
                'gm_buttons': gm_aresure_buttons},
            {
                'gm_modal_title': 'forbiden',
                'gm_modal_id': 'GenericModalPermissionDenied.html',
                'gm_form': 'permissiondenied',
                'gm_buttons': [{'type': 'success fa fa-check', 'func': 'ok()', 'title': ''}]}],
            'gt_table_title': 'bpmnlist',
            'gt_object_name': 'bpmn',
            'gt_func_col': 'tbl-process-btns',
            'gt_search_func': 'searchBpmn()',
            'gt_create_func': 'createBpmn()',
            'gt_datas_title': gt_datas_title,
            'gt_datas_dbtitle': gt_datas_dbtitle,
            'gt_buttons': gt_buttons,
            'bpmn_table_template': 'generic-templates/Table.html',
            'bpmn_edit_modal': 'generic-templates/Modal.html',
        }

        return render_to_response('companyManagement/BPMN/BpmnsTable.html', data,
                                  context_instance=RequestContext(self.request))

    @list_route(methods=["POST"])
    def CopyBpmn(self, request, **kwargs):
        data = request.data
        oldbpmn = Bpmn.objects.get(id=data['bpmnId'])
        if Bpmn.objects.filter(user_id=oldbpmn['user_id'], company_id=oldbpmn["company_id"],
                               name=data['value']).count() > 0:
            return Response({
                'message': 'erorr',
                'status': 'Bad request',
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            newBpmn = Bpmn(
                user_id=request.user.id,
                company_id=request.user.current_company.id,
                name=data['value'],
                description=oldbpmn.description,
                xml=oldbpmn.xml,
                form=oldbpmn.form,
                processObjs=oldbpmn.processObjs,
                userTasks=oldbpmn.userTasks,
                storage=oldbpmn.storage,
                bindingMap=oldbpmn.bindingMap,
                is_valid_form=oldbpmn.is_valid_form,
                publishedUsers=oldbpmn.publishedUsers,
                publishedUsersDetail=oldbpmn.publishedUsersDetail)
            newBpmn.save()
            return Response(str(newBpmn.id))

    @list_route(methods=["GET"])
    def listForStart(self, request, *args, **kwargs):
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)
        # queryset = self.filter_queryset(self.get_queryset())
        self.queryset = self.queryset.filter(publishedUsers__contains=str(posistionObj.id)).order_by('-id')

        return self.list(request, *args, **kwargs)

    @list_route(methods=["GET"])
    def listForEdit(self, request, *args, **kwargs):

        # queryset = self.filter_queryset(self.get_queryset())
        # self.queryset = self.queryset.filter(publishedUsers__contains=str(posistionObj.id)).order_by('-id')

        return self.list(request, *args, **kwargs)
