'use strict';


function BIMenuMemeberUsersPartialCtrl($scope,
                                       $http, $mdDialog,
                                       selectedMenu) {


    $scope.PositionsList = {};
    $scope.positionListSearch = "";

    $scope.__selectedMenu = selectedMenu;


    $scope.$watch('positionListSearch', function () {
        $scope.GetPositions();
    });

    $scope.GetPositions = function () {
        $http.get("/api/v1/companies/0/members/getListJustHasPos/?q=" + $scope.positionListSearch).then(function (data) {
            $scope.PositionsList = data.data;
        }).catch(function () {

        })
    };


    $scope.addToPositions = function (position) {
        let found = false;

        if (!($scope.__selectedMenu['users_allowed'])) {
            $scope.__selectedMenu.users_allowed = [];
        }

        for (let i = 0; $scope.__selectedMenu.users_allowed.length > i; i++) {
            if ($scope.__selectedMenu.users_allowed[i]['positionID'] === position.positionID) {
                found = true;
            }
        }
        if (found === false) {
            $scope.__selectedMenu.users_allowed.push(position);
        }


    }


    $scope.savemember = function () {
        $http.patch("/api/v1/bi_menus/" + $scope.__selectedMenu.id + "/", $scope.__selectedMenu).then(function (data) {
            $mdDialog.hide();
        })
    }

    $scope.removeFromList = function (index) {
        $scope.__selectedMenu.users_allowed.splice(index, 1);
    }


    // $scope.addToPositions = function (position){
    //    
    // }
    // $scope.GetPositions();

}

