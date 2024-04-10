'use strict';


angular.module('AniTheme').controller(
    'ControlProjectSubProjectsCtrl',
    function ($scope,
              $translate,
              $http,
              $q, $stateParams,
              $mdDialog,
              $rootScope,
              $modal) {


        $scope.subProject = {};
        $scope.subProjects = {};
        $scope.yearID = $stateParams.YearID;

        var urlProject = "/api/v1/ControlProject/Year/"+$stateParams.ProjectID+"/subProjects/";
        crudProject($scope, $http,$rootScope, "project", urlProject, "modal_add_new_project");
        TableNav($scope,$http,"projects",urlProject );


    });