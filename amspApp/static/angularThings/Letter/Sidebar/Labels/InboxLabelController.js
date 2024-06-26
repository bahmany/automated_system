'use strict';

angular.module('AniTheme').controller('ModalLabelCreateInstanceCtrl', function (
    $scope,
    $modalInstance,
    $http,
    $translate,
    LetterInboxService,
    InboxLabelService,
    oldLabel) {
    $scope.newLabel = {};
    if (oldLabel) {
        $scope.newLabel.title = oldLabel.title;
        $scope.newLabel.color = oldLabel.color;
        $scope.newLabel.bgcolor = oldLabel.bgcolor;
    } else {
        $scope.newLabel.color = '#000000';
        $scope.newLabel.bgcolor = '#FAFAFA';

    }

    $scope.saveLabel = function () {
        $scope.newLabel.positionID = 2;
        if (oldLabel) {
            InboxLabelService.editLabel(oldLabel.id, $scope.newLabel).then(function (data) {
                $modalInstance.close(data.data);
            }).catch(function (data) {
                swal('Error', data.data.title, "error");
            });
        } else {
            InboxLabelService.createLabel($scope.newLabel).then(function (data) {
                $modalInstance.close(data.data);
            }).catch(function (data) {
                swal('Error', data.data.title, "error");
            });
        }

    };

    $scope.cancelLabel = function () {
        $modalInstance.dismiss('cancel');
    };
});
