'use strict';

angular.module('AniTheme').controller(
    'BIBaseCtrl',
    function ($scope,
              $translate,
              $q, $http,
              $rootScope,
              $modal) {

        $scope.toggleLeft = buildToggler('right');
        $scope.menu = [];

        function buildToggler(componentId) {
            return function () {
                $mdSidenav(componentId).toggle();
            };
        }


        $scope.get_menu = function () {
            $http.get('/api/v1/bi_menus_items/get_menu/').then(function (data) {
                let casted = [];
                for (let i = 0; data.data.length > i; i++) {
                    let mmm = {};
                    if (data.data[i].parent == null && data.data[i].page == null) {
                        mmm = {
                            "icon": "fa fa-shopping-bag",
                            "name": data.data[i]['title'],
                            "type": "toggle"
                        }
                    } else {
                        mmm = {
                            "state": "bi-page({id:'" + data.data[i].page + "'})",
                            "icon": "fa fa-bar-chart",
                            "name": data.data[i]['title'],
                            "type": "link"
                        }
                    }
                    let ccc = [];
                    for (let y = 0; data.data[i].children.length > y; y++) {
                        if (data.data[i].children[y].page) {
                            ccc.push({
                                "state": "bi-page({id:'" + data.data[i].children[y].page + "'})",
                                "icon": "fa fa-newspaper-o",
                                "name": data.data[i].children[y]['title'],
                                "type": "link"
                            });
                        }
                    }
                    mmm['pages'] = ccc;
                    casted.push(mmm)
                }
                $scope.menu = casted;
            })
        }

        $scope.sections = [
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
                    },
                    {
                        "state": "bi-menus",
                        "icon": "fa fa-newspaper-o",
                        "name": "منوها",
                        "type": "link"
                    }
                ],
                "icon": "fa fa-tools",
                "name": "تنظیمات",
                "type": "toggle"
            },


        ];
        $scope.get_menu();

    });




