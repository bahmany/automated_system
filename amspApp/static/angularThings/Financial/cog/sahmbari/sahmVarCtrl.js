'use strict';

angular.module('AniTheme').controller(
    'sahmVarCtrl',
    function ($scope,
              //$translate,
              $q,
              $http,
              $location,
              $rootScope,
              $timeout) {

        $scope.tashimVar = {};


        $scope.editTashim = function (item) {
            $scope.tashimVar = item;
            $("#colored-header").modal("show");
        };

        $scope.deleteTashim = function (item) {
            if (confirm("آیا می خواهید حذف نمایید ؟")) {
                $http.delete("/Financial/api/v1/tashvar/" + item.id + "/").then(function (e) {
                    showSuccMsg("با موفقیت حذف شد");
                    $scope.getTashimList();

                })
            }
        };

        $scope.getDetCode = function () {
            $http.get("/Financial/api/v1/tashvar/GetKol_uwyegfjsdf875ryhfewigfw487ykdfjvdisgheirgh9759348wewpeofu39457/").then(function (data) {
            }).catch(function (e) {

            })
        }

        $scope.getCalcMarkazeTolidi = function () {
            $http.get("/Financial/api/v1/tashvar/GetKol_dflighghghfihdisfvh9er8ugheivnWIQWEFASDLVKJBH9R8GALDSJFOSADF/").then(function (data) {
            }).catch(function (e) {

            })
        }


        $scope.tashimVars = [];

        $scope.getTashimList = function () {
            $http.get("/Financial/api/v1/tashvar/").then(function (data) {
                $scope.tashimVars = data.data
            }).catch(function (e) {
                $scope.tashimVars = [];
            })
        };
        $scope.getTashimList();


        $scope.$watch("tashimVar.sl", function () {
            $scope.tashimVar.moeenTitle = "";
            if ($scope.tashimVar.sl === undefined) {
                return
            }
            $scope.getGlText($scope.tashimVar.sl, "sl")
        })

        $scope.$watch("tashimVar.gl", function () {
            $scope.tashimVar.tafzilTitle = "";
            if ($scope.tashimVar.gl === undefined) {
                return
            }
            $scope.getGlText($scope.tashimVar.gl, "gl")
        })

        $scope.postTashim = function () {
            var ps;
            if ($scope.tashimVar.id) {
                ps = $http.patch("/Financial/api/v1/tashvar/" + $scope.tashimVar.id + "/", $scope.tashimVar)
            } else {
                ps = $http.post("/Financial/api/v1/tashvar/", $scope.tashimVar)
            }

            ps.then(function (data) {
                if (data.data.id) {
                    $scope.getTashimList();
                    $scope.tashimVar = {};
                    $("#colored-header").modal("hide");
                    showSuccMsg("تخصیص مورد نظر ثبت شد")
                }
            }).catch(function (e) {
                showErrMsg("خطا....")

            })
        }

        $scope.getGlText = function (code, dest) {
            $http.get("/Financial/api/v1/accgl/" + code + "/getAccNum/").then(function (data) {
                if (data.data.res) {
                    var dt = data.data.res;
                    if (dest === "sl") {
                        $scope.tashimVar.moeenTitle = dt;
                    }
                    if (dest === "gl") {
                        $scope.tashimVar.tafzilTitle = dt;
                    }

                    // hot.setDataAtCell(changes[0][0], 3, data.data.res);
                }
            }).catch(function (e) {
            })

        }

        $scope.OpenNewTashimPanel = function () {

        }


        $scope.cancelTashim = function () {
            $scope.tashimVar = {};
            $("#colored-header").modal("hide");

        }

        $scope.UpdateGL = function (ev) {
            var btnCaption = ev.target.innerText;
            ev.target.innerText = "لطفا صبر کنید ...";
            ev.target.enabled = false;
            $http.get("/Financial/api/v1/accgl/updateFromSG/").then(function (data) {
                if (data.data.result) {

                    $http.get("/Financial/api/v1/accsl/updateFromSG/").then(function (data) {
                        if (data.data.result) {
                            ev.target.innerText = btnCaption;
                            ev.target.enabled = true;
                            showSuccMsg("با موفقیت بروز رسانی شد")

                        } else {
                            ev.target.innerText = btnCaption;
                            ev.target.enabled = true;
                        }
                    }).catch(function (data) {
                        ev.target.innerText = btnCaption;
                        ev.target.enabled = true;
                    })

                } else {
                    ev.target.innerText = btnCaption;
                    ev.target.enabled = true;
                }
            }).catch(function (data) {
                ev.target.innerText = btnCaption;
                ev.target.enabled = true;
            })
        }


    });
