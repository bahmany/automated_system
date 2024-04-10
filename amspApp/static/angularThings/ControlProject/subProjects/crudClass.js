'use strict';


function crudProject($scope, $http, $rootScope, modelName, url, modalDivID) {
    $scope.Post = function () {
        if ($scope[modelName].id) {
            $http.patch(url + $scope[modelName].id + "/", $scope[modelName]).then(function (data) {
                if (data.data.id) {
                    $scope[modelName + "sList"]();
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    $("#" + modalDivID).modal("hide");

                } else {
                    swal.showInputError("لطفا در ورود اطلاعات دقت نمایید");
                }


            }).catch(function (data) {

            });

        } else {
            $http.post(url, $scope[modelName]).then(function (data) {
                if (data.data.id) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    $scope[modelName + "sList"]();
                    $("#" + modalDivID).modal("hide");
                } else {
                    swal.showInputError("لطفا در ورود اطلاعات دقت نمایید");
                }
            }).catch(function (data) {

            });

        }
    };
    $scope.Cancel = function () {
        $scope[modelName] = {};
    };
    $scope.AddNewProject = function () {

        $scope[modelName] = {};
        $("#" + modalDivID).modal("show");
    };
    $scope.Edit = function (project) {
        $scope[modelName] = project;
        $("#" + modalDivID).modal("show");
    };
    $scope.Delete = function ($index, project) {
        swal({
            title: "حذف دوره",
            text: "آیا از حذف دوره انتخابی اطمینان دارید",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "بله",
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            $http.delete(url + project.id + "/").then(function (data) {
                $scope[modelName + "sList"]();

                swal("حذف شد!", "دوره انتخابی حذف شد", "success");

            })
        });
    };
}