'use strict';


angular.module('AniTheme').controller(
    'BISqlsCtrl',
    function ($scope,
              $translate,
              $q,
              $rootScope, $stateParams,
              $mdDialog,
              $location,
              $http) {


        $scope.sqls = [];
        $scope.list = function (){
            $http.get('/api/v1/bi_sqls/').then(function (data){
                $scope.sqls = data.data;
            });
        }

        $scope.list();

        // $scope.createSQL = function () {
        //
        // }


        $scope.editorOptions = {
            lineWrapping: true,
            lineNumbers: true,
            readOnly: 'nocursor',
            mode: 'sql',
        };




    })