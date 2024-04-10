'use strict';

angular.module('Supplement').controller(
    'profileCtrl',
    function ($scope,
              $q,
              $http,
              FileUploader,
              $state,
              $location,
              $rootScope,
              $timeout) {


        $scope.profile = {};
        $scope.getProfile = function () {
            $http.get("/api/v1/profile/1/").then(function (data) {
                $scope.profile = data.data;
            });
        };

        $scope.getProfile();


        $scope.changeAvatarOpenUploader = function () {
            // angular.element(document.getElementById("divAvatarUploader")).trigger('click');
            document.getElementById("divAvatarUploader").click();
        };

        var uploader = $scope.uploader = new FileUploader({
            url: '/api/v1/file/upload'
        });

        uploader.filters.push({
            name: 'customFilter',
            fn: function (item /*{File|FileLikeObject}*/, options) {
                return this.queue.length < 10;
            }
        });

        var controller = $scope.controller = {
            isImage: function(item) {
                var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
            }
        };

        uploader.onAfterAddingFile = function (fileItem) {
            uploader.uploadAll();
        }

        uploader.onCompleteItem = function (fileItem, response, status, headers) {
            // console.log("uploader.onCompleteItem");
            // fileItem.serverAddress = response;
            // if (!($scope.uploadedFiles)) {
            //     $scope.uploadedFiles = [];
            // }
            // $scope.uploadedFiles.push(response);
            // dataToSend.parentScope.uploadedFiles = $scope.uploadedFiles;
            // console.info('onCompleteItem', fileItem, response, status, headers);
        };
    });