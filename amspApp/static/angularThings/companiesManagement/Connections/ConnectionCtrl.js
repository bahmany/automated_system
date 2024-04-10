'use strict';
angular.module('AniTheme')
    .controller('ConnectionCtrl', function ($scope,
                                            $http,
                                            $timeout,
                                            $rootScope,
                                            $stateParams,
                                            $location,
                                            $$$) {






        // ---------------------------------------------------
        // ---------------------------------------------------
        // ---------------------------------------------------
        // ---------------------------------------------------
        // ---------------------------------------------------





        // ---------------------------------------------------
        // ---------------------------------------------------
        // ---------------------------------------------------
        // ---------------------------------------------------
        // ---------------------------------------------------
        // ---------------------------------------------------




        $scope.companyId = $stateParams.companyid;

        $scope.Connection = {};
        $scope.post = function () {
            $http.post("/api/v1/companies/" + $scope.companyId + "/connections/", $scope.Connection).then(function (data) {
                if (data.data.userID) {
                    $rootScope.$broadcast("showToast", "Successfully saved");
                    $scope.list();
                    $scope.Connection = {};
                    $("#add_edit_connections").fadeOut(function () {
                        $("#div_list_connections").fadeIn()
                    })

                } else {
                    swal($$$("Error"), $$$("Not posted"), "error");

                }

            }).catch(function (data) {
            });
        };


        $scope.BackToConneciotns = function () {
            $("#pools").fadeOut(function () {
                $("#div_list_connections").fadeIn(function () {

                })
            })
        };

        $scope.Connections = [];
        $scope.list = function () {
            $http.get("/api/v1/companies/" + $scope.companyId + "/connections/").then(function (data) {
                $scope.Connections = data.data;
            })

        };
        $scope.list();

        $scope.add = function () {
            $scope.Connection = {};
            $("#div_list_connections").fadeOut(function () {
                $("#add_edit_connections").fadeIn()
            })
        };

        $scope.ConnectionPool = {};
        $scope.EnterToPools = function (item) {
            $scope.ConnectionPool = item;
            $scope.listPool();
            $("#div_list_connections").fadeOut(function () {
                $("#pools").fadeIn(function () {

                })
            })


        };

        $scope.sqlresult = [];
        $scope.sqlColNames = [];
        $scope.sqlCode = "";

        function getCols(data) {
            $scope.sqlColNames = [];
            if (data.length > 0) {
                return Object.keys(data[0]);
            }

        }

        $scope.isSqlExec = true;
        $scope.testTsql = function () {
            var enteredCode = $scope.editor1.getValue();
            $http.post("/api/v1/companies/" + $scope.companyId + "/connections/generateSql/", {
                // connection: $scope.ConnectionPool.id,
                commands: enteredCode
            }).then(function (data) {
                $scope.sqlresult = data.data;
                $scope.isSqlExec = false;
            }).catch(function (data) {
                $scope.sqlresult = data.data;
                $scope.isSqlExec = true;
            });

        };
        $scope.SqlTestResult = [];
        $scope.TestAllSqlCodes = function () {
            $http.post(
                "/api/v1/companies/" + $scope.companyId + "/connections/" + $scope.ConnectionPool.id + "/pools/test/", $scope.pool).then(function (data) {
                $scope.pool = data.data;

            }).catch(function (data) {
            })

        }
        $scope.runSqlResult = [];
        $scope.RunAllSqlCodes = function () {
            $http.post(
                "/api/v1/companies/" + $scope.companyId + "/connections/" + $scope.ConnectionPool.id + "/pools/runSql/", $scope.pool).then(function (data) {
                $scope.runSqlResult = data.data;
                // $scope.pool = data;

            }).catch(function (data) {
            })

        }


        $scope.finalresult = "";
        $scope.TestPool = function () {
            $http.post(
                "/api/v1/companies/" + $scope.companyId + "/connections/" + $scope.ConnectionPool.id + "/pools/run/", $scope.pool).then(function (data) {
                // $scope.runSqlResult = data;
                // $scope.pool = data;
                $scope.finalresult = JSON.stringify(JSON.stringify(data.data))
            }).catch(function (data) {
            })

        }



        // $scope.runSql = function () {
        //     var enteredCode = $scope.editor1.getValue();
        //     $http.post("/api/v1/companies/" + $scope.companyId + "/connections/runSql/", {
        //         connection: $scope.ConnectionPool.id,
        //         commands: enteredCode,
        //         variables: $scope.sqlresult
        //     }).then(function (data) {
        //         $scope.sql_final_render_result = data;
        //     }).catch(function (data) {
        //         $scope.sql_final_render_result = data;
        //     });
        // };

        $scope.pool = {};
        $scope.AddSqlCommand = function () {
            if (!($scope.pool.sqls)) {
                $scope.pool.sqls = []
            }
            $scope.pool.sqls.push({});
        };

        $scope.edit = function (item) {
            $scope.Connection = item;
            $("#div_list_connections").fadeOut(function () {
                $("#add_edit_connections").fadeIn()
            })
        };

        $scope.cancel = function () {
            $scope.Connection = {};
            $("#add_edit_connections").fadeOut(function () {
                $("#div_list_connections").fadeIn()
            })
        }

        $scope.test = function (item) {
            $http.post("/api/v1/companies/" + $scope.companyId + "/connections/testConnection/", item).then(function (data) {

                if (data.data.ok) {
                    swal($$$("Success"), $$$("Server is reachable"), "success")
                } else {
                    swal($$$("Error"), $$$("Server is not available"), "error")

                }
            }).catch(function () {
                swal($$$("Error"), $$$("Server is not available"), "error")

            });
        };


        $scope.editorOptions = {
            lineWrapping: true,
            lineNumbers: true,
            // readOnly: 'nocursor',
            mode: 'text/x-mssql'
        };
        $scope.editorOptionsPython = {
            lineWrapping: true,
            lineNumbers: true,
            // readOnly: 'nocursor',
            mode: 'python'
        };


        $scope.poolsList = {};
        $scope.listPool = function () {
            $http.get("/api/v1/companies/" + $scope.companyId + "/connections/" + $scope.ConnectionPool.id + "/pools/").then(function (data) {
                $scope.poolsList = data.data;
            })
        };

        $scope.PostPool = function () {
            $http.post("/api/v1/companies/" + $scope.companyId + "/connections/" + $scope.ConnectionPool.id + "/pools/", $scope.pool).then(function (data) {
                if (!(data.data.companyID)) {
                    swal("Error", "Check Debugger", "error");
                    return
                }
                $rootScope.$broadcast("showToast", $$$("successfully saved"));
                $scope.listPool();
                // $scope.pool = {};
                // $scope.showEdit = false;
            }).catch(function (data) {
                swal("Error", "Check Debugger", "error");
            })
        };


        $scope.EditPool = function (item) {
            $scope.showEdit = true;
            $scope.pool = item;
        }

        $scope.AddNewPool = function () {
            $scope.showEdit = true;
            $scope.pool = {};
        }

        $scope.RemovePool = function (item) {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary sql command!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false
            }, function () {
                $http.delete("/api/v1/companies/" + $scope.companyId + "/connections/" + $scope.ConnectionPool.id + "/pools/" + item.id + "/").then(function (data) {
                    swal("Deleted!", "Your imaginary file has been deleted.", "success");
                    $scope.listPool();
                }).catch(function (data) {
                    swal("Error", "Check Debugger", "error");
                })
            });
        }


        $scope.RemoveSqlCommand = function (index) {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary sql command!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false
            }, function () {
                $scope.pool.sqls.splice(index, 1);
                swal("Deleted!", "Your imaginary file has been deleted.", "success");
            });
        }


    });
