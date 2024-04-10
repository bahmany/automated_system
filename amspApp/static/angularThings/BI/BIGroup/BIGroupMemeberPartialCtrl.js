'use strict';


function BIGroupMemeberPartialCtrl($scope,
                                   $http,$mdDialog,
                                   selectedGroup) {


    $scope.allmembers = [];


    $scope.searchMemeber = "";
    $scope.getList = function (txt) {
        $http.get('/api/v1/bi_group/get_all_member/?q=' + txt).then(function (data) {
            $scope.allmembers = data.data;
        });
    }


    $scope.$watch("searchMemeber", function () {
        $scope.getList($scope.searchMemeber);
    });


    $scope.__selectedMember = selectedGroup.groupMember;
    $scope.addToMember = function (member) {
        let found = false;
        for (let i = 0; $scope.__selectedMember.length > i; i++) {
            if ($scope.__selectedMember[i]['positionID'] === member.positionID) {
                found = true
            }
        }
        if (found === false) {
            $scope.__selectedMember.push(member);
        }
        selectedGroup.groupMember = $scope.__selectedMember;

    }

    $scope.removeFromList = function (index) {
        $scope.__selectedMember.splice(index, 1);
    }

    // $scope.getList();


    $scope.savemember = function () {
        $http.patch("/api/v1/bi_group/" + selectedGroup.id + "/", selectedGroup).then(function (data) {
            $mdDialog.hide();
        })
    }

}

