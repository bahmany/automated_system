'use strict';

angular.module('AniTheme')
    .directive('selectPosition', ['$http', '$q', function ($http, $q) {
        return {
            templateUrl: '/scripts/directives/select_position_directive/',
            replace: true,
            transclude: true,
            priority: 1,
            scope: {
                ngModel: '=',
                // ngChangeModel: '@',
            },
            link: function (scope, element) {
                // if (!(scope.ngModel)) {
                //     scope.ngModel = {};
                // }

                scope.ngChangeModel = function (item) {
                    console.log("I am going to change this")
                }

                // scope.myModel = null;
                scope.selected = {};
                scope.positions = [];
                scope.searchText = "";
                scope.searchSting = "";
                console.log("loooadeddded");
                // scope.$watch('ngModel', function () {
                //     // scope.searchText = null;
                //     console.log("watcher from directive ----------------------");
                //     console.log(scope.ngModel);
                //     // scope.profileName = null;
                //     if (scope.ngModel) {
                //         // scope.profileName = scope.ngModel.profileName;
                //         // scope.searchText = scope.ngModel.profileName;
                //
                //     }
                //     // scope.ngModel.$render();
                //
                // })

                scope.setSearchText = function () {
                    if (!scope.ngModel) {
                        return ''
                    }
                    return scope.ngModel.searchText
                }

                scope.querySearch = function () {
                    // if (!scope.ngModel){
                    //     return []
                    // }

                    var results = $http.get("/api/v1/members-search/?page_size=5&q=" + scope.searchSting);
                    var deferred = $q.defer();
                    results.then(function (results) {
                        deferred.resolve(results.data.results);
                    }).catch(function (resu) {
                        defer.reject(resu.data.results);
                    });
                    return deferred.promise;
                }
                scope.selectedItemChange = function (item) {
                    scope.$parent.$parent[element.attr('ng-model')] = item;
                }


            }
        }
    }]);
