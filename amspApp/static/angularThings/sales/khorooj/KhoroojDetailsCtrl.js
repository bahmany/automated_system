'use strict';
angular.module('AniTheme')
    .controller(
        'KhoroojDetailsCtrl',
        function ($scope, $window, $http,
                  $translate, $rootScope, $state,
                  $stateParams, $location, $$$,
                  $filter, Upload, $mdDialog) {


            $scope.details = {};
            $scope.headerDet = {};
            $scope.Files = {};

            $scope.sign1 = {};
            $scope.sign2 = {};
            $scope.sign3 = {};
            $scope.sign4 = {};
            // $scope.hasStep = function (stepNum) {
            //     for (var i = 0; $scope.signs.length > i; i++) {
            //         if ($scope.signs[i].whichStep == stepNum) {
            //             $scope["sign" + i.toString()] = $scope.signs[i];
            //             return true
            //         }
            //     }
            // }

            $scope.showSMSNoFound = false;
            $scope.showProfileNotFound = false;

            $scope.makeqrcode = function (signID) {
                // return "http://app.****.ir/qr/3_" + signID + "/"
                return "http://app.******.com/qr/2_" + signID + "/"
            }

            $scope.checkPath = function (base, path) {
                try {
                    var current = base;
                    var components = path.split(".");
                    for (var i = 0; i < components.length; i++) {
                        if ((typeof current !== "object") || (!current.hasOwnProperty(components[i]))) {
                            return false;
                        }
                        current = current[components[i]];
                    }
                    return true;
                } catch (e) {
                    return false

                }

            }

            $scope.gotoprev = function () {
                $http.get('/api/v1/hamkaranKhorooj/' + $stateParams.khid + '/gotoprev/').then(function (data) {
                    if (data.data.id !== "") {
                        $state.go("KhoroojDetails", {"khid": data.data.id});

                    }
                })
            }
            $scope.gotonext = function () {
                $http.get('/api/v1/hamkaranKhorooj/' + $stateParams.khid + '/gotonext/').then(function (data) {
                    if (data.data.id !== "") {
                        $state.go("KhoroojDetails", {"khid": data.data.id});

                    }
                })
            }

            $scope.checkIfSMSNo = function () {

                if (!($scope.headerDet)) {
                    $scope.showSMSNoFound = true;
                    return
                }

                if (!($scope.headerDet.profile)) {
                    $scope.showSMSNoFound = true;
                    return
                }

                if (!($scope.headerDet.profile.exp)) {
                    $scope.showSMSNoFound = true;
                    return
                }

                if (!($scope.headerDet.profile.exp.contact)) {
                    $scope.showSMSNoFound = true;
                    return
                }

                if (!($scope.headerDet.profile.exp.contact.cell)) {
                    $scope.showSMSNoFound = true;
                    return
                }

                if ($scope.headerDet.profile.exp.contact.cell === '') {
                    $scope.showSMSNoFound = true;
                    return
                }

                $scope.showSMSNoFound = false

            }

            $scope.checkIfProfile = function () {

                if (!($scope.headerDet)) {
                    $scope.showProfileNotFound = true;
                    return
                }

                if (!($scope.headerDet.profile)) {
                    $scope.showProfileNotFound = true;
                    return
                }
                $scope.showProfileNotFound = false
            }


            $scope.addToProfile = function () {
                var cellNo = prompt("شماره موبایل مشتری مورد را وارد نمایید", "")
                if (cellNo) {
                    $http.post("/api/v1/salesProfile/", {
                        name: $scope.headerDet.item.CntrprtTitle,
                        hamkaranCode: $scope.headerDet.item.DLRef,
                        exp: {
                            contact: {
                                cell: cellNo,
                                name: "ناشناس"
                            }
                        }
                    }).then(function (data) {
                        if (data.id) {
                            $scope.getDetails();

                        }
                    })
                }

            }
            $scope.updateToProfile = function () {
                debugger;
                var cellNo = prompt("شماره موبایل مشتری مورد را وارد نمایید", "");
                if (cellNo) {
                    $http.patch("/api/v1/salesProfile/" + $scope.headerDet.profile.id + "/", {
                        exp: {
                            contact: {
                                cell: cellNo,
                                name: "ناشناس"
                            }
                        }
                    }).then(function (data) {
                        if (data.id) {
                            $scope.getDetails();

                        }
                    })
                }

            }


            $scope.makeItBatel = function () {
                let reason = prompt("دلیل ابطال را وارد نمایید");


                if (reason !== "" && reason !== undefined) {
                    $http.post('/api/v1/exits/' + $stateParams.khid + '/makeItBatel/', {reason:reason}).then(function (data) {
                        if (data.data['msg'] === "ok") {
                            $state.go('Khorooj');
                        }
                    })
                }
            }


            $scope.getDetails = function () {
                $http.get('/api/v1/hamkaranKhorooj/' + $stateParams.khid + '/').then(function (data) {
                    $scope.headerDet = data.data;
                    $scope.checkIfSMSNo();
                    $scope.checkIfProfile();
                });

                // $http.get('/api/v1/hamkaranKhorooj/' + $stateParams.khid + '/getDetailBarnamehSigns/').then(function (data) {
                //     $scope.signs = data.data;
                // });
                //
                //
                // $http.get('/api/v1/hamkaranKhorooj/' + $stateParams.khid + '/getDetailBarnameh/').then(function (data) {
                //     $scope.details = data.data;
                //     if ($scope.details === {}) {
                //         return
                //     }
                //     // $scope.headerDet = data.data[0];
                //
                //     // getting total
                //     var sumOf = 0;
                //     for (var i = 0; $scope.details.length > i; i++) {
                //         // sumOf += $scope.details[i].item.ItmQty
                //     }
                //     if ($scope.headerDet.item) {
                //         $scope.headerDet.item.sumOf = sumOf;
                //
                //     }
                //     //
                //
                    $http.get('/api/v1/hamkaranKhorooj/' + $stateParams.khid + '/getFiles/').then(function (data) {
                        $scope.Files = data.data.Files;
                        // if ($scope.sms) {
                        //     if ($scope.sms.mobile) {
                        //         $scope.sms.mobile = $scope.headerDet.item.Mobile
                        //     }
                        // }
                    });
                // });


                // $scope.hasStep
            };

            $scope.getDetails();

            $scope.sms = {};
            $scope.sendSms = function () {

                $http.post('/api/v1/hamkaranKhorooj/sendSms/', {
                    id: $scope.headerDet.id
                }).then(function (data) {
                    $scope.getSMSList();
                })
            }

            $scope.signs = [];


            $scope.customFullscreen = false;

            $scope.showAdvanced = function (stepID, ev) {
                $mdDialog.show({
                    locals: {
                        dataToSend: {
                            exitID: $stateParams.khid,
                            stepID: stepID,
                            signType: 1,
                            httppost: '/api/v1/hamkaranKhorooj/signExit/',
                            id: $scope.headerDet.id
                        }
                    },
                    controller: signBodyCtrl,
                    templateUrl: '/page/showSignBodyPrc/',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    onComplete: function (s, e) {
                        $(e).find('input').first().focus()
                    },
                    clickOutsideToClose: true,
                    fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
                })
                    .then(function (answer) {
                        $scope.getDetails();

                        // $http.get('/api/v1/hamkaranKhorooj/' + $stateParams.khid + '/getDetailBarnamehSigns/').then(function (data) {
                        //     $scope.signs = data.data;
                        //     $scope._signs = $scope.signs[$scope.signs.length - 1];
                        //
                        //     if ($scope._signs) {
                        //         if ($scope._signs.whichStep === 5) {
                        //             $scope.sms = {
                        //                 mobile: $scope.headerDet.profile.exp.contact.cell
                        //             }
                        //             $scope.sendSms();
                        //         }
                        //     }
                        // })

                    }, function () {
                        $scope.status = 'You cancelled the dialog.';
                    });
            };


            $scope.sign = function (stepNum, ev) {
                $scope.showAdvanced(stepNum, ev);
            };

            $scope.smss = [];
            $scope.getSMSList = function () {
                $http.get('/api/v1/hamkaranKhorooj/' + $stateParams.khid + '/getSMS/').then(function (data) {
                    $scope.smss = data.data;
                });
            }
            $scope.getSMSList();

            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
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
                return ;

                var confirm = $mdDialog.confirm()
                    .title('حذف فایل')
                    .textContent('فایل مورد نظر حذف شود ؟')
                    .ariaLabel('حذف فایل')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {

                    $scope.Files.uploaded.splice(index, 1);
                    $http.post("/api/v1/hamkaranKhorooj/" + $stateParams.khid + "/saveFiles/", {
                        Files: {
                            uploaded: $scope.Files.uploaded
                        }
                    }).then(function () {

                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });


            }
            $scope.saveFiles = function () {
                var final = [];
                angular.forEach($scope.UploadedFiles, function (value, key) {
                    final.push(value);
                });
                final = angular.copy($scope.UploadedFiles);
                if ($scope.Files) {
                    if ($scope.Files.uploaded) {
                        for (var i = 0; $scope.Files.uploaded.length > i; i++) {
                            final.push($scope.Files.uploaded[i]);
                        }
                    }
                }

                $http.post("/api/v1/hamkaranKhorooj/" + $stateParams.khid + '/saveFiles/', {
                    Files: {
                        uploaded: final,
                    },
                    id: $scope.headerDet.id
                }).then(function () {
                    $scope.Files = {};
                    $scope.Files.uploaded = final;
                    $scope.UploadedFiles = [];
                    $("#divUploader").fadeOut(function () {
                        $("#divFiles").fadeIn();
                    });
                })
            };
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------

            $("#div_main_container").scroll(function () {
                var hT = $('#div_main_container').offset().top,
                    hH = $('#div_main_container').outerHeight(),
                    wH = $(window).height(),
                    wS = $(this).scrollTop();
                // console.log(hT);
                // console.log(hH);
                // console.log(wH);
                // console.log(wS);

                if (wS > (hT + hH - wH)) {
                    // console.log('H1 on the view!');
                }

            });


        });


