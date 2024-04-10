'use strict';
angular.module('AniTheme')
    .controller(
        'OldHavalehForooshDetailsCtrl',
        function ($scope, $window, $mdMenu, $http, $translate, $mdDialog, $state,
                  $rootScope, $stateParams, $location, $$$, $filter) {

            $scope.havaleh = {};
            $scope.firstData = {};

            $scope.get = function () {
                $http.get("/api/v1/havakehForooshOld/" + $stateParams.hfdid + "/getDetails/").then(function (data) {

                    $scope.havaleh = data.data;
                    $scope.firstData = data.data[0];
                    $scope.firstData.desc = data.data[0].item.items[0];

                });

            };

            $scope.get();


            $scope.handleprint = function (approve) {

            }


            $scope.next_rec = function () {
                $http.get("/api/v1/havakehForooshOld/" + $stateParams.hfdid + "/nextRecord/").then(function (data) {
                    if (data.data.id !== "") {
                        $state.go("OldHavalehForooshDetails", {"hfdid": data.data.id});

                    }
                })
            }
            $scope.prev_rec = function () {
                $http.get("/api/v1/havakehForooshOld/" + $stateParams.hfdid + "/prevRecord/").then(function (data) {
                    if (data.data.id !== "") {
                        $state.go("OldHavalehForooshDetails", {"hfdid": data.data.id});

                    }
                })
            }


            $scope.waitForAppr = false;

            $scope.proveByTolid = function (convItem, event) {
                $scope.waitForAppr = true;
                $http.post("/api/v1/havakehForooshOld/proveTolid/", convItem).then(function (data) {
                    convItem.exp = data.data.exp;
                    $scope.waitForAppr = false;
                }).catch(function (e) {
                    $scope.waitForAppr = false;
                })
            }


            $scope.changeTarikheTahvil = function (approve, item) {
                var b = prompt("لطفا تاریخ مورد نظر را وارد نمایید مثال ۱۳۹۸/۰۲/۰۹", item.tarikheTahvil)

                if (b) {
                    $http.post("/api/v1/havakehForooshOld/changesayer/", {
                        item: item,
                        approve: approve
                    }).then(function (data) {

                    })

                    item.tarikheTahvil = b;
                }
            }

            $scope.tolidBelaApply = function (approve, what) {
                $http.post("/api/v1/havakehForooshOld/tolidBelaApply/", {
                    item: what,
                    approve: approve
                }).then(function (data) {
                    if (data.data.type === "err") {
                        alert("شما مجوز تغییر ندارید")
                    }
                })
            }
            $scope.khroojBelaApply = function (approve, what) {
                $http.post("/api/v1/havakehForooshOld/khroojBelaApply/", {
                    item: what,
                    approve: approve
                }).then(function (data) {
                    if (data.data.type === "err") {
                        alert("شما مجوز تغییر ندارید")
                    }
                })
            }

            $scope.ersaleFactorApply = function (approve, what) {
                $http.post("/api/v1/havakehForooshOld/ersaleFactorApply/", {
                    item: what,
                    approve: approve
                }).then(function (data) {
                    if (data.data.type === "err") {
                        alert("شما مجوز تغییر ندارید")
                    }
                })
            }


            $scope.changeKarbod = function (approve, item) {
                var b = prompt("لطفا کاربرد مصرفی مشتری را وارد نمایید", item.karbord)

                if (b) {
                    $http.post("/api/v1/havakehForooshOld/changekarbord/", {
                        item: item,
                        approve: approve
                    }).then(function (data) {

                    })

                    item.karbord = b;
                }
            }

            $scope.changeKarbod = function (approve, item) {
                var b = prompt("لطفا کاربرد مصرفی مشتری را وارد نمایید", item.karbord)

                if (b) {
                    $http.post("/api/v1/havakehForooshOld/changekarbord/", {
                        item: item,
                        approve: approve
                    }).then(function (data) {

                    })

                    item.karbord = b;
                }
            }


            $scope.changeHavaleh = function (approve, signID, ev) {
                $state.go("OldHavalehForooshChange", {ApproveID: approve.id, Step: signID});
            };


            $scope.printIt = function () {
                var cdd = jQuery("html").html();
                $http.post("/api/v1/havakehForooshOld/sendAutomated_tolid/", {dt: cdd});
            }


            $scope.sign = function (approve, stepNum, ev) {
                $scope.showAdvanced(approve, stepNum, ev);
            };


            $scope.makeqrcode = function (signID) {
                return "http://app.****.ir/qr/3_" + signID + "/"
                // return "http://127.0.0.1:8000/qr/3_" + signID + "/"
            }


            $scope.showAdvanced = function (approve, stepID, ev) {
                var hid = $stateParams.khid;
                $mdDialog.show({
                    locals: {
                        dataToSend: {
                            stepID: stepID,
                            signType: 1,
                            httppost: '/api/v1/havakehForooshOld/signHavaleh/',
                            VchHdrId: approve.id
                        }
                    },
                    onComplete: function (s, e) {
                        $(e).find('input').first().focus()
                    },
                    controller: signBodyCtrl,
                    templateUrl: '/page/showSignBodyPrc/',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true,
                    fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
                })
                    .then(function (answer) {

                        $http.get('/api/v1/havakehForooshOld/' + approve.id + '/getDetailBarnamehSigns/').then(function (data) {
                            approve.signs = data.data;
                            // approve.signs.push(data.data);

                            if ($scope._signs) {
                                if ($scope._signs.whichStep === 5) {
                                    $scope.sms = {
                                        mobile: $scope.headerDet.profile.exp.contact.cell
                                    }
                                    // $scope.sendSms();
                                }
                            }
                        })

                    }, function () {
                        $scope.status = 'You cancelled the dialog.';
                    });
            };


            var publicEditorOptions = {
                language: 'fa',
                toolbar: [
                    {
                        name: 'document',
                        items: ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates']
                    },
                    {
                        name: 'clipboard',
                        items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']
                    },
                    {name: 'editing', items: ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt']},
                    {
                        name: 'forms',
                        items: ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                            'HiddenField']
                    },
                    '/',
                    {
                        name: 'basicstyles',
                        items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']
                    },
                    {
                        name: 'paragraph',
                        items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                            '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']
                    },
                    {name: 'links', items: ['Link', 'Unlink', 'Anchor']},
                    {
                        name: 'insert',
                        items: ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']
                    },
                    '/',
                    {name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize']},
                    {name: 'colors', items: ['TextColor', 'BGColor']},
                    {name: 'tools', items: ['Maximize', 'ShowBlocks', '-', 'About']}

                ],
                extraPlugins: 'lineutils,notification,uploadwidget,uploadimage',
                removePlugins: 'sourcearea',
                filebrowserUploadUrl: '/api/v1/file/upload',
                resize_maxHeight: 900,
                height: 600

            };
            $scope.publicEditorOptions = publicEditorOptions;


            $scope.addNewConv = function (approve, ev) {
                $mdDialog.show({
                    controller: AddNewConvController,
                    templateUrl: 'addNewConv.tmpl.html',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    locals: {
                        approve: approve

                    },
                    clickOutsideToClose: true
                })
                    .then(function (answer) {

                        $scope.listConv();

                        $scope.status = 'You said the information was "' + answer + '".';
                    }, function () {
                        $scope.status = 'You cancelled the dialog.';
                    });
            };

            $scope.waitForAppr = false;
            $scope.weProduceIt = function (approve, $event) {
                $scope.waitForAppr = true;
                $http.post("/api/v1/havakehForooshConvOld/weProduceIt/", {
                    "approve": approve
                }).then(function (data) {
                    $scope.waitForAppr = false;
                    approve.convs.push(data.data);

                }).catch(function () {
                    $scope.waitForAppr = false;
                })
            }
            $scope.readyToSend = function (approve, $event) {
                $scope.waitForAppr = true;
                $http.post("/api/v1/havakehForooshConvOld/readyToSend/", {
                    "approve": approve
                }).then(function (data) {
                    $scope.waitForAppr = false;
                    approve.convs.push(data.data);

                }).catch(function () {
                    $scope.waitForAppr = false;
                })
            }

            $scope.showPrerenderedDialog = function (ev) {
                $mdDialog.show({
                    contentElement: '#myDialog',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true
                });
            };

            function AddNewConvController($scope, $mdDialog, $stateParams, approve) {
                $scope.hide = function () {
                    $mdDialog.hide();
                };

                $scope.cancel = function () {
                    $mdDialog.cancel();
                };

                $scope.answer = function (answer) {
                    $mdDialog.hide(answer);
                };

                $scope.isPosting = false;

                $scope.postConv = function () {
                    $scope.isPosting = true;
                    $scope.conv.HavalehForooshApproveLink = approve.id;
                    if ($scope.conv.id) {
                        $http.patch("/api/v1/havakehForooshConvOld/" + approve.id + "/", $scope.conv).then(function (data) {

                            $scope.conv = {};
                            $mdDialog.hide();
                            $scope.isPosting = false;
                        }).catch(function () {
                            $scope.isPosting = false;
                        })

                    } else {

                        $http.post("/api/v1/havakehForooshConvOld/", $scope.conv).then(function (data) {
                            // $("#addConv").fadeOut(function () {
                            //     $("#convTimeLine").fadeIn();
                            // });
                            $scope.conv = {};
                            approve.convs.push(data.data);
                            $mdDialog.hide();
                            $scope.isPosting = false;
                        }).catch(function () {
                            $scope.isPosting = false;

                        })

                    }
                };
            }


            $scope.isThisApproveFinishedTotaly = function () {
                $http.get("/api/v1/havakehForooshOld/" + $stateParams.hfdid + "/isThisApproveFinishedTotaly/").then(function (data) {
                    if (data.data.result === true) {
                        $scope.thisHavalehHasFinished = true;
                    } else {
                        $scope.thisHavalehHasFinished = false;

                    }
                })
            };
            $scope.isThisApproveFinishedTotaly();

            $scope.startNewActivity = function () {
                $http.get("/api/v1/havakehForooshOld/" + $stateParams.hfdid + "/startFromRemaining/").then(function (data) {
                    $scope.get();
                    $scope.isThisApproveFinishedTotaly();
                })
            }


            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            $scope.conv = {};
            $scope.Convs = {};
            $scope.listConv = function () {
                return
                $http.get("/api/v1/havakehForooshConvOld/?convID=" + $stateParams.hfdid).then(function (data) {
                    $scope.Convs = data.data;
                    $(".timeline-content").find("img").css({"width": "100%", "height": "100%"})
                })
            };
            $scope.listConv();
            $scope.editConv = function (item) {
                $("#convTimeLine").fadeOut(function () {
                    $("#addConv").fadeIn();
                });
                $scope.conv = item;
            };
            $scope.cancelConv = function () {
                $scope.conv = {};
            };
            $scope.deleteConv = function (ev, conv) {
                var confirm = $mdDialog.confirm()
                    .title('حذف نظر')
                    .textContent('نظر مورد نظر حذف شود ؟')
                    .ariaLabel('حذف نظر')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {
                    $http.delete("/api/v1/havakehForooshConvOld/" + conv.id + "/").then(function () {
                        $scope.listConv();
                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });

            };
            $scope.listReplays = function (item) {
                $http.get("/api/v1/havakehForooshConvOld/" + item.havalehForooshLink + "/getReplays/").then(function (data) {
                    item.replays = data.data;
                    $(".timeline-content").find("img").css({"width": "100%", "height": "100%"})
                })
            }
            $scope.removeReplay = function (parentItem, item, ev) {

                var confirm = $mdDialog.confirm()
                    .title('حذف نظر')
                    .textContent('نظر مورد نظر حذف شود ؟')
                    .ariaLabel('حذف نظر')
                    .targetEvent(ev)
                    .ok('حذف شود')
                    .cancel('انصراف');
                $mdDialog.show(confirm).then(function (result) {
                    $http.get("/api/v1/havakehForooshConvOld/removeReplay/?replayID=" + item.id).then(function () {
                        $scope.listReplays(parentItem);
                    })
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });
            }
            $scope.replayConv = function (ev, conv) {

                // Appending dialog to document.body to cover sidenav in docs app
                var confirm = $mdDialog.prompt()
                    .title('نظر شما')
                    .textContent('نظر خود را وارد نمایید')
                    .placeholder('نظر')
                    .ariaLabel('نظر')
                    .initialValue('')
                    .targetEvent(ev)
                    .ok('تایید')
                    .cancel('انصراف');

                $mdDialog.show(confirm).then(function (result) {
                    $http.post("/api/v1/havakehForooshConvOld/" + $stateParams.hfdid + "/AddToReplay/", {
                        comment: result.data
                    }).then(function (data) {
                        $scope.listReplays(conv)

                    })

                    $scope.status = 'You decided to name your dog ' + result.data + '.';
                }, function () {
                    $scope.status = 'You didn\'t name your dog.';
                });


            }


            //Get the button
            var mybutton = document.getElementById("back_btn_static");

// When the user scrolls down 20px from the top of the document, show the button
            window.onscroll = function () {
                scrollFunction()
            };

            function scrollFunction() {
                if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                    mybutton.style.display = "block";
                } else {
                    mybutton.style.display = "none";
                }
            }

// When the user clicks on the button, scroll to the top of the document
            function topFunction() {
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
            }


            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------
            //------------------------------------------------------------------------------------


        });

setTimeout(function () {
    $(".timeline-content").find("img").css({"width": "100%", "height": "100%"});
}, 5000);
setTimeout(function () {
    $(".timeline-content").find("img").css({"width": "100%", "height": "100%"});
}, 15000);
setTimeout(function () {
    $(".timeline-content").find("img").css({"width": "100%", "height": "100%"});
}, 25000);

