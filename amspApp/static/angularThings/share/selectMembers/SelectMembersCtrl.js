angular.module('AniTheme').controller(
    'SelectMembersCtrl',
    function ($scope,
              $translate,
              $timeout,
              $q,
              $mdToast,
              $rootScope,
              $http,
              $stateParams,
              SelectMembersService) {
        $scope.ComplexSearchResult = {};
        $scope.SentToSearchText = "";
        $scope.Selected = {};
        $scope.Selected.data = [];
        $scope.ComplexSearchResult.filter = [
            {'v': true, 'd': 1},
            {'v': true, 'd': 2},
            {'v': true, 'd': 3},
            {'v': true, 'd': 4}];
        $scope.GetDetail = function (item) {
            if (item.type == 1) {
                $http.get("/api/v1/inboxGroups/" + item.id + "/GetGroupMember/").then(function (data) {
                    item.members = data.data.members;
                });
            }
            if (item.type == 3) {
                $http.get("/api/v1/companies/" + $stateParams.companyid + "/members/GetChartPositionList/?id=" + item.id).then(function (data) {
                    item.members = data.data;
                });
            }
            if (item.type == 4) {
                $http.get("/api/v1/companies/" + $stateParams.companyid + "/chart-zone/GetZoneMembers/?id=" + item.id).then(function (data) {
                    item.members = data.data;
                });
            }

        };
        $scope.ChangeFilter = function (itemID) {
            angular.forEach($scope.ComplexSearchResult.filter, function (value, key) {
                if (value.d == itemID) {
                    value.v = !value.v;
                }
            });
            //item.v = !item.v;

            $scope.GetAllComplex($scope.SentToSearchText);

        };

        $scope.ShowFilterBtn = function (items, itemID) {
            var output = "hide";
            angular.forEach(items, function (value, key) {
                //debugger;
                if (value.d == itemID) {
                    if (value.v == true) {
                        output = "font-make-green";
                    } else {
                        output = "font-make-white";
                    }
                }
            })

            return output;
        }
        $scope.GetFilterClass = function (filterObj, item) {
            for (var i = 0; filterObj.length > i; i++) {
                if (filterObj[i]["_" + item.toString()]) {
                    return filterObj[i]["_" + item.toString()]
                }
            }
            return false
        };
        $scope.RemoveFromSelected = function (index, members) {
            members.splice(index, 1);
        }
        $scope.GetAllComplex = function (q) {
            var rq = {
                q: q,
                f: $scope.ComplexSearchResult.filter
            };
            //$scope.ComplexSearchResult.filter = {};
            $http.post("search/company/complex-members/", rq).then(function (data) {
                $scope.ComplexSearchResult = data.data;
            })
        };
        $scope.$watch("SentToSearchText", function () {
            $scope.GetAllComplex($scope.SentToSearchText);

        });
        $scope.AddToSelected = function (item) {
            for (var i = 0; $scope.Selected.data.length > i; i++) {
                if ($scope.Selected.data[i].id === item.id) {
                    return
                }
            }
            $scope.GetDetail(item);
            $scope.Selected.data.push(item)
        };
        $scope.showPerRecDetails = function (event) {
            $(event.target).parent().find(".send-detail-per-rec").toggleClass("hide");
        };

        $scope.SelOptionItem = {};


        $scope.RefereshRecCache = function () {
            $http.get("search/company/complex-members/?fg=true").then(function (data) {
                if (data.data["ok"]) {
                    $scope.GetAllComplex($scope.SentToSearchText);
                }

            })
        }

        $scope.PostSelected = function () {

            // 1 = send to reciever of a letter and add it to the draft
            // 2 = forwarding group of letter
            // 3 = forwarding a letter
            // 4 = publish bpmn to list
            // 5 = forwarding a letter and archive
            // 6 = forwarding group of letter and archive


            var defer = $q.defer();
            var ds = {};
            ds.desc = {};
            ds.thisListIsFor = $scope.Prop.thisListIsFor;
            ds.desc = $scope.Prop;
            ds.items = $scope.Selected.data;

            function sanitizePosition() {
                var current = ctrl.toastPosition;

                if (current.bottom && last.top) {
                    current.top = false;
                }
                if (current.top && last.bottom) {
                    current.bottom = false;
                }
                if (current.right && last.left) {
                    current.left = false;
                }
                if (current.left && last.right) {
                    current.right = false;
                }

                last = angular.extend({}, current);
            }

            var pinTo = $scope.getToastPosition();
            if (ds.thisListIsFor == 3 || ds.thisListIsFor == 2 || ds.thisListIsFor == 5 || ds.thisListIsFor == 6) {
                $mdToast.show(
                    $mdToast.simple()
                        .textContent('نامه های شما در حال ارجاع است. لطفا صبر کنید...')
                        .position(pinTo)
                        .hideDelay(3000));

                // $(".please-wait").fadeIn(100);
                // $(".wait-layer-msg").text("نامه های شما در حال ارجاع است. لطفا صبر کنید...").css("color", "honeydew");
            }


            var res = $http.post("/api/v1/select/members/", ds);
            res.then(function (data) {
                // $rootScope.GetIntimeNotification();
                if (ds.thisListIsFor == 3 || ds.thisListIsFor == 2 || ds.thisListIsFor == 5 || ds.thisListIsFor == 6) {
                    $rootScope.$broadcast("callInboxItems");
                    $mdToast.show(
                        $mdToast.simple()
                            .textContent("نامه یا نامه های شما ارجاع شد")
                            .position(pinTo)
                            .hideDelay(3000));

                    // $(".please-wait").fadeIn(100);
                    // $(".wait-layer-msg").text("نامه یا نامه های شما ارجاع شد").css("color", "#04FF00");

                }

                $timeout(function () {
                    $(".please-wait").fadeOut(100);
                }, 2000);

                $rootScope.$broadcast("showToast", "Selected letter successfully sent");
                $scope.CancelSelect();
                $rootScope.$broadcast("UpdateRecievers", data.data);
                return defer.resolve(res);

            }).catch(function () {

                if (ds.thisListIsFor == 3 || ds.thisListIsFor == 2 || ds.thisListIsFor == 5 || ds.thisListIsFor == 6) {
                    $mdToast.show(
                        $mdToast.simple()
                            .textContent("نامه های شما ارجاع نشد - لطفا دادهای ورودی را کنترل نمایید")
                            .position(pinTo)
                            .hideDelay(3000));

                    // $(".please-wait").fadeIn(100);
                    // $(".wait-layer-msg").text("نامه های شما ارجاع نشد - لطفا دادهای ورودی را کنترل نمایید").css("color", "FF7858");
                }


                $timeout(function () {
                    $(".please-wait").fadeOut(100);
                }, 2000);
                return defer.reject("");
            });
            return defer.promise;
        };
        $scope.CancelSelect = function () {
            $("#" + $scope.Prop.currDivName).fadeOut(function () {
                $("#" + $scope.Prop.prevDivName).fadeIn();
            });
        };
        $scope.SelectAllMember = function () {
            $http.get("search/company/complex-members").then(function (data) {
                $scope.Selected.data = data.data;
            })
        };
        $scope.$on("CallMembers", function (event, args) {
            //////console.log(args);
            $http.get("/api/v1/select/members/" + args + "/").then(function (data) {
                //ds.thisListIsFor = $scope.Prop.thisListIsFor;
                //ds.desc = $scope.Prop;
                //ds.items = $scope.Selected.data;
                $scope.Prop = data.data.desc;
                $scope.Selected.data = data.data.items
            })
        });

        $scope.hamesh_history = [];
        $scope.getPreviousHamesh = function () {
            $http.get('/api/v1/inbox/getHameshHistory/').then(function (data) {
                $scope.hamesh_history = data.data;
            })
        }


        $scope.Prop = {};
        $scope.$on("setSelectMemProp", function (event, args) {
            $scope.Prop = args;
            //////console.log($scope.Prop);
        })
        $rootScope.$on("setSelectMemProp", function (event, args) {
            $scope.Prop = args;
            //////console.log($scope.Prop);
        })


        $scope.sendOption = {};
        $scope.NumOfItemSel = -1;
        $scope.ShowRecDetail = function (item, $index) {
            $scope.NumOfItemSel = $index;
            $scope.SelOptionItem = item;
            $("#modal_select_recievers").modal("show");
            $scope.getPreviousHamesh();

        }

        $scope.makehamesh = function (hamesh){
            $("#txtaHamesh").val(hamesh);
            $("#txtaHamesh").click();
        }

        $scope.AcceptOption = function () {
            $scope.Selected.data[$scope.NumOfItemSel] = $scope.SelOptionItem;
            $("#modal_select_recievers").modal("hide");

        }

    });