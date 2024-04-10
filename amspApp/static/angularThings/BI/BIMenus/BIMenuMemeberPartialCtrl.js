'use strict';


function BIMenuMemeberPartialCtrl($scope,
                                   $http,$mdDialog,
                                   selectedMenu) {


    $scope.allgroups = [];
    $scope.allusers = [];


    $scope.searchMemeber = "";
    $scope.getList = function (txt) {
        $http.get('/api/v1/bi_group/').then(function (data) {
            $scope.allgroups = data.data;
        });
    }


    // $scope.$watch("searchMemeber", function () {
    //     $scope.getList($scope.searchMemeber);
    // });


    $scope.__selectedMenu = selectedMenu;
    $scope.addToMember = function (group) {
        let found = false;

        if (!($scope.__selectedMenu['groups_allowed'])){
            $scope.__selectedMenu.groups_allowed = [];
        }

        for (let i = 0; $scope.__selectedMenu.groups_allowed.length > i; i++) {
            if ($scope.__selectedMenu.groups_allowed[i]['id'] === group.id) {
                found = true;
            }
        }
        if (found === false) {
            $scope.__selectedMenu.groups_allowed.push(group);
        }


    }

    $scope.removeFromList = function (index) {
        $scope.__selectedMenu.groups_allowed.splice(index, 1);
    }

    $scope.getList();


    $scope.savemember = function () {
        $http.patch("/api/v1/bi_menus/" + $scope.__selectedMenu.id + "/", $scope.__selectedMenu).then(function (data) {
            $mdDialog.hide();
        })
    }

}

