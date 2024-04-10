'use strict';
angular.module('AniTheme')
    .controller('CompanyChartCtrl', function ($scope, $http, $translate, $rootScope, $stateParams, $location, $modal, $element,
                                              companiesManagmentService, $$$) {


        $scope.ChartSimpleList = [];
        $scope.Zone = {};
        $scope.Zones = [];
        $scope.SelectedZones = [];
        $scope.SelectedChartID = 0;
        $scope.SecratraitsList = [];
        $scope.SelectedCompanyID = $stateParams.companyid;
        $scope.newChart = {};


        $scope.ModalRAWSwitch = function (tp) {
            if (tp == 1) {
                $("#divRAW").fadeOut(function () {
                    $("#divPersonel").fadeIn()
                })
            }
            if (tp == 2) {
                $("#divPersonel").fadeOut(function () {
                    $("#divRAW").fadeIn()
                })
            }
        }


        $scope.PositionsList = {};
        $scope.GetPositions = function () {
            $scope.isLoadingChartRow = true;
            $http.get("/api/v1/companies/" + $stateParams.companyid + "/members/getList/?q=" + $scope.positionListSearch).then(function (data) {
                $scope.PositionsList = data.data;
                $scope.isLoadingChartRow = false;
            }).catch(function () {
                $scope.isLoadingChartRow = false;
            })
        };


        $scope.OpenChartModalForChange = function (item) {
            $scope.isLoadingChartRow = true;
            $scope.selectedChartRAW = {
                id: item.chartID,
                title: item.chartName
            };
            $scope.currentSelectedChart = item;

            $http.get("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/GetAllChartsCurrentTopChart/?q=" + $scope.searchStringForRawModalTop + "&selectedID=0").then(function (data) {
                $scope.topChartListModalRAW = data.data;
                $('#modal_change_chart').modal('show');
                $scope.isLoadingChartRow = false;
            }).catch(function (data) {
                $scope.isLoadingChartRow = false;
            });

        }


        $scope.deletePosition = function (item, $index) {
            swal({
                title: "اخطار",
                text: "پس از حذف قابلیت برگشت وجود ندارد آیا اطمینان دارید ؟",
                type: "warning",
                showCancelButton: true,
                showLoaderOnConfirm: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: false
            }, function () {
                $http.delete("/api/v1/companies/" + $stateParams.companyid + "/positions/" + item.positionID + "/").then(function (data) {
                    if (data.data.msg) {
                        swal("حذف نشد !", data.data.msg, "error");
                    } else {
                        swal("حذف شد", "سمت مورد نظر حذف شد", "success");
                        $scope.PositionsList.splice($index, 1);
                    }
                }).catch(function (data) {
                })


            });
        }


        $scope.ShowPanel = function (pos) {

            if (pos === 1) {
                $scope.GetRawChart();
                $("#divRAWChart").addClass("show");
                $("#treeContainer").removeClass("show");
                $("#changeSemat").removeClass("show");
            }
            if (pos === 2) {
                $("#treeContainer").addClass("show");
                $("#divRAWChart").removeClass("show");
                $("#changeSemat").removeClass("show");
            }
            if (pos === 3) {
                $("#changeSemat").addClass("show");
                $("#treeContainer").removeClass("show");
                $("#divRAWChart").removeClass("show");
                $scope.GetPositions();
            }
        }

        $scope.PostNewChart = function () {
            $http.post("/api/v1/companies/" + $stateParams.companyid + "/chart/" + $scope.newChart.topID + "/AddNewChart/", {
                parentID: $scope.newChart.topID,
                name: $scope.newChart.name
            }).then(function (data) {
                $scope.GetRawChart();
            }).catch(function () {

            })
        }


        $scope.AddNewChart = function () {
            $scope.isLoadingChartRow = true;
            $http.get("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/GetAllChartsCurrentTopChart/?q=" + $scope.searchStringForRawModalTop + "&selectedID=0").then(function (data) {

                $scope.topChartListModalRAW = data.data;
                $("#modal_add_new_top").modal('show');
                $scope.isLoadingChartRow = false;
            }).catch(function (data) {
                $scope.isLoadingChartRow = false;
            });


        }


        $scope.DeleteChart = function (chartID) {


            swal({
                title: "اخطار",
                text: "پس از حذف قابلیت برگشت وجود ندارد آیا اطمینان دارید ؟",
                type: "warning",
                showCancelButton: true,
                showLoaderOnConfirm: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: false
            }, function () {
                $http.delete("/api/v1/companies/" + $stateParams.companyid + "/chart/" + chartID + "/").then(function (data) {
                    if (data.data.msg) {
                        swal("حذف نشد !", data.data.msg, "error");
                    } else {
                        swal("حذف شد", "سمت مورد نظر حذف شد", "success");
                        $scope.GetRawChart();
                    }
                }).catch(function (data) {
                })


            });
        }


        $scope.GetZoneList = function () {
            //
            companiesManagmentService.GetZones($scope.SelectedCompanyID, selectedItem.id).then(function (data) {
                $scope.Zones = data.data;
                // $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
            })
        };

        $scope.UpdatePerSec = function (item) {

            companiesManagmentService.UpdateSecPer($scope.SelectedCompanyID, $scope.SelectedChartID, item).then(function (data) {
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
            })
        }

        $scope.UpdatePerSecWithSelect = function (item, ii, index) {
            item.perm[index] = ii;
            $scope.UpdatePerSec(item);

        };


        $scope.receiverProfileID = "";


        $scope.positionListSearch = "";


        $scope.addPersonToPosition = function (item) {
            $http.post("/api/v1/companies/" + $stateParams.companyid + "/chart/AddToChart/", {
                selected: true,
                positionID: item.positionID,
                isEmpty: true,
                receiver: item.receiverProfileID,
                chart: $scope.SelectedChartID
            }).then(function (data) {
                if (typeof data.data == 'object') {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    $scope.GetProfileList($scope.SelectedChartID);
                } else {
                    swal("Error!", "این شخص قبلا سمت دهی شده است", "error");
                }

            }).catch(function (data) {

                swal("Error!", "این شخص قبلا سمت دهی شده است", "error");
            })
        }


        $scope.CheckOtherSecPer = function (item) {
            for (var i = 0; $scope.SecratraitsList.length > i; i++) {
                if (item.Id != $scope.SecratraitsList[i].Id) {
                    $scope.SecratraitsList[i].default = false;
                }
            }

            $scope.UpdatePerSec(item);


        };

        $scope.ForceOut = function (item) {


            swal({
                title: "آیا اطمینان دارید",
                text: "آیا از تعلیق این شخص اطمینان دارید ؟",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "بله",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                $scope.SelectedPerson = item;
                $http.post("/api/v1/companies/" + $stateParams.companyid + "/chart/0/ForceOut/", {
                    profileID: null,
                    chartID: $scope.SelectedChartID,
                    userID: item.userID,
                    positionID: item.positionID,
                    companyID: item.companyID
                }).then(function (data) {
                    $rootScope.$broadcast("UpdateProfiles");

                    // $scope.GetMembers($stateParams.companyid);
                    $scope.GetProfileList($scope.SelectedChartID);
                    swal($$$("Removed"), "کاربر مورد نظر تعلیق گردید", "success");

                });
            });
        };


        $scope.GetSecList = function (chartID) {
            companiesManagmentService.GetSecByChartPos($scope.SelectedCompanyID, chartID).then(function (data) {
                $scope.SecratraitsList = data.data;
            })
        };

        $scope.Positions = [];

        $scope.GetProfileList = function (chartID) {
            $scope.isLoadingChartRow = true;
            $scope.Positions = [];
            $scope.isLoadingChartRow = false;
            $http.get("/api/v1/members-search/" + chartID + "/getByChartID/").then(function (data) {
                $scope.Positions = data.data;
            }).catch(function () {
                $scope.isLoadingChartRow = false;
            })
        }


        $scope.currentSelectedRAWchart = {};
        $scope.searchStringForRawModalTop = "";
        $scope.selectedTopChartRAW = {};
        $scope.selectedChartRAW = {};
        $scope.topChartListModalRAW = [];
        $scope.NewChartRAW = "";
        $scope.NewChartRAWTitle = "";

        $scope.PostTopChartRAW = function (topChartRAWID) {
            $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/" + $scope.currentSelectedRAWchart.id + "/ChangeLevel/", {
                id: $scope.currentSelectedRAWchart.id,
                parentId: topChartRAWID
            }).then(function (data) {
                $scope.GetRawChart();

                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
            }).catch(function (data) {

            })
        }
        $scope.PostChartRAW = function (newChartID) {

            $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/positions/" + $scope.currentSelectedChart.positionID + "/ChangeChartID/", {
                newChartID: $scope.selectedChartRAW.id
            }).then(function (data) {
                $scope.GetPositions();
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
            }).catch(function (data) {

            })
        }
        $scope.PostRenameChartRAW = function () {
            $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/" + $scope.currentSelectedRAWchart.id + "/ChangeChartName/", {
                name: $scope.NewChartRAWTitle
            }).then(function (data) {
                $scope.GetRawChart();
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
            }).catch(function (data) {

            })
        };


        $scope.ChangeCell = function (item) {
            let a = prompt('موبایل جدید را وارد کنید مثلا : 09121234567');
            if (a) {
                $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/" + item.positionID + "/ChangeCell/", {
                    newCell: a
                }).then(function (data) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    $scope.GetPositions();
                })
            }
        }


        $scope.ChangeProfileName = function (item) {
            let a = prompt('نام مورد نظر را وارد نمایید : مثال : محمد علی صالحی');
            if (a) {
                $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/" + item.positionID + "/ChangeCell/", {
                    newCell: a
                }).then(function (data) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    $scope.GetPositions();
                })
            }
        }


        $scope.ChangePersCode = function (item) {
            let a = prompt('کد پرسنلی را وارد نمایید مثلا 1234');
            if (a) {
                $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/" + item.positionID + "/ChangePersCode/", {
                    newCell: a
                }).then(function (data) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    $scope.GetPositions();
                })
            }
        }


        $scope.PostRankChartRAW = function () {
            $http.post("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/" + $scope.currentSelectedRAWchart.id + "/ChangeChartRank/", {
                rank: $scope.NewChartRAWRank
            }).then(function (data) {
                $scope.GetRawChart();
                $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
            }).catch(function (data) {

            })
        };

        $scope.newUsername = "";
        $scope.selectedPosition = {};
        $scope.showSetUsername = function (item) {
            $scope.selectedPosition = item;
            $("#modal_set_user").modal('show');

        }

        $scope.addAUserToThisPost = function (item) {
            $http.post("/api/v1/companies/" + $stateParams.companyid + "/chart/addPersonToOldPosition/", {
                selectedPosition: $scope.selectedPosition.positionID,
                newUsername: $scope.newUsername
            }).then(function (data) {
                // debugger;
                if (typeof data.data == 'object') {
                    $scope.GetPositions();
                    $rootScope.$broadcast("UpdateProfiles");
                    $scope.GetProfileList($scope.SelectedChartID);
                    $rootScope.$broadcast("showToast", "با موفقيت ثبت شد");
                } else {
                    swal("Error!", "اين شخص قبلا سمت دهي شده است", "error");

                }
            }).catch(function (data) {
                swal("Error!", "اين شخص قبلا سمت دهي شده است", "error");

            })
        }


        $scope.ShowChangeTopModal = function (item) {
            $scope.isLoadingChartRow = true;
            $scope.selectedTopChartRAW = {
                id: item.topID,
                title: item.topTitle
            };
            $scope.currentSelectedRAWchart = item;
            $http.get("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/GetAllChartsCurrentTopChart/?q=" + $scope.searchStringForRawModalTop + "&selectedID=" + item.id).then(function (data) {
                $scope.topChartListModalRAW = data.data;
                $('#modal_change_top').modal('show');
                $scope.isLoadingChartRow = false;
            }).catch(function (data) {
                $scope.isLoadingChartRow = false;
            });
        };

        $scope.ShowChangeTitleModal = function (item) {
            $scope.NewChartRAWTitle = item.title;
            $scope.currentSelectedRAWchart = item;
            $("#modal_change_rename").modal('show');
        };

        $scope.ShowChangeRankModal = function (item) {
            $scope.NewChartRAWTitle = item.title;
            $scope.NewChartRAWRank = item.rank;
            $scope.currentSelectedRAWchart = item;
            $("#modal_change_rank").modal('show');
        };


        $scope.ShowRAWDabirkhanehModal = function (item) {
            $scope.isLoadingChartRow = true;
            $scope.SelectedChartID = item.id;
            $scope.GetSecList(item.id)

            $scope.isLoadingChartRow = false;
            $scope.currentSelectedRAWchart = item;
            $("#modal_access_dabir").modal('show');


        }

        $scope.ShowRAWPositionsInChartModal = function (item) {

            $scope.SelectedChartID = item.id;
            $scope.currentSelectedRAWchart = item;
            $scope.GetProfileList(item.id);
            $("#modal_preview_positions").modal("show");

        }

        $scope.clearsearchStringForRawModalTop = function () {
            $scope.searchStringForRawModalTop = '';
        };
        $element.find('input').on('keydown', function (ev) {
            ev.stopPropagation();
        });


        $scope.rawChartSearch = "";
        $scope.rawCharts = [];
        $scope.isLoadingChartRow = false;

        $scope.GetRawChart = function () {
            $scope.isLoadingChartRow = true;
            $http.get("/api/v1/companies/" + $scope.SelectedCompanyID + "/chart/GetAllChartsCurrent/?q=" + $scope.rawChartSearch).then(function (data) {
                $scope.rawCharts = data.data;
                $scope.isLoadingChartRow = false;

            }).catch(function () {
                $scope.isLoadingChartRow = false;

            })
        };
        $scope.GetRawChart();
        $scope.OpenCompanyChart = function (item) {
            $scope.SelectedCompanyID = item;
            companiesManagmentService.GetChart(item);
            companiesManagmentService.GetZones($scope.SelectedCompanyID, "0").then(function (data) {
                $scope.Zones = data.data;
                // $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
            })


        };
        $scope.GetCompanyChartList = function (companyID) {
            companiesManagmentService.GetCompanyChartList(companyID).then(function (data) {
                $scope.ChartSimpleList = data.data;
            });
        };
        $scope.OpenCompanyChart($stateParams.companyid);
        $scope.NewZone = function () {

            swal({
                    title: "New Zone",
                    text: "Enter your new zone name",
                    type: "input",
                    showCancelButton: true,
                    closeOnConfirm: false,
                    animation: "slide-from-top",
                    inputPlaceholder: "Write Zone Name"
                },
                function (inputValue) {
                    if (inputValue === false)
                        return false;
                    if (inputValue === "") {
                        swal.showInputError("Zone name is require");
                        return false
                    }
                    $scope.Zone.title = inputValue;
                    $scope.Zone.company = $scope.SelectedCompanyID.toString();
                    companiesManagmentService.PostZone($scope.SelectedCompanyID, $scope.Zone).then(
                        function (data) {
                            $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                            $scope.GetZoneList();
                            swal(
                                "Nice!",
                                "" + data.data.name + " added !",
                                "success");
                        }
                    ).catch(
                        function (err) {
                            swal.showInputError(err.name[0]);
                        }
                    )

                });
        };

        $scope.DeleteZone = function (zone, index) {
            swal({
                title: "Are you sure?",
                text: "You will not be able to recover this imaginary file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {
                companiesManagmentService.DeleteZone($scope.SelectedCompanyID, zone.selectedChartID, zone.id).then(function (data) {
                    $scope.Zones.results.splice(index, 1);
                    swal("Deleted!", "Your imaginary file has been deleted.", "success");
                }).catch(function (data) {

                });


            });
        };

        $scope.ChangeZonesChart = function (zone) {
            //
            zone.selectedChartID = selectedItem.id;
            companiesManagmentService.ChangeZone(zone.selectedChartID, zone).then(function (data) {

            });
        };


        $scope.EditZone = function (zone, index) {
            swal({
                title: "An input!",
                text: "Write something interesting:",
                type: "input",
                inputValue: zone.title,
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: "Write something"
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {

                    swal.showInputError("You need to write something!");
                    return false
                }
                zone.title = inputValue;
                companiesManagmentService.EditZone($scope.SelectedCompanyID, zone).then(function (data) {
                    $rootScope.$broadcast("showToast", "با موفقیت ثبت شد");
                    swal("Nice!", "You wrote: " + inputValue, "success");

                });
            });
        };

    });
