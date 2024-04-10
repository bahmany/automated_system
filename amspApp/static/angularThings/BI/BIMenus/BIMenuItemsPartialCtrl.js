'use strict';
'use strict';


function BIMenuItemsPartialCtrl($scope,
                                $http, $mdDialog,
                                selectedMenu) {


    $scope.pages = [];
    $scope.item = {};
    $scope.items = [];
    $scope.item.menu = selectedMenu.id;
    $scope.getItemPages = function () {
        $http.get('/api/v1/bi_dashboard_page/').then(function (data) {
            $scope.pages = data.data;
        })
    }

    $scope.getItemsJustParent = function () {
        $http.get('/api/v1/bi_menus_items/' + selectedMenu.id + '/get_just_parent/').then(function (data) {
            $scope.items = data.data;
        });
    }

    $scope.delete = function (item)
    {
        $http.delete('/api/v1/bi_menus_items/' + item.id + "/").then(function (data) {
            init();
        });
    }

    $scope.postItem = function () {
        if ($scope.item.id) {
            $http.patch('/api/v1/bi_menus_items/' + $scope.item.id + "/", $scope.item).then(function (data) {
                init();
            });

        } else {
            $http.post('/api/v1/bi_menus_items/', $scope.item).then(function (data) {
                init();
            });

        }
    }


    $scope._menu = {};
    $scope.get_structure = function () {
        $http.get('/api/v1/bi_menus_items/' + selectedMenu.id + "/get_one_step_menu/").then(function (data) {
            $scope._menu = data.data;
        });
    }


    $scope.edit = function (item) {
        $scope.item = item;
        if (item.menu) {
            $scope.item.menu = item.menu.id;
        }
        if (item.parent) {
            $scope.item.parent = item.parent.id;
        }
        if (item.page) {
            $scope.item.page = item.page.id;
        }

    }


    let init = function () {
        $scope.pages = [];
        $scope.item = {};
        $scope.item.menu = selectedMenu.id

        $scope.getItemPages();
        $scope.getItemsJustParent();
        $scope.get_structure();
    }


    init();


    $scope.saveit = function () {
        $http.patch("/api/v1/bi_menus/" + $scope.__selectedMenu.id + "/", $scope.__selectedMenu).then(function (data) {
            $mdDialog.hide();
        })
    }

}

