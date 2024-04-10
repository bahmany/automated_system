'use strict';
// The restrict option is typically set to:
// 'A' - only matches attribute name
// 'E' - only matches element name
// 'C' - only matches class name
// 'M' - only matches comment
angular.module('AniTheme').directive('biSingleValue', function () {

    return {
        templateUrl: '/static/angularThings/BI/BIPages/directives/bi_single_value.html',
        restrict: 'E',
        scope: {
            amartemplateid: '=amartemplateid'
        },
        replace: true,
        controller: ['$scope', '$element', '$attrs', '$transclude', '$http',
            function ($scope, $element, $attrs, $transclude, $http) {


                $scope.get_amar = function (amar_id) {
                    $http.get("/api/v1/dataForMS/" + amar_id + "/getLastEntery/").then(function (data) {
                        $scope.amar_values = data.data;
                    })
                }

                $scope.get_amar($scope.amartemplateid);


            }
        ],


    }
});
