'use strict';


angular.module('AniTheme').controller(
    'QCBaseController',
    function ($scope,
              $translate,
              $http,
              $q, $mdDialog,
              $rootScope,
              $modal) {


        $scope.PdfParse = function () {
            $http.post("/api/v1/qcfinding/parsPdf/",{})
        }
        

    });