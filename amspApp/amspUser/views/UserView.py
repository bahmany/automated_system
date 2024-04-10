import math
# import secrets
import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import viewsets, permissions, views
from rest_framework.decorators import list_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response

from amspApp.Administrator.Customers.models import UserCustomer, Billing_Customer
from amspApp.Administrator.Customers.views.CustomerRegistrationView import CustomerRegistrationViewSet
from amspApp.CompaniesManagment.models import Company
from amspApp.MyProfile.models import Profile
from amspApp.Virtual.Registration.forms.loginForm import RegisterationHireForm
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.amspUser.forms.loginForm import LoginForm
from amspApp.amspUser.models import MyUser, BasicAuths
from amspApp.amspUser.permissions.UserPermissions import IsAccountOwner
from amspApp.amspUser.serializers.UserSerializer import UserSerializer, BasicAuthsSerializer
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


# import secrets


class UserListPagination(PageNumberPagination):
    page_size = 14
    page_size_query_param = 'page_size'
    max_page_size = 50


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = DetailsPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner())

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        query = self.request.GET.get('query')
        item_per_page = self.request.GET.get('itemPerPage')

        if item_per_page and not item_per_page == 'undefined':
            self.pagination_class.page_size = item_per_page

        if query and not query == 'undefined':
            search_text = self.request.GET['query']
            queryset = MyUser.objects.filter(Q(username__contains=search_text) |
                                             Q(email__contains=search_text) |
                                             Q(first_name__contains=search_text) |
                                             Q(last_name__contains=search_text) & Q(is_deleted=False))
        else:
            queryset = MyUser.objects.filter(is_deleted=False)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        request.user.current_company = Company.objects.get(id=request.data["current_company"])
        request.user.save()
        return Response({'id': request.user.current_company.id, 'name': request.user.current_company.name},
                        status.HTTP_200_OK)

    @list_route(methods=['get'])
    def GetUserInfo(self, request):

        currentPosition = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        res = {}
        res['profileName'] = currentPosition.profileName
        res['chartName'] = currentPosition.chartName
        res['avatar'] = currentPosition.avatar
        return Response(res)

    @list_route(methods=["get"])
    def GetProfileLevel(self, request):
        level = 0
        if request.user.is_active:
            profileInstance = Profile.objects.get(userID=request.user.id)
            # complete name , family , title , profile pic
            # level = 20
            if "Name" in profileInstance.extra:
                if profileInstance.extra["Name"] != "":
                    level += 10
            if "Title" in profileInstance.extra:
                if profileInstance.extra["Title"] != "":
                    level += 10
            if "job" in profileInstance.extra:
                if "Doreh" in profileInstance.extra["job"]:
                    level += 10 if len(profileInstance.extra["job"]["Doreh"].keys()) > 0 else 0

                if "Education" in profileInstance.extra["job"]:
                    level += 10 if len(profileInstance.extra["job"]["Education"].keys()) > 0 else 0

                if "Experience" in profileInstance.extra["job"]:
                    level += 10 if len(profileInstance.extra["job"]["Experience"].keys()) > 0 else 0

                if "Job" in profileInstance.extra["job"]:
                    level += 10 if len(profileInstance.extra["job"]["Job"].keys()) > 0 else 0

                if "Language" in profileInstance.extra["job"]:
                    level += 10 if len(profileInstance.extra["job"]["Language"].keys()) > 0 else 0

                if "Resume" in profileInstance.extra["job"]:
                    level += 10 if len(profileInstance.extra["job"]["Resume"].keys()) > 0 else 0

                if "Shenasnameh" in profileInstance.extra["job"]:
                    level += 10 if len(profileInstance.extra["job"]["Shenasnameh"].keys()) > 0 else 0

                if "Software" in profileInstance.extra["job"]:
                    level += 10 if len(profileInstance.extra["job"]["Software"].keys()) > 0 else 0

                if "Resume" in profileInstance.extra["job"]:
                    level += 10 if len(profileInstance.extra["job"]["Resume"].keys()) > 0 else 0
            return Response({"rank": int((level / 11) * 10)})
        return Response({"rank": -1})

    def checkUserSignPass(self, userInstance, Password):
        return check_password(Password, userInstance.sign_password)

    def template_view(self, request, *args, **kwargs):
        gt_datas_title = [
            'id',
            'username'
            'email',
            'active',
            'staff',
            'superuser',
            'lastlogin ',
        ]

        gt_datas_dbtitle = [
            'id',
            'username',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            "last_login | jalaliDateFromNow:'jYYYY-jMM-jDD hh:mm:ss' ",
        ]

        gt_buttons = [
            {'type': 'primary fa fa-edit', 'func': 'userEdit(obj.username)', 'is_toggle_func': 's', 'is_toggle': 0},
            {'type': 'info fa fa-key', 'func': 'passEdit(obj.username)', 'is_toggle_func': 's', 'is_toggle': 0},
            {'type': 'warning fa fa-lock', 'type2': 'success fa fa-unlock', 'is_toggle_func': 'is_active',
             'func': 'userPassive(obj.username)', 'title': 'passive',
             'is_toggle': 1},
            {'type': 'danger fa fa-trash', 'func': 'userDelete(obj.username)', 'is_toggle_func': 's', 'is_toggle': 0}

        ]

        gm_user_buttons = [
            {'type': 'success fa fa-save', 'func': 'saveUserEdit()', 'title': ''},
            {'type': 'danger fa fa-times', 'func': 'cancel()', 'title': ''},
        ]

        gm_pass_buttons = [
            {'type': 'success fa fa-save', 'func': 'savePassEdit()', 'title': ''},
            {'type': 'danger fa fa-times', 'func': 'cancel()', 'title': ''},
        ]

        gm_aresure_buttons = [
            {'type': 'success fa fa-check', 'func': 'yes()', 'title': ''},
            {'type': 'danger fa fa-times', 'func': 'no()', 'title': ''},
        ]

        serializer = self.get_serializer()
        renderer = HTMLFormRenderer()
        gm_user_form = renderer.render(serializer.data, renderer_context={
            'template': 'forms/amsp-user/EditUsernameEmail.html',
            'request': self.request
        })

        gm_pass_form = renderer.render(serializer.data, renderer_context={
            'template': 'forms/amsp-user/EditPass.html',
            'request': self.request
        })

        # gt_ means GenericTable
        # gm_ means GenericModal

        data = {'gm_items': [{
            'gm_modal_title': 'edituser',
            'gm_modal_id': 'GenericModalUserEdit.html',
            'gm_form': gm_user_form,
            'gm_buttons': gm_user_buttons},
            {
                'gm_modal_title': 'editpass',
                'gm_modal_id': 'GenericModalPassEdit.html',
                'gm_form': gm_pass_form,
                'gm_buttons': gm_pass_buttons},
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
            'gt_table_title': 'userlist',
            'gt_object_name': 'user',
            'gt_func_col': 'col-md-2',
            'gt_search_func': 'searchUsers()',
            'gt_datas_title': gt_datas_title,
            'gt_datas_dbtitle': gt_datas_dbtitle,
            'gt_buttons': gt_buttons,
            'user_table_template': 'ani-theme/generic-templates/Table.html',
            'user_edit_modal': 'ani-theme/generic-templates/Modal.html',
        }

        return render_to_response('ani-theme/views/pages/dashboard/../../../templates/amsp-user/UsersTable.html', data,
                                  context_instance=RequestContext(self.request))


class LoginView(views.APIView):

    def id_generator(self):
        try:
            import secrets
            id = secrets.token_urlsafe(math.floor(32 / 1.3))
        except:
            id = uuid.uuid4().hex[:6].upper() + uuid.uuid4().hex[:6].upper() + uuid.uuid4().hex[
                                                                               :6].upper() + uuid.uuid4().hex[
                                                                                             :6].upper() + uuid.uuid4().hex[
                                                                                                           :6].upper()

        id = id.replace('-', '').replace('!', '').replace('?', '').replace(' ', '').replace(':', '').replace('&', '')
        return id

    def GenerateBasicAuth(self, user, request):
        # print('---------------------BasicAuths.objects.filter-------------------')
        # print('---------------------BasicAuths.objects.filter-------------------')
        # print('---------------------BasicAuths.objects.filter-------------------')
        # print('---------------------BasicAuths.objects.filter-------------------')
        # print('---------------------BasicAuths.objects.filter-------------------')
        # print('---------------------BasicAuths.objects.filter-------------------')
        # print('---------------------BasicAuths.objects.filter-------------------')
        # print('---------------------BasicAuths.objects.filter-------------------')
        # print('---------------------BasicAuths.objects.filter-------------------')
        # print('---------------------BasicAuths.objects.filter-------------------')
        bb = BasicAuths.objects.filter(
            userID=user.id,
            deviceType=request.stream.META['HTTP_USER_AGENT']
        )
        """
        برای اینکه بیش از ۱۰ سیشن باز نداشته باشیم
        """
        if bb.count() > 15:
            delc = bb.count() - 15
            # BasicAuths.objects.filter(userID=user.id,
            #                           deviceType=request.stream.META['HTTP_USER_AGENT']).order_by('dateOfPost').limit(
            #     delc).delete()
        dt = dict(
            token=self.id_generator() + self.id_generator(),
            deviceType=request.stream.META['HTTP_USER_AGENT'],
            userID=user.id
        )

        ser = BasicAuthsSerializer(data=dt)
        ser.is_valid(raise_exception=True)
        ser.save()
        return ser.data

    @csrf_exempt
    def post(self, request, format=None):

        # checking captch after login fail
        if not request.session.get("loginAttempts"):
            request.session["loginAttempts"] = 0
        if request.session["loginAttempts"] > 0:
            frm = LoginForm(request.POST)
            if len(request.POST) == 0:
                frm = LoginForm(request.data)
            if not frm.is_valid():
                request.session["loginAttempts"] = 1 + request.session["loginAttempts"]
                return Response({
                    'status': 'Captcha',
                    'message': 'حروف نوشته شده داخل تصویر را اصلاح نمایید'
                }, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        remember = data.get('remember', True)
        if username[0:2] == "09":
            username = "+989" + username
            username = username.replace("+98909", "+989")
        if username[0:2] == "98":
            username = "+989" + username
            username = username.replace("+98998", "+989")
        if username[0:1] == "9":
            username = "+989" + username
            username = username.replace("+9899", "+989")
        username.replace("+", "")
        # frm = LoginForm(request.POST).visible_fields() if "username" in request.data: userInstance =
        # MyUser.objects.filter(username = request.data["username"]) if userInstance.count() != 1 : return Response({
        #  'status': 'Unauthorized', 'message': 'این نام کاربری توسط مدیر سیستم غیر فعال شده است - لطفا با مدیر سیستم
        #  تماس بگیرید' }, status=status.HTTP_401_UNAUTHORIZED) userInstance = userInstance[0] profileInstance =
        # Profile.objects.get(userID = userInstance.id) if "isAllowed" in profileInstance.extra : if not
        # profileInstance.extra["isAllowed"]: return Response({ 'status': 'Unauthorized', 'message': 'کاربر محترم شما
        #  هنوز در سیستم توسط کارشناس منابع انسانی تایید نشده اید - لطفا منتظر تایید کارشناس بمانید - با تشکر' },
        # status=status.HTTP_401_UNAUTHORIZED)

        username = username.replace("+", "")

        user = authenticate(username=username, password=password)
        if user == None:
            user = authenticate(username=username.replace("989", "09"), password=password)
        if user == None:
            user = authenticate(username=username.replace("+989", "09"), password=password)
        if user == None:
            user = authenticate(username=username.replace("989", "+989"), password=password)
        if user == None:
            if username[0:3] == "989":
                user = authenticate(username=username.replace("989", "+989"), password=password)
        if user == None:
            user = authenticate(username=username.replace("+989", "09"), password=password)
        if user == None:
            if username[0:3] == "989":
                user = authenticate(username="09" + username[3:], password=password)

        if user is not None:
            if user.is_active:

                basicAuth = self.GenerateBasicAuth(user, request)
                request.session['basicAuth'] = basicAuth
                # request.basicAuth = basicAuth
                request.user = user
                cutomerID = CustomerRegistrationViewSet().GetCustomerIDFromBilling(request)
                userID = user.id
                isInSubDomain = UserCustomer.objects.filter(userID=userID, customerID=cutomerID).count()
                if isInSubDomain == 0:
                    return Response({
                        'status': 'Unauthorized',
                        'message': 'کاربر گرامی شما مجاز به استفاده از این دومین نیستید - لطفا با دومین مخصوص خود '
                                   'وارد شوید '
                    }, status=status.HTTP_401_UNAUTHORIZED)

                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(7 * 24 * 60 * 60)
                serialized = UserSerializer(user)

                return Response({"u": user.account_type})
                # return redirect('/')
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'این نام کاربری توسط مدیر سیستم غیر فعال شده است - لطفا با مدیر سیستم تماس بگیرید'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:

            request.session["loginAttempts"] = 1 + request.session["loginAttempts"]
            # request.session["loginTry"] = datetime.now()

            return Response({
                'status': 'Unauthorized',
                'message': 'نام کاربری یا رمز عبور صحیح نیست'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LoginViewset(viewsets.ViewSet):
    @csrf_exempt
    def getTemplate(self, request):
        if not "loginAttempts" in request.session:
            request.session["loginAttempts"] = 0

        if request.user.is_active:
            logout(request)

        loginPageName = "login.html"
        if request.subdomain != None:
            if request.subdomain.defaultLoginPage != None:
                loginPageName = request.subdomain.defaultLoginPage

        if request.subdomain == None:
            loginPageName = "domainNotFound.html"

        userCount = MyUser.objects.all().count()
        domainCount = Billing_Customer.objects.all().count()

        return render(request, 'authentication/logins/' + "base_" + loginPageName, {
            'form': LoginForm(None),
            "userCount": userCount,
            "domainCount": domainCount,
            'regForm': RegisterationHireForm(None)
        }, context_instance=RequestContext(request))


class ResetPassView(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'password_reset'
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    def create(self, request, *args, **kwargs):
        key = request.data["hashed"]

        if not request.data["newPass"] == request.data["ConfnewPass"]:
            return Response({
                'status': 'Unauthorized',
                'message': 'Password is not matched'
            }, status=status.HTTP_400_BAD_REQUEST)
        if len(request.data["newPass"]) < 4:
            return Response({
                'status': 'Unauthorized',
                'message': 'Password is too short it must be more than 4 chars'
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(key) != 96:
            return Response({
                'status': 'Unauthorized',
                'message': 'Invalid Key'
            }, status=status.HTTP_400_BAD_REQUEST)

        userInstance = MyUser.objects.filter(password_reset=key)

        if userInstance.count() != 1:
            return Response({
                'status': 'Unauthorized',
                'message': 'User not found !!'
            }, status=status.HTTP_400_BAD_REQUEST)

        userInstance = userInstance[0]
        userInstance.set_password(request.data["newPass"])
        userInstance.password_reset = ""
        userInstance.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        return render_to_response('authentication/resetpass.html', {},
                                  context_instance=RequestContext(request))
