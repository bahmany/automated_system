'use strict';
angular.module('AniTheme')
    .controller(
        'TaminDakheliRegisteredCtrl',
        function ($scope, $window, $http, $translate, $rootScope, $stateParams, $location, $$$, $filter, $state, Upload) {


            var table = $('#table2').DataTable({
                "processing": true,
                "serverSide": true,
                "searchDelay": 500,
                "order": [[0, "desc"]],
                "ajaxSource": "/api/v1/adminTaminDakheli/getForDataTables/",
                // "ajax": {
                // "url": "/Financial/api/v1/cog_89/",
                // "url": "/api/v1/adminTaminDakheli/getForDataTables/",
                // "type": "GET"
                // },
                "columns": [
                    {'type': 'string', 'data': 'extra.gen_code', 'title': 'کد'},
                    {'type': 'string', 'data': 'extra.username', 'title': 'نام کاربر / موبایل'},
                    {'type': 'string', 'data': 'extra.name', 'title': 'نام تامین کننده'},
                    {'type': 'string', 'data': 'extra.type_of_provider', 'title': 'نوع'},
                    {'type': 'string', 'data': 'dateOfPost', 'title': 'تاریخ ثبت نام'},
                    {
                        'data': 'id',
                        "searchable": false,
                        "title": "عملیات",
                        "render": function (data, type, full) {
                            return "<button onclick='karshEdit(\"" + data + "\");'>ویرایش</button> " +
                                "<button onclick='karshDel(\"" + data + "\");'>حذف</button> " +
                                "<button onclick='changeType(\"" + data + "\");'>تغییر نوع</button> " +
                                "<button onclick='changePass(\"" + data + "\");'>تغییر رمز</button> "

                        }
                    }
                ]
            });


            $scope.dataTableOpt = {
                // fnPageChange: tablePageChange,

                //custom datatable options
                "aLengthMenu": [[10, 50, 100, 200], [10, 50, 100, 200]],
                "bProcessing": true,
                "sAjaxSource": '/api/v1/adminTaminDakheli/getForDataTables/',
                "bServerSide": true,
                "iSearchDelay": 500,
                "aoColumns": [
                    {"mData": "extra.gen_code", "sTitle": "کد"},
                    {"mData": "extra.username", "sTitle": "نام کاربر / موبایل"},
                    {"mData": "extra.name", "sTitle": "نام تامین کننده"},
                    {"mData": "extra.type_of_provider", "sTitle": "نوع"},
                    {"mData": "dateOfPost", "sTitle": "تاریخ ثبت نام"},
                    {
                        "mData": "id",
                        "bSearchable": false,
                        "sTitle": "عملیات",
                        "mRender": function (data, type, full) {
                            return "<button onclick='karshEdit(\"" + data + "\");'>ویرایش</button> " +
                                "<button onclick='karshDel(\"" + data + "\");'>حذف</button> " +
                                "<button onclick='changeType(\"" + data + "\");'>تغییر نوع</button> " +
                                "<button onclick='changePass(\"" + data + "\");'>تغییر رمز</button> "

                        }
                    }
                    // "sDefaultContent": "<button onclick='hiii(this);'>...</button>"}
                    // {"mData": "row.z_MeghdareMandePayamDoreh", "sTitle": "مقداری مانده پایان دوره", "sType": "numeric"},
                    // {"mData": "row.z_MablagheMandePayamDoreh", "sTitle": "ریالی مانده پایان دوره", "sType": "numeric"},
                    // {"mData": "row.z_MeghdareKhaleseTolidi", "sTitle": "مقداری خالص مصرف تولیدی", "sType": "numeric"},
                    // {"mData": "row.z_MablagheKhaleseTolidi", "sTitle": "ریالی خالص مصرف تولیدی", "sType": "numeric"}
                ]
            };


            $scope.edit = function (id) {
                $state.go("TaminDakheliRegisteredDetails", {details: id});
            }

            $scope.changeType = function (id) {
                var ss = prompt("نوع را وارد کنید ۴=فروشنده   ۵=خدماتی   ۶=سازنده", "")
                if (ss) {
                    if (ss !== "") {
                        $http.post("/api/v1/adminTaminDakheli/" + id + "/setType/", {newType: ss}).then(function (data) {
                            if (data.data.result == "ok") {
                                location.reload();
                            }
                        })

                    }

                }
            }

            $scope.del = function (id) {
                var ss = prompt("پس از حذف امکان برگشت اطلاعات وجود ندارد لطفا تایپ کنید OK", "")
                if (ss) {
                    if (ss === "OK") {
                        $http.post("/api/v1/adminTaminDakheli/" + id + "/removeIt/", {newType: ss}).then(function (data) {
                            if (data.data.result === "ok") {
                                location.reload();
                            }
                        })
                    }
                }
            };

            $scope.registeredCount = -1;
            $scope.getRegisteredCount = function () {
                $http.get("/api/v1/adminTaminDakheli/getRegisteredCount/").then(function (data) {
                    $scope.registeredCount = data.data.count;
                })
            }
            $scope.getRegisteredCount();
            $scope.changePass = function (id) {
                var ss = prompt("لطفا رمز جدید را وارد کنید", "");
                if (ss) {
                    $http.post("/api/v1/adminTaminDakheli/" + id + "/changePass/", {newPass: ss}).then(function (data) {
                        if (data.data.result == "ok") {
                            alert("رمز عبور تغییر کرد");
                        }
                    })
                }
            }


            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            $scope.headerDet = {};
            $scope.Files = {};
            $scope.downloadFile = {};
            $scope.UploadedFiles = [];
            $scope.Scans = {};
            $scope.Scan = {};
            loadUploader($scope, $http, Upload);
            $scope.showUploader = function () {
                $("#divFiles").fadeOut(function () {
                    $("#divUploader").fadeIn();
                });
            };
            $scope.cancelFiles = function () {
                $("#divUploader").fadeOut(function () {
                    $("#divFiles").fadeIn();
                });
            }
            $scope.RemoveFromUploaded = function (ev, index) {

                var confirm = $mdDialog.confirm()
                    .title('حذف فایل')
                    .textContent('فایل مورد نظر حذف شود ؟')
                    .ariaLabel('حذف فایل')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {

                    $scope.UploadedFiles.splice(index, 1);

                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });


            }


            $scope.addToOdoo = function () {
                $http.post('/api/v1/adminTaminDakheli/genOdooContact/', {}).then(function (data) {

                })
            }


        });


function karshEdit(id) {
    var scope = angular.element($("#ppapapapa")).scope();
    scope.edit(id);

}

function karshDel(id) {
    var scope = angular.element($("#ppapapapa")).scope();
    scope.del(id);
}


function changeType(id) {
    var scope = angular.element($("#ppapapapa")).scope();
    scope.changeType(id);
}

function changePass(id) {
    var scope = angular.element($("#ppapapapa")).scope();
    scope.changePass(id);
}


