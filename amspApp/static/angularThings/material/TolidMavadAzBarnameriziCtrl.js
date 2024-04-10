'use strict';


angular.module('AniTheme').controller(
    'TolidMavadAzBarnameriziCtrl',
    function ($scope,
              $translate,
              $http, $filter,
              $q, $mdDialog,
              $rootScope, $timeout,
              $modal) {




        $scope.coils = [];
        $scope.list = function () {
            $http.get("/api/v1/barcodes/getMaterialForTolid/").then(function (data) {
                $scope.coils = data.data;
            })
        }

        $scope.init = function () {
            $scope.list();
        }

        $scope.init();


        $scope.getToLine = function (barname, coil, ev, index) {
            var confirm = $mdDialog.confirm()
                .title('تولید')
                .textContent('از تولید این کویل اطمینان دارید ؟')
                .ariaLabel('ولید')
                .targetEvent(ev)
                .ok('اقدام به تولید')
                .cancel('انصراف');


            $mdDialog.show(confirm).then(function () {
                $http.post('/api/v1/barcodes/getToTolid/',
                    {
                        barname: barname,
                        coil: coil
                    }).then(function (data) {
                    // debugger;
                    let ddd = data.data;
                    angular.forEach($scope.coils, function (value, key) {
                        angular.forEach(value.items, function (valueB, keyB) {
                            if (valueB.id === ddd.coil.id) {
                                $scope.list();
                            }
                        })
                    })
                    if (data.data.coil) {
                        // coil = null;
                        // coil = data.data.coil;
                    }


                });

                $scope.status = 'You decided to get rid of your debt.';
            }, function () {
                $scope.status = 'You decided to keep your debt.';
            });
        };


    });


