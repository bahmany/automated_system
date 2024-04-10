angular.module('AniTheme').controller('FolderEditModalInstanceCtrl', function ($scope,
                                                                               $modalInstance,
                                                                               $http, $translate,
                                                                               LetterInboxService,
                                                                               oldFolder,
                                                                               InboxFolderService) {
    $scope.folder = {};
    $scope.SelectedFolder = {};
    $scope.listFolder = [];
    $scope.folder = oldFolder;


    $scope.ListFolders = function () {
        InboxFolderService.listFolder().then(function (data) {
            $scope.listFolder = data.data;
        }).catch(function (data) {

        });
    };
    $scope.ListFolders();

    $scope.saveFolder = function () {
        InboxFolderService.createFolder($scope.folder).then(function (data) {
            $modalInstance.close(data.data);
        });
    };
    $scope.cancelFolder = function () {
        $modalInstance.dismiss('cancel');
    };




});
