'use strict';

angular.module('AniTheme')
    .directive('sidebar', function ($http, companiesManagmentService) {
            return {
                templateUrl: '/scripts/directives/sidebar/',
                restrict: 'E',
                replace: true,
                controller: 'sidenavCtrl',
                link: function (scope, element, attr, $location, $rootScope, $mdSidenav) {
                    scope.currentCompany = {};
                    scope.toggleDateShow = false;
                    scope.hostname = "";
                    scope.companyLogo = "";
                    scope.companyLogo = companyLogo;
                    scope.companyName = companyName;
                    scope.global = $rootScope;

                    scope.GetCompaniesList = function () {
                        $http.get("/api/v1/companies/" + companyID + "/positions/CompaniesForCurrent/").then(function (data) {
                            scope.companies = data.data;
                        })
                    };
                    scope.initCurrentCompany = function (CurrentCompanyId, CurrentCompanyName) {
                        scope.currentCompany.name = CurrentCompanyName;
                        scope.currentCompany.id = CurrentCompanyId;
                    };

                    scope.ShowCompanyList = false;
                    scope.ToggleChoose = function () {
                        scope.ShowCompanyList = !scope.ShowCompanyList
                    }


                    scope.setAsCurrent = function (_companyId) {
                        companiesManagmentService.setAsCurrentService(userID, _companyId).then(
                            function (data) {
                                if (data.id) {
                                    window.location.reload();
                                }
                            });
                    };
                    scope.GetCompaniesList();


                    scope.getUnreadCount = function () {
                        $http.get('/api/v1/notify/getUnreadsCount/').then(function (data) {
                            scope.$root.alarms = data.data;
                        })
                    }

                    // scope.getUnreadCount();

                }
            }
        }
    )
    .factory('menu', [
        '$location',
        '$rootScope',
        '$http',
        "$mdSidenav", "$timeout",
        function ($location, $http, $rootScope, $mdSidenav, $timeout) {

            var sections = [
                {
                    "state": "home",
                    "icon": "fa fa-home",
                    "name": "خانه",
                    "type": "link"
                },

                {
                    "state": "list",
                    "icon": "fa fa-inbox",
                    "name": "کارتابل",
                    "type": "link"
                }, {
                    "state": "secretariat",
                    "icon": "fa fa-tasks",
                    "name": "دبیرخانه",
                    "type": "link"
                }, {
                    "state": "bi",
                    "icon": "fa fa-tasks",
                    "name": "داشبورد مدیریتی",
                    "type": "link"
                }, {
                    "state": "edari",
                    "icon": "fa fa-bar-chart",
                    "name": "اداری",
                    "type": "link"
                },
                {
                    "pages": [
                        {
                            "state": "SalesReportBase",
                            "icon": "fa fa-newspaper-o",
                            "name": "گزارش ها",
                            "type": "link"
                        },
                        {
                            "state": "HavalehForoosh",
                            "icon": "fa fa-money",
                            "name": "حواله فروش",
                            "type": "link"
                        }, {
                            "state": "Khorooj",
                            "icon": "fa fa-car",
                            "name": "حواله خروج",
                            "type": "link"
                        },{
                            "state": "MojoodiGhabeleForoosh",
                            "icon": "fa fa-car",
                            "name": "موجودی قابل فروش",
                            "type": "link"
                        }, {
                            "state": "OldHavalehForoosh",
                            "icon": "fa fa-bar-chart",
                            "name": "حواله فروش قدیمی",
                            "type": "link"
                        }, {
                            "state": "OldKhorooj",
                            "icon": "fa fa-bar-chart",
                            "name": "حواله خروج قدیمی",
                            "type": "link"
                        }, {
                            "state": "Karshenasi",
                            "icon": "fa fa-bar-chart",
                            "name": "درخواست ها",
                            "type": "link"
                        }, {
                            "state": "TaminDakheliRegistered",
                            "icon": "fa fa-bar-chart",
                            "name": "تامین کننده ها",
                            "type": "link"
                        }, {
                            "state": "SalesConv",
                            "icon": "fa fa-bar-chart",
                            "name": "مذاکرات",
                            "type": "link"
                        }, {
                            "state": "SendSMS",
                            "icon": "fa fa-bar-chart",
                            "name": "ارسال پیام کوتاه",
                            "type": "link"
                        }],

                    "icon": "fa fa-magnet",
                    "name": "بازرگانی",
                    "type": "toggle"
                },
                {
                    "pages": [
                        {
                            "state": "request-goods",
                            "icon": "fa fa-bar-chart",
                            "name": "آواتار و عکس من",
                            "type": "link",
                            "href": "/page/apps/imageUploadCrop/home/",
                            "target": "_blank"
                        },
                        {
                            "state": "Contacts",
                            "icon": "fa fa-users",
                            "name": "دفترچه تلفن",
                            "type": "link"
                        },
                        {
                            "state": "companies-dashboard",
                            "icon": "fa fa-building",
                            "name": "مدیریت شرکت ها",
                            "type": "link"
                        },

                        {
                            "state": "AccessToSecratariat",
                            "icon": "fa fa-bar-chart",
                            "name": "دسترسی ها",
                            "type": "link"
                        },
                        {
                            "state": "Change",
                            "icon": "fa fa-bar-chart",
                            "name": "رمز عبور و ایمیل",
                            "type": "link"
                        }],

                    "icon": "fa fa-bar-chart",
                    "name": "ابزارهای من",
                    "type": "toggle"
                },
                {
                    "pages": [{
                        "state": "material_locations",
                        "icon": "fa fa-bar-chart",
                        "name": "انبارها",
                        "type": "link"
                    }, {
                        "state": "material_baskol",
                        "icon": "fa fa-bar-chart",
                        "name": "باسکول و ورود",
                        "type": "link"
                    }, {
                        "state": "material_bakol_to_anbar",
                        "icon": "fa fa-bar-chart",
                        "name": "ورود به انبار ورق سیاه",
                        "type": "link"
                    }, {
                        "state": "qc_blackplate",
                        "icon": "fa fa-bar-chart",
                        "name": "کیفیت و انبار ورق سیاه",
                        "type": "link"
                    }
                        // ,
                        // {
                        // "state": "material_tolid_sale_conv",
                        // "icon": "fa fa-bar-chart",
                        // "name": "فروش و تولید",
                        // "type": "link"
                        // }
                        , {
                            "state": "material_barname_base",
                            "icon": "fa fa-bar-chart",
                            "name": "برنامه ریزی",
                            "type": "link"
                        }, {
                            "state": "material_barname_tolid",
                            "icon": "fa fa-bar-chart",
                            "name": "اقدام به تولید",
                            "type": "link"
                        }, {
                            "state": "material_reports",
                            "icon": "fa fa-bar-chart",
                            "name": "گزارش",
                            "type": "link"
                        }
                        // ,{
                        //     "state": "material_barcode_list",
                        //     "icon": "fa fa-bar-chart",
                        //     "name": "ورود و خروج",
                        //     "type": "link"
                        // }
                        , {
                            "state": "request-goods-help",
                            "icon": "fa fa-bar-chart",
                            "name": "راهنما",
                            "type": "link"
                        }],

                    "icon": "fa fa-bar-chart",
                    "name": "گردش مواد",
                    "type": "toggle"
                },
                {
                    "pages": [{
                        "state": "request-goods",
                        "icon": "fa fa-bar-chart",
                        "name": "درخواست کالا",
                        "type": "link"
                    }, {
                        "state": "request-goods-chat",
                        "icon": "fa fa-bar-chart",
                        "name": "گفتگو با انبار",
                        "type": "link"
                    }, {
                        "state": "request-goods-help",
                        "icon": "fa fa-bar-chart",
                        "name": "راهنما",
                        "type": "link"
                    }],

                    "icon": "fa fa-bar-chart",
                    "name": "درخواست کالا",
                    "type": "toggle"
                },
                {
                    "state": "inbox-process-dashboard",
                    "pages": [
                        {
                            "state": "inbox-process-dashboard",
                            "icon": "fa fa-inbox",
                            "name": "کارتابل",
                            "type": "link"
                        }, {
                            "state": "message-process-dashboard",
                            "icon": "fa fa-envelope-o",
                            "name": "پیام ها و نتایج",
                            "type": "link"
                        }, {
                            "state": "doneArchive-process-dashboard",
                            "icon": "fa fa-search",
                            "name": "پایش",
                            "type": "link"
                        }, {
                            "state": "lunchedArchive-process-dashboard",
                            "icon": "fa fa-table    ",
                            "name": "بایگانی",
                            "type": "link"
                        }, {
                            "state": "reports-process-dashboard",
                            "icon": "fa fa-tasks",
                            "name": "گزارشات",
                            "type": "link"
                        }, {
                            "state": "search-process-dashboard",
                            "icon": "fa fa-search",
                            "name": "استعلام",
                            "type": "link"
                        }],
                    "icon": "fa fa-refresh",
                    "name": "فرآیندها",
                    "type": "toggle"
                },
                {
                    "pages": [{
                        "state": "cog_home",
                        "icon": "fa fa-bar-chart",
                        "name": "بهای تمام شده",
                        "type": "link"
                    }],

                    "icon": "fa fa-bar-chart",
                    "name": "مالی اداری",
                    "type": "toggle"
                },
                // {
                //     "state": "Sales",
                //     "icon": "fa fa-eur",
                //     "name": "فرم و آیین نامه ها",
                //     "type": "link",
                //     "href": "/docs/blog/",
                //     "target": "_blank"
                // },
                // {
                //     "state": "control_project",
                //     "icon": "fa fa-eur",
                //     "name": "کنترل پروژه",
                //     "type": "link",
                //     "target": "_blank"
                // },
                // {
                //     "state": "trace-cat",
                //     "icon": "fa fa-bar-chart",
                //     "name": "ردیابی",
                //     "type": "link"
                // },

                {
                    "state": "statistics",
                    "icon": "fa fa-bar-chart",
                    "name": "آمارها",
                    "type": "link"
                },
                {
                    "state": "datatables",
                    "icon": "fa fa-table",
                    "name": "جداول داده",
                    "type": "link"
                },
                {
                    "state": "oldAmsp",
                    "icon": "fa fa-graduation-cap",
                    "name": "نسخه قبلی",
                    "type": "link"
                }];


            var self;
            return self = {
                sections: sections,
                globalscope: $rootScope,

                toggleSelectSection: function (section) {
                    self.openedSection = (self.openedSection === section ? null : section);
                },
                isSectionSelected: function (section) {
                    return self.openedSection === section;
                },

                selectPage: function (section, page) {
                    page && page.url && $location.path(page.url);
                    self.currentSection = section;
                    self.currentPage = page;
                }
            };

            function sortByHumanName(a, b) {
                return (a.humanName < b.humanName) ? -1 :
                    (a.humanName > b.humanName) ? 1 : 0;
            }


        }])
    .directive('menuToggle', ['$timeout', function ($timeout) {
        return {
            scope: {
                section: '='
            },
            templateUrl: '/static/angularThings/others/directives/sidebar/menu-toggle.tmpl.html',
            link: function (scope, element) {
                // var controller = element.parent().controller();
                var controller = scope.$root;

                scope.isOpen = function () {
                    return controller.isOpen(scope.section);
                };
                scope.toggle = function () {
                    controller.toggleOpen(scope.section);
                };

                var parentNode = element[0].parentNode.parentNode.parentNode;
                if (parentNode.classList.contains('parent-list-item')) {
                    var heading = parentNode.querySelector('h2');
                    element[0].firstChild.setAttribute('aria-describedby', heading.id);
                }
            }
        };
    }])
    .directive('menuLink', function () {
        return {
            scope: {
                section: '='
            },
            templateUrl: '/static/angularThings/others/directives/sidebar/menu-link.tmpl.html',
            link: function ($scope, $element) {
                var controller = $scope.$root;

                $scope.focusSection = function () {
                    // set flag to be used later when
                    // $locationChangeSuccess calls openPage()
                    controller.autoFocusContent = true;
                };
            }
        };
    })

