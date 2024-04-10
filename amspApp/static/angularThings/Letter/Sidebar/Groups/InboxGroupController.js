'use strict';


angular.module('AniTheme').controller('GroupEditModalInstanceCtrl', function ($scope,
                                                                              $modalInstance,
                                                                              $http,
                                                                              $translate,
                                                                              LetterInboxService,
                                                                              oldGroup,
                                                                              InboxGroupService) {
    $scope.group = oldGroup;
    $scope.finalList = [];
//------------------------------------------------------
//------------------------------------------------------
//------------------------------------------------------
    memberInbox($scope, $http);
//------------------------------------------------------
//------------------------------------------------------
//------------------------------------------------------
    chartInbox($scope, $http);
//--------------------------------------------------
//--------------------------------------------------
//--------------------------------------------------
    zoneInbox($scope, $http);
//-------------------------------------------------
//-------------------------------------------------
//-------------------------------------------------
    groupInbox($scope, $http);
//-------------------------------------------------
//-------------------------------------------------
//-------------------------------------------------

    $scope.saveGroup = function () {
        var finalSent = {
            group: $scope.group,
            members: $scope.selects
        };
        InboxGroupService.editGroup(
            finalSent).then(function (data) {
                $modalInstance.close(data.data);
            }).catch(function (data) {
                swal('Error', data.data.title, "error");
            });
    };
    $scope.listMember = function () {
        InboxGroupService.listGroupMembers($scope.group.id, $scope.MembersSearchText).then(function (data) {
            $scope.selects = data.data.members;
        }).catch(function (data) {

        });
        //$scope.member = $scope.group.members
    };
    $scope.listMember();
    $scope.cancelGroup = function () {
        $modalInstance.dismiss('cancel');
    };

});