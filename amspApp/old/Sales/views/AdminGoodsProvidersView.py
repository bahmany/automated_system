from random import randint

from mongoengine import Q
from amspApp.Infrustructures.odoo_connector.connectors import OdooConnector
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amsp import settings
from amspApp.Dashboards.Supply.models import GoodsProviders
from amspApp.Dashboards.Supply.serialization.GoodsSupplaySerializer import GoodsProvidersSerializer, \
    SupplementCategoriesSerializer
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time
from amspApp._Share.ListPagination import ListPagination, DataTablesPagination
from amspApp.amspUser.models import MyUser


class AdminTaminDakheliViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = GoodsProviders.objects.all().order_by("-id")
    serializer_class = GoodsProvidersSerializer
    pagination_class = ListPagination

    def retrieve(self, request, *args, **kwargs):
        result = super(AdminTaminDakheliViewSet, self).retrieve(request, *args, **kwargs)
        userInstance = MyUser.objects.get(id=result.data["extra"]["userID"])
        result.data["reg_type"] = userInstance.account_type

        if result.data["reg_type"] == 4:
            result.data['reg_type_str'] = "فروشنده"
        if result.data["reg_type"] == 5:
            result.data['reg_type_str'] = "خدمات دهنده"
        if result.data["reg_type"] == 6:
            result.data['reg_type_str'] = "سازنده"

        if result.data["reg_type"] == 4:
            result.data["reg_type"] = 0
        if result.data["reg_type"] == 5:
            result.data["reg_type"] = 1
        if result.data["reg_type"] == 6:
            result.data["reg_type"] = 2

        if result.data.get("extra"):
            if result.data.get("extra").get("frm1"):
                if result.data.get("extra").get("frm1").get("name"):
                    result.data["name"] = result.data.get("extra").get("frm1").get("name")
            if result.data.get("extra").get("frm2"):
                if result.data.get("extra").get("frm2").get("name"):
                    result.data["name"] = result.data.get("extra").get("frm2").get("name")
            if result.data.get("extra").get("frm3"):
                if result.data.get("extra").get("frm3").get("name"):
                    result.data["name"] = result.data.get("extra").get("frm3").get("name")
        return result

    @list_route(methods=["GET"])
    def getForDataTables(self, request, *args, **kwargs):
        if request.user.groups.filter(name='foroosh').count() == 0:
            return Response({})
        self.pagination_class = DataTablesPagination
        # get users
        searchStr = request.query_params.get("sSearch")
        if searchStr:
            if searchStr != "":
                users = [x["id"] for x in list(MyUser.objects.filter(username__contains=searchStr).values("id"))]
                q_users = [Q(extra__userID=x) for x in users]
                query = Q()
                if len(q_users) != 0:
                    query = q_users.pop()
                for item in q_users:
                    query |= item
                query |= Q(extra__frm1__name__contains=searchStr)
                query |= Q(extra__frm2__name__contains=searchStr)
                query |= Q(extra__frm3__name__contains=searchStr)
                query |= Q(extra__gen_code__contains=searchStr)
                query |= Q(extra__type_of_provider__contains=searchStr)
                self.queryset = self.queryset.filter(query)

        result = self.list(request, args, kwargs)
        for r in result.data["aaData"]:
            if r["extra"].get("gen_code") is None:
                r["extra"]["gen_code"] = "NULL"
            if r.get("extra").get("step2") is None:
                r["extra"]["step2"] = {}
            if r["extra"]["step2"].get("name") is None:
                r["extra"]["step2"]["name"] = "NULL"
            if r["extra"].get("type_of_provider") is None:
                r["extra"]["type_of_provider"] = "NULL"
                """
                    1 = automation
                    2 = First Try
                    4 = supplier seller
                    5 = supplier service
                    6 = supplier factory
                    7 = hire
                
                """
            if r['extra'].get("userID"):
                userInstance = MyUser.objects.get(id=r['extra']['userID'])
                r['extra']['type_of_provider'] = ""
                if userInstance.account_type == 4:
                    r['extra']['type_of_provider'] = "فروشنده"
                if userInstance.account_type == 5:
                    r['extra']['type_of_provider'] = "خدمات دهنده"
                if userInstance.account_type == 6:
                    r['extra']['type_of_provider'] = "سازنده"

            r["extra"]["name"] = ""
            if r.get("extra"):
                if r.get("extra").get("frm1"):
                    if r.get("extra").get("frm1").get("name"):
                        r["extra"]["name"] = r.get("extra").get("frm1").get("name")
                if r.get("extra").get("frm2"):
                    if r.get("extra").get("frm2").get("name"):
                        r["extra"]["name"] = r.get("extra").get("frm2").get("name")
                if r.get("extra").get("frm3"):
                    if r.get("extra").get("frm3").get("name"):
                        r["extra"]["name"] = r.get("extra").get("frm3").get("name")

            r["dateOfPost"] = mil_to_sh_with_time(r["dateOfPost"])

            ff = MyUser.objects.filter(id=r.get("extra").get("userID")).first()
            r["extra"]["username"] = ""
            if ff:
                r["extra"]["username"] = ff.username
        return result

    def checkPerm(self, req):
        if req.user.groups.filter(name__contains="foroosh").count() == 0:
            raise Exception("مجوز دسترسی ندارید")


    def list(self, request, *args, **kwargs):
        self.checkPerm(request)
        return super(AdminTaminDakheliViewSet, self).list(request, *args, **kwargs)

    @list_route(methods=["POST"])
    def genOdooContact(self, request, *args, **kwargs):
        self.checkPerm(request)

        odoo = OdooConnector(endpoint=settings.ODOO_HTTP_REFERER,
                             dbname='odooDB',
                             username='bahmanymb@gmail.com',
                             password='****')
        uid = odoo.connect()
        result = odoo.search(uid=uid,
                             model='res.partner',
                             action='search',
                             queries=[[['name', '=', "tttttttt"]]],
                             parameters={'limit': 5}
                             )

        # odoo = OdooConnector(endpoint=ODOO_Platform,
        #                      dbname='odoodb',
        #                      username='bahmanymb@gmail.com',
        #                      password='****')
        # data = [{
        #     "name":"tttttttt",
        #     "street":"fdgdfsg dsfg",
        # }]
        #
        # result = odoo.write(uid=uid, model='res.partner', action='create', data=

        pass

    @list_route(methods=["GET"])
    def createSuppCats(self, request, *args, **kwargs):
        self.checkPerm(request)

        return Response({})
        p1 = {'code': -1, "name": "تجهیزات و قطعات مکانیکی "}
        p2 = {'code': -1, "name": "تجهیزات و قطعات برقی "}
        p3 = {'code': -1, "name": "قطعات عمومی صنعتی و ابزار آلات "}
        p4 = {'code': -1, "name": "لوازم و قطعات تاسیسات "}
        p5 = {'code': -1, "name": "مصالح، مواد شیمیایی و اقلام مصرفی "}
        p6 = {'code': -1, "name": "ملزومات اداری و اقلام عمومی "}
        p7 = {'code': -1, "name": "اقلام ایمنی و بهداشت "}
        p8 = {'code': -1, "name": "خدمات "}

        ins1 = SupplementCategoriesSerializer(data=p1)
        ins2 = SupplementCategoriesSerializer(data=p2)
        ins3 = SupplementCategoriesSerializer(data=p3)
        ins4 = SupplementCategoriesSerializer(data=p4)
        ins5 = SupplementCategoriesSerializer(data=p5)
        ins6 = SupplementCategoriesSerializer(data=p6)
        ins7 = SupplementCategoriesSerializer(data=p7)
        ins8 = SupplementCategoriesSerializer(data=p8)

        ins1.is_valid(raise_exception=True)
        ins2.is_valid(raise_exception=True)
        ins3.is_valid(raise_exception=True)
        ins4.is_valid(raise_exception=True)
        ins5.is_valid(raise_exception=True)
        ins6.is_valid(raise_exception=True)
        ins7.is_valid(raise_exception=True)
        ins8.is_valid(raise_exception=True)

        ins1 = ins1.save()
        ins2 = ins2.save()
        ins3 = ins3.save()
        ins4 = ins4.save()
        ins5 = ins5.save()
        ins6 = ins6.save()
        ins7 = ins7.save()
        ins8 = ins8.save()

        csss = [{'code': 110,
                 'name': 'تجهیزات و قطعات هیدرولیکی، پنوماتیک، اکچویتورها، رگلاتورها، تنظیم­کننده­ها، واحد مراقبت و قطعات',
                 'parent': ins1.id},
                {'code': 111, 'name': 'بیرینگ­ها و کنس­ها ،کاسه نمد، پولی، یاتاقان ، اورینگ، انواع پولی، گریس­خور',
                 'parent': ins1.id},
                {'code': 112, 'name': 'محفظه­ها و سیلندرهای تحت فشار ', 'parent': ins1.id},
                {'code': 113, 'name': 'تجهیزات، سیستم­ها و یونیت­های روانکاری و متعلقات   ', 'parent': ins1.id},
                {'code': 114, 'name': 'لوازم و قطعات یدکی خودرو', 'parent': ins1.id},
                {'code': 115, 'name': 'لوازم موتور (دیزلی  و بنزین)', 'parent': ins1.id},
                {'code': 116, 'name': 'فنر، پران', 'parent': ins1.id},
                {'code': 117, 'name': 'فیلترها، لوازم ومتعلقات', 'parent': ins1.id},
                {'code': 118, 'name': 'رینگ، تیوپ، تایر', 'parent': ins1.id},
                {'code': 119, 'name': 'لیفتراک، لوازم موتوری خاص ویدکی', 'parent': ins1.id},
                {'code': 120, 'name': 'لنت و دیسک وصفحه ومتعلقات  (صنعتی)', 'parent': ins1.id},
                {'code': 121, 'name': 'اتصالات ( پیچ ، مهره، واشر، رولپلاک)', 'parent': ins1.id},
                {'code': 122, 'name': 'شافت­های فلزی و غیرفلزی', 'parent': ins1.id},
                {'code': 123, 'name': 'گسکت و واشرلاستیکی', 'parent': ins1.id},
                {'code': 124, 'name': 'پین، اشپیل، خار،کلید', 'parent': ins1.id},
                {'code': 125, 'name': 'شیلنگ­ها، سرشیلنگ (هیدرولیک ، پنوماتیک ) ', 'parent': ins1.id},
                {'code': 126, 'name': 'قطعات پلیمری', 'parent': ins1.id},
                {'code': 127, 'name': 'متعلقات پرس های هیدرولیکی و ضربه ای', 'parent': ins1.id},
                {'code': 128, 'name': 'تسمه ( V-Belt ، Timing Belt )وتسمه های قابل آپارات', 'parent': ins1.id},
                {'code': 129, 'name': 'قطعات انتقال قدرت (چرخ دنده ، چرخ زنجیر ، کوپلینگ دنده ای،زنجیر،گاردان ها) ',
                 'parent': ins1.id},
                {'code': 130, 'name': 'کوپلینگ ­ ها (صلب،فلاکسیبل و هیدرولیکی) ', 'parent': ins1.id},
                {'code': 131, 'name': ' قط عات استاندارد خط چاپ(دستگاه (Mailander ', 'parent': ins1.id},
                {'code': 132, 'name': 'اجزای استاندارد کوره LTG ', 'parent': ins1.id},
                {'code': 133, 'name': 'ماشین­افزار، فرز، تراش، برش، سنگ (محور،مغناطیسی) و متعلقات ', 'parent': ins1.id},
                {'code': 134, 'name': 'کرپی ، بست، شگل،سیم بگسل،بلت،زنجیر،قلاب', 'parent': ins1.id},
                {'code': 135, 'name': 'جرثقیل ­ های سقفی (جیم بلاک) و متعلقات ', 'parent': ins1.id},
                {'code': 136, 'name': 'قطعات ریخته گری وآهنگری', 'parent': ins1.id},
                {'code': 137, 'name': 'متعلقات قالب (سنبه،واش،تیغه،ماتریس )', 'parent': ins1.id},
                {'code': 210, 'name': 'موتورهای الکتریکی و ژنراتورهای AC    DC, ', 'parent': ins2.id},
                {'code': 211, 'name': 'سیستم های اتوماسیون PLC وقطعات جانبی', 'parent': ins2.id},
                {'code': 212, 'name': 'تجهیزات مکانیکی ریلی ', 'parent': ins2.id},
                {'code': 213, 'name': 'فیوزها', 'parent': ins2.id},
                {'code': 214, 'name': 'محافظ الکتریکی( کنترل فاز )', 'parent': ins2.id},
                {'code': 216, 'name': 'سیستم­های جمع کننده کابل،ترمزهای برقی و قطعات مربوطه', 'parent': ins2.id},
                {'code': 217, 'name': 'تجهیزات سیستم های توزین،لودسل ها و قطعات جانبی ', 'parent': ins2.id},
                {'code': 218, 'name': 'لوازم روشنایی', 'parent': ins2.id},
                {'code': 219, 'name': 'سروموتور،انکدر', 'parent': ins2.id},
                {'code': 220, 'name': 'ترموکوپل ها،المنت ', 'parent': ins2.id},
                {'code': 221, 'name': 'بوش باتوم ها، Emergency ', 'parent': ins2.id},
                {'code': 222, 'name': 'تایمرها و متعلقات', 'parent': ins2.id},
                {'code': 223, 'name': 'قطعات مدارهای فرمان و قدرت ( خازن ، مقاومت ، دیود و ...)', 'parent': ins2.id},
                {'code': 224, 'name': 'زغال ­ های صنعتی', 'parent': ins2.id},
                {'code': 225, 'name': 'سیم وکابل – وایر وسرسیم', 'parent': ins2.id},
                {'code': 226, 'name': 'بوبین ­ ها', 'parent': ins2.id},
                {'code': 227, 'name': 'سنسورها', 'parent': ins2.id},
                {'code': 228, 'name': 'ترانس ­ ها', 'parent': ins2.id},
                {'code': 229, 'name': 'انواع cpu ،انواع کارت ', 'parent': ins2.id},
                {'code': 230, 'name': 'تجهیزات وکابل­های فرمان', 'parent': ins2.id},
                {'code': 231, 'name': 'منبع تغذیه', 'parent': ins2.id},
                {'code': 232, 'name': 'انواع بورد­های الکترونیکی وپنل­های­کنترلی', 'parent': ins2.id},
                {'code': 233, 'name': 'کنتاکتور، رله ها ', 'parent': ins2.id},
                {'code': 234, 'name': 'تاسیسات الکتریکی ساختمان', 'parent': ins2.id},
                {'code': 235, 'name': 'باکس­ها (جعبه شاسی  وتقسیم وجعبه، سنسور )', 'parent': ins2.id},
                {'code': 236, 'name': 'تجهیزات اعلام حریق', 'parent': ins2.id},
                {'code': 237, 'name': 'شین ­ ها', 'parent': ins2.id},
                {'code': 238,
                 'name': 'سکسیونرها، دژنگتورها، تجهیزات پست ­ های برق، کلیدهای فشارقوی، برق ­ گیرها، مقره ­ ها، بوشینگ ­ ها و عایق ­ ها ',
                 'parent': ins2.id},
                {'code': 310, 'name': 'یراق­آلات', 'parent': ins3.id},
                {'code': 311, 'name': 'تجهیزات اندازه گیری (کولیس،عمق سنج، میکرومترو.....) و متعلقات آن­ها ',
                 'parent': ins3.id},
                {'code': 312, 'name': ' سنگ، دریل، مینی سنگ و ...', 'parent': ins3.id},
                {'code': 313, 'name': 'متعلقات ودستگاه­های بادی( ابزارآلات پنوماتیکی)', 'parent': ins3.id},
                {'code': 314, 'name': 'تجهیزات اندازه­گیری الکتریکی(آمپرمتر، ولت متر و .. ) و متعلقات آن­ها ',
                 'parent': ins3.id},
                {'code': 315, 'name': 'ابزارآلات براده­برداری (انواع **** ها و تیغچه ) ', 'parent': ins3.id},
                {'code': 316, 'name': 'ابزارآلات عمومی ', 'parent': ins3.id},
                {'code': 317, 'name': 'تسمه­کش', 'parent': ins3.id},
                {'code': 318, 'name': 'لوله خم­کن', 'parent': ins3.id},
                {'code': 319, 'name': 'لوله بر', 'parent': ins3.id},
                {'code': 320, 'name': 'پولی ­ کش', 'parent': ins3.id},
                {'code': 321, 'name': 'تجهیزات توزین وترازو', 'parent': ins3.id},
                {'code': 322, 'name': 'تجهیزات عمومی آزمایشگاه', 'parent': ins3.id},
                {'code': 323, 'name': 'منگنه­کوب، میخ­کوب بسته­بندی', 'parent': ins3.id},
                {'code': 324, 'name': 'وسایل و تجهیزات اندازه­گیری حجمی ( بشر، بالن ژوژه و ...)', 'parent': ins3.id},
                {'code': 325, 'name': 'وسایل و تجهیزات اندازه­گیری الکتریکی ( ولت متر، مولتی متر، آمپرمتر و ... )',
                 'parent': ins3.id},
                {'code': 326, 'name': 'دستگاه­های جوش، برش و متعلقات آن­ها ', 'parent': ins3.id},
                {'code': 327, 'name': 'الکترودها، سیم جوش،سیم لحیم و مواد جانبی ', 'parent': ins3.id},
                {'code': 410, 'name': 'لوله­ها (صنعتی و عمومی) ', 'parent': ins4.id},
                {'code': 411, 'name': 'سیل، درزبند و عایق ها، کاسه نمد، پکینگ و... ', 'parent': ins4.id},
                {'code': 412, 'name': 'کمپرسورها و متعلقات', 'parent': ins4.id},
                {'code': 413, 'name': 'اتصالات انبساطی ', 'parent': ins4.id},
                {'code': 414, 'name': 'پمپ ها و متعلقات آنها ', 'parent': ins4.id},
                {'code': 415, 'name': 'مبدل­های حرارتی، تیوب باندل و متعلقات ', 'parent': ins4.id},
                {'code': 416, 'name': 'تجهیزات حرارتی (مشعل ، رادیانت، تیوپ ) ', 'parent': ins4.id},
                {'code': 417, 'name': 'سیستم­های هواساز، فن­ها و بلوئرها ', 'parent': ins4.id},
                {'code': 418, 'name': 'انواع اتصالات', 'parent': ins4.id},
                {'code': 419, 'name': 'انواع شیرهای صنعتی ', 'parent': ins4.id},
                {'code': 420, 'name': 'شعله پخش کن، نازل، سرنازل، مشعل', 'parent': ins4.id},
                {'code': 421, 'name': 'پروانه­ها، فن، بولئر و متعلقات', 'parent': ins4.id},
                {'code': 422, 'name': 'مخازن فلزی و غیر فلزی ', 'parent': ins4.id},
                {'code': 423, 'name': 'دیگ­های بخار، و تجهیزات مربوطه', 'parent': ins4.id},
                {'code': 424, 'name': 'سیستم­های گرمایشی و سرمایشی', 'parent': ins4.id},
                {'code': 510, 'name': 'تسمه فلزی بسته­بندی', 'parent': ins5.id},
                {'code': 511, 'name': 'زینک، بلنکت', 'parent': ins5.id},
                {'code': 512, 'name': 'قطعات کامپوزیت، تکستولیت، گرافیت، شیشه وسرامیک', 'parent': ins5.id},
                {'code': 513, 'name': 'قطعات ( نبشی، ناودانی، ورق، تسمه، تیرآهن )', 'parent': ins5.id},
                {'code': 514, 'name': 'رنگ­های صنعتی، عمومی و مواد مربوطه', 'parent': ins5.id},
                {'code': 515, 'name': 'سیمان، آجر، بلوک، خاک', 'parent': ins5.id},
                {'code': 516, 'name': 'مصالح ساختمان­سازی ', 'parent': ins5.id},
                {'code': 517, 'name': 'لفافه،کارتن پلاست و طلق­ها ', 'parent': ins5.id},
                {'code': 518,
                 'name': 'پوشش­های داخل ساختمانی (دکوراسیون داخلی وملزومات،پوشش کف،پوشش های سقف،پوشش­های بدنه و....)',
                 'parent': ins5.id},
                {'code': 519, 'name': 'پارچه­های نظافتی( تنظیف)', 'parent': ins5.id},
                {'code': 520, 'name': 'روغن، گریس، ضد یخ ', 'parent': ins5.id},
                {'code': 521, 'name': 'حلال­ها، پاک­کننده­ها (تینر،ایزو پروپیل الکل،استون)', 'parent': ins5.id},
                {'code': 522, 'name': 'چسب­ها', 'parent': ins5.id},
                {'code': 523, 'name': 'عایق ها و نسوزها(پشم سنگ­،آجر نسوز،خاک نسوز،سیمان نسوز )', 'parent': ins5.id},
                {'code': 524,
                 'name': 'سودکاستیک، پتاس، سدیم کربنات، سدیم تری پلی فسفات، سدیم دی کرومات، اسید کرومیک، سدیم متابی­سولفیت، سولفات آلومینیوم، پلی الکترولیت، سولفات قلع، سدیم کلرید',
                 'parent': ins5.id},
                {'code': 525, 'name': 'اسیدها( اسید سولفوریک )', 'parent': ins5.id},
                {'code': 526, 'name': 'PSA ، ENSA ، آنتی فوم، پلی اتیلن­گلیکول، مایع آب­بندی (ماستیک)، غوک، هیدرو­فیکس',
                 'parent': ins5.id},
                {'code': 527, 'name': 'روغن DOS ', 'parent': ins5.id},
                {'code': 528, 'name': 'مواد ضد رسوب و ضد خوردگی', 'parent': ins5.id},
                {'code': 529, 'name': 'پیگمنت آلومینیم، کوتینگ­ چاپ، لاک سفید، لاک ایزی اپن، لاک الکتروکوتر',
                 'parent': ins5.id},
                {'code': 530, 'name': 'ورنی چاپ، ورنی طلایی ایزی اپن', 'parent': ins5.id},
                {'code': 531, 'name': 'مرکب­ها', 'parent': ins5.id},
                {'code': 610, 'name': 'ماشین­ها و تجهیزات اداری، کامپیوتری و اجزای آنها ', 'parent': ins6.id},
                {'code': 611, 'name': 'اثاثیه و ملزومات اداری واقلام ستادی ', 'parent': ins6.id},
                {'code': 612, 'name': 'قفسه، کمد، ملزومات طبقه­بندی و گاو صندوق ', 'parent': ins6.id},
                {'code': 613, 'name': 'اقلام فرهنگی و تبلیغاتی', 'parent': ins6.id},
                {'code': 614, 'name': 'سیستم­های مداربسته', 'parent': ins6.id},
                {'code': 615, 'name': 'کلیه ملزومات آشپزخانه و آشپزی', 'parent': ins6.id},
                {'code': 616, 'name': 'مواد غذائی و خوراکی', 'parent': ins6.id},
                {'code': 617, 'name': 'گل، گیاه و درختچه­های زینتی', 'parent': ins6.id},
                {'code': 618, 'name': 'ملزومات باغبانی', 'parent': ins6.id},
                {'code': 710, 'name': 'اقلام نظافتی و بهداشتی وشوینده­ ها', 'parent': ins7.id},
                {'code': 711,
                 'name': 'اقلام حفاظت فردی ( لباس کار، ماسک، کلاه و سربند،کفش، عینک، دستکش، کمربند ایمنی، پیش بند ایمنی وگوشی) ',
                 'parent': ins7.id},
                {'code': 712, 'name': 'کپسول آتش­نشانی', 'parent': ins7.id},
                {'code': 713, 'name': 'لوازم پزشکی وکمک­های اولیه ', 'parent': ins7.id},
                {'code': 810,
                 'name': 'خدمات اجاره و اجاره به شرط تملیک (تجهیزات خاکبرداری، تجهیزات آزمایشگاهی، حمل و نقل، ماشین­های اداری)',
                 'parent': ins8.id},
                {'code': 811, 'name': 'خدمات اماکن ( زمین،هتل،رستوران،نمایشگاه و غرفه در سمینارها) ',
                 'parent': ins8.id},
                {'code': 812, 'name': 'خدمات پروژه­ای ( طراحی، مهندسی، تهیه و ساخت، نصب و راه اندازی، ( EPC ) و .... )',
                 'parent': ins8.id},
                {'code': 813, 'name': 'خدمات حمل­ونقل(دریایی،زمینی،هوایی) ', 'parent': ins8.id},
                {'code': 814, 'name': 'خدمات آزمایشگاهی وکالیبراسیون و بازرسی ', 'parent': ins8.id},
                {'code': 815, 'name': 'خدمات آموزشی،مشاوره­ای وتحقیقاتی', 'parent': ins8.id},
                {'code': 816, 'name': 'خدمات واردات و صادرات ', 'parent': ins8.id},
                {'code': 817,
                 'name': 'خدمات عمومی(تامین ****، خدمات حرفه­ای، خدمات حفاظتی، راهبری مراکز تفریحی و هتل، رفاهی و تشریفات) ',
                 'parent': ins8.id},
                {'code': 818, 'name': 'خدمات فرهنگی و تبلیغاتی ( چند رسانه ای و چاپ ، نمایشگاهی )', 'parent': ins8.id},
                {'code': 819,
                 'name': 'خدمات فنی و مهندسی ( اجرای پروژه­های فنی و مهندسی ( PC )،آماده سازی،راهبری و نگهداری،بازرسی فنی،بازسازی و تعمیرات و نگهداری،خدمات طراحی فنی و مهندسی و مشاوره،ساخت،نصب و راه­اندازی،فناوری اطلاعات،مهندسی معکوس، مونتاژ و دمونتاژ، نظارت عالیه و کارگاهی )',
                 'parent': ins8.id},
                ]

        for c in csss:
            psa = SupplementCategoriesSerializer(data=c)
            psa.is_valid(raise_exception=True)
            psa.save()

        return Response({})

    @list_route(methods=["GET"])
    def getRegisteredCount(self, request, *args, **kwargs):
        count = self.queryset.count()
        return Response({"count": count})

    @detail_route(methods=["POST"])
    def setType(self, request, *args, **kwargs):
        id = kwargs.get("id")
        instance = self.queryset.get(id=id)
        userinstance = MyUser.objects.get(id=instance.extra.get("userID"))
        tp = int(request.data.get("newType"))
        if tp in [4, 5, 6]:
            userinstance.account_type = tp
            userinstance.save()
        return Response({"result": "ok"})

    @detail_route(methods=["POST"])
    def removeIt(self, request, *args, **kwargs):
        id = kwargs.get("id")
        instance = self.queryset.get(id=id)
        rand_id = randint(1520025, 8999999)
        rm = "remove_" + str(rand_id) + "__"
        userinstance = MyUser.objects.filter(id=instance.extra.get("userID")).first()
        tp = request.data.get("newType")
        if tp == "OK":
            if userinstance:
                userinstance.username = rm + userinstance.username
                userinstance.email = rm + userinstance.email
                userinstance.cellphone = rm + userinstance.cellphone
                userinstance.save()
            instance.delete()
            return Response({"result": "ok"})
        return Response({"result": "no change"})

    @detail_route(methods=["POST"])
    def changePass(self, request, *args, **kwargs):
        id = kwargs.get("id")
        newPass = request.data.get("newPass")
        instance = self.queryset.get(id=id)
        userinstance = MyUser.objects.get(id=instance.extra.get("userID"))
        if newPass != "":
            userinstance.set_password(newPass)
            userinstance.save()
            return Response({"result": "ok"})
        return Response({"result": "no change"})
