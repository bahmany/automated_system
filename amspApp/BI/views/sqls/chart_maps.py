from amspApp.BI.views.sqls.rahkaraan_quotation_items import rahkaraan_quotation_items
from amspApp.BI.views.sqls.rahkaraan_quotation_items_for_mobile import rahkaraan_quotation_items_for_mobile
from amspApp.BI.views.sqls.rahkaraan_quotation_items_sabte_avalie import rahkaraan_quotation_items_sabte_avalieh

charts_map = [
    {
        'link': 'dasgasdfawfasdvag',
        'class': rahkaraan_quotation_items
    }, {
        'link': 'egergervgegergreg',
        'class': rahkaraan_quotation_items_sabte_avalieh
    }, {
        'link': 'erghnvkjdnudfgsdfe',
        'class': rahkaraan_quotation_items_for_mobile
    }
]


bi_main_menu = [
            {
                "state": "bi-sample-page-for-ceo",
                "icon": "fa fa-bar-chart",
                "name": "صفحه ویژه",
                "type": "link"
            },

            {
                "state": "bi-amare-roozaneh",
                "icon": "fa fa-binoculars",
                "name": "آمارهای روزانه مدیران",
                "type": "link"
            },
            {
                "pages": [
                    {
                        "state": "bi-pages({id:'5'})",
                        "icon": "fa fa-adjust",
                        "name": "پیش فاکتورها",
                        "type": "link"
                    },{
                        "state": "bi-pages({id:'5'})",
                        "icon": "fa fa-adjust",
                        "name": "فروش کلی",
                        "type": "link"
                    },{
                        "state": "bi-pages({id:'3'})",
                        "icon": "fa fa-adjust",
                        "name": "فروش ناحیه ۱",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'4'})",
                        "icon": "fa fa-braille",
                        "name": "فروش ناحیه ۲",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-map-signs",
                        "name": "فروش  ضایعات",
                        "type": "link"
                    }],
                "icon": "fa fa-shopping-bag",
                "name": "فروش",
                "type": "toggle"
            },
            {
                "pages": [
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "تامین ورق سیاه",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "تامین قلع",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "تامین ناحیه ۲",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "SPII",
                        "type": "link"
                    }],
                "icon": "fa fa-magnet",
                "name": "تامین",
                "type": "toggle"
            }, {
                "pages": [
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "تولیدات ناحیه ۱",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "تولیدات ناحیه ۲",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "ورق کارمزدی",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "چاپ و لاک",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "قوطی سازی",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "آسان باز شو",
                        "type": "link"
                    }],
                "icon": "fa fa-magnet",
                "name": "تولید",
                "type": "toggle"
            }, {
                "pages": [
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "موجودی بانک ها",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "ال سی ها",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "تسهیلات",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "حقوق دستمزد",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "هزینه ها",
                        "type": "link"
                    },
                    {
                        "state": "bi-pages({id:'1'})",
                        "icon": "fa fa-newspaper-o",
                        "name": "دریافتی ها",
                        "type": "link"
                    }],
                "icon": "fa fa-magnet",
                "name": "مالی",
                "type": "toggle"
            },

            {
                "state": "bi-pages({id:'1'})",
                "icon": "fa fa-inbox",
                "name": "مصوبات هیات مدیره",
                "type": "link"
            },
            {
                "state": "bi-pages({id:'1'})",
                "icon": "fa fa-inbox",
                "name": "گزارشات پرسنل",
                "type": "link"
            },
            {
                "state": "bi-pages({id:'1'})",
                "icon": "fa fa-inbox",
                "name": "عملکردهای برنامه ای",
                "type": "link"
            },
            {
                "pages": [
                    {
                        "state": "bi-groups",
                        "icon": "fa fa-newspaper-o",
                        "name": "گروه ها",
                        "type": "link"
                    },
                    {
                        "state": "bi-dashboard-pages",
                        "icon": "fa fa-newspaper-o",
                        "name": "صفحات",
                        "type": "link"
                    },
                    {
                        "state": "bi-charts",
                        "icon": "fa fa-newspaper-o",
                        "name": "نمودارها",
                        "type": "link"
                    },
                    {
                        "state": "bi-sqls",
                        "icon": "fa fa-newspaper-o",
                        "name": "فراخوانی ها",
                        "type": "link"
                    },
                    {
                        "state": "bi-datasources",
                        "icon": "fa fa-newspaper-o",
                        "name": "منابع",
                        "type": "link"
                    }
                ],
                "icon": "fa fa-tools",
                "name": "تنظیمات",
                "type": "toggle"
            },


        ]