'use strict';


angular.module('AniTheme').controller(
    'LetterPrevCtrl',
    function ($scope,
              $translate,
              $timeout,
              $q, $state,
              $rootScope,
              $location,
              $stateParams,
              $modal,
              $$$, $filter,
              $mdToast,
              $http,
              shareService,
              InboxListService,
              LetterPrevService,
              shareServiceBool) {
        $scope.CurrentLetter = {};
        $scope.letterHistory = [];
        $rootScope.$broadcast("hideInboxLeft");


        InboxListService.MakeLetterRead($stateParams.inboxID).then(function (data) {
            $rootScope.GetIntimeNotification();
        });


        $scope.prevImgLink = "";
        $scope.hideLayer = function () {
            $scope.prevImgLink.replace("um5", "um70");
            $("#divPrevLayer").fadeOut();
        }
        $scope.previewAtt = function (imgUrl) {
            $scope.prevImgLink = imgUrl;
            $scope.prevImgLink = $scope.prevImgLink.replace("um5", "um70");

            $("#divPrevLayer").fadeIn(function () {

            });


        }


        $scope.OpenPrint = function () {
            $scope.CurrentLetter.LetterShDate = $filter('jalaliDate')($scope.CurrentLetter.letter.dateOfPost, 'jYYYY/jMM/jDD');
            $scope.CurrentLetter.InboxDate = $filter('jalaliDate')($scope.CurrentLetter.dateOfObservable, 'jYYYY/jMM/jDD');
            PopupLetter($scope.CurrentLetter);
        }

        $scope.downloadLetterAtt = function ($event) {
            angular.element($event.target).attr("disabled", true);
            downloadURL("/api/v1/inbox/" + $stateParams.inboxID + "/downloadAttachment/");
            angular.element($event.target).attr("disabled", false);
        }

        $scope.download = function (imgInf) {
            downloadURL(imgInf.replace('thmum50_', ''));
        }

        $scope.ReadInboxItem = function (inboxID) {

            $("#divLetterPrev").fadeOut(100, function () {
                $scope.letterHistory = [];
                $(".letterHistory").hide();
                $(".letter-body-prev").show();
                LetterPrevService.GetInboxItem(inboxID).then(function (data) {
                    $scope.CurrentLetter = data.data;
                    $("#divLetterPrev").fadeIn(100);
                    update_notif();
                    ////////console.log($scope.CurretLetter);
                });
            });

        };
        $scope.$on("callInboxPrev", function (event, args) {
            $scope.ReadInboxItem(args.inboxID);
        });

        $scope.InboxList = [];
        //$scope.inboxIndex = 0;


        $scope.init = function () {
            shareServiceBool.set(true); // for handling back from prev
            $scope.InboxList = shareService.get();
            $scope.InboxList.currentSelected = $stateParams.inboxID;
            shareService.set($scope.InboxList);

            if (!$scope.InboxList.results) {
                LetterPrevService.GetInboxItem($stateParams.inboxID).then(function (data) {
                    $scope.CurrentLetter = data.data;
                    update_notif();


                });
                return
            }
            var found = false;
            for (var i = 0; $scope.InboxList.results.length > i; i++) {
                if ($scope.InboxList.results[i].inboxId == $stateParams.inboxID) {
                    LetterPrevService.GetInboxItem($stateParams.inboxID).then(function (data) {

                        $scope.CurrentLetter = data.data;
                        $scope.inboxIndex = $scope.InboxList.from + i;
                        found = true;
                        update_notif();

                    });
                }
            }
            if (found == false) {
                LetterPrevService.GetInboxItem($stateParams.inboxID).then(function (data) {
                    $rootScope.$broadcast("hideInboxLeft");
                    $scope.CurrentLetter = data.data;
                    $scope.inboxIndex = $scope.InboxList.from + i;
                    update_notif();

                    found = true;
                });
            }
            InboxListService.MakeLetterRead($stateParams.inboxID);
        };

        $scope.OpenNext = function () {
            if (!$scope.InboxList.results) {
                $location.path("/dashboard/Letter/Inbox/List");
                return
            }
            for (var i = 0; $scope.InboxList.results.length > i; i++) {
                if ($scope.CurrentLetter.id == $scope.InboxList.results[i].id) {
                    if (i + 1 < $scope.InboxList.pageSize) {
                        //if ($scope.InboxList.results.length >= i) {
                        //    $location.path("/dashboard/Letter/list");
                        //    return
                        //}
                        $location.path('/dashboard/Letter/Inbox/' + $scope.InboxList.results[i + 1].id + '/Preview')
                        $scope.inboxIndex = $scope.InboxList.from + i;
                    } else {
                        if ($scope.InboxList.next) {
                            InboxListService.GetInboxListByPager($scope.InboxList.next).then(function (data) {
                                $scope.isSearchCallbackCompleted = true;
                                $scope.InboxList = data.data;
                                shareService.set($scope.InboxList);
                                $rootScope.$broadcast("transferList", $scope.InboxList);
                                $scope.inboxIndex = $scope.InboxList.from + i;
                                $location.path('/dashboard/Letter/Inbox/' + $scope.InboxList.results[0].id + '/Preview')
                            }).catch(function (data) {
                                $scope.isSearchCallbackCompleted = true;
                            });
                        }
                    }
                }
            }
        };

        $scope.OpenPrev = function () {
            if (!$scope.InboxList.results) {
                $location.path("/dashboard/Letter/Inbox/List");
                return
            }

            for (var i = 0; $scope.InboxList.results.length > i; i++) {
                if ($scope.CurrentLetter.id == $scope.InboxList.results[i].id) {
                    if (i > 0) {
                        $scope.inboxIndex = $scope.InboxList.from + i;
                        $location.path('/dashboard/Letter/Inbox/' + $scope.InboxList.results[i - 1].id + '/Preview')
                    } else {
                        if ($scope.InboxList.previous) {
                            InboxListService.GetInboxListByPager($scope.InboxList.previous).then(function (data) {
                                $scope.isSearchCallbackCompleted = true;
                                $scope.InboxList = data.data;
                                shareService.set($scope.InboxList);
                                $rootScope.$broadcast("transferList", $scope.InboxList);
                                $scope.inboxIndex = $scope.InboxList.from + i;
                                shareServiceBool.set(true); // for handling back from prev

                                $location.path('/dashboard/Letter/Inbox/' + $scope.InboxList.results[$scope.InboxList.results.length - 1].id + '/Preview')
                            }).catch(function (data) {
                                $scope.isSearchCallbackCompleted = true;
                            });
                        }
                    }
                }
            }
        };


        $scope.GoToList = function () {
            $location.path("/dashboard/Letter/Inbox/List")
        };

        $scope.init();
        $scope.prepareDownloadUrl = function (url) {
            return url.replace("thmum50_", "");
        }
        $scope.OpenEdit = function () {
            $state.go("compose", {letterID: $scope.CurrentLetter.letter.id});
        }
        $scope.forwardModelInstance = {};
        $scope.OpenForward = function (letterToEdit) {
            $scope.forwardModelInstance = $modal.open({
                animation: true,
                templateUrl: 'page/letter/forward',
                controller: 'LetterForwardCtrl',
                scope: $scope,
                size: '',
                resolve: {
                    deps: ["$ocLazyLoad", function ($ocLazyLoad) {
                        ////////console.log("perparing to get scripts");
                        return $ocLazyLoad.load({
                            name: 'AniTheme.EditLetter',
                            files: [
                                '/static/angularThings/Letter/Sidebar/Groups/classChart.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classGroup.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classMember.js',
                                '/static/angularThings/Letter/Sidebar/Groups/classZone.js',
                                '/static/angularThings/Letter/Forward/LetterForwardService.js',
                                '/static/angularThings/Letter/Forward/LetterForwardController.js'
                            ],
                            catch: true
                        }).then(
                            function () {

                                $timeout(function () {
                                }, 0);
                            }
                        )
                    }]

                }
            });
            $scope.forwardModelInstance.opened.then(function () {
                $timeout(function () {
                    $rootScope.$broadcast("SetCurrentLetterForForward", {CurrentLetter: $scope.CurrentLetter});
                }, 0);

                //$scope.$apply();

            })
            $scope.forwardModelInstance.result.then(function (res) {
            }, function () {

            });
        };


        //----------------------
        var originatorEv;
        $scope.openMenu = function ($mdOpenMenu, ev) {
            originatorEv = ev;
            $mdOpenMenu(ev);
        };
        //----------------------


        $scope.moveToTrash = function () {
            ////////console.log(letter);
            swal({
                title: $$$("Are you sure?"),
                text: $$$("Selected letter move to your trash!"),
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes, remove it!"),
                cancelButtonText: $$$("No, cancel plx!"),
                closeOnConfirm: false,
                closeOnCancel: false,
                showLoaderOnConfirm: true
            }, function (isConfirm) {
                if (isConfirm) {
                    LetterPrevService.moveToTrash($stateParams.inboxID).then(function (data) {
                        swal($$$("Removed!"), $$$("Selected letter successfully removed to trash ."), "success");
                        $rootScope.$broadcast("callInboxItems", {});
                        $location.path("/dashboard/Letter/Inbox/List");
                    });
                } else {
                    swal($$$("Cancelled"), $$$("Operation canceled"), "error");
                }
            });
        };
        $scope.deleteForEver = function (letter) {
            swal({
                title: $$$("Are you sure?"),
                text: $$$("Selected letter move to your trash!"),
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: $$$("Yes, remove it!"),
                cancelButtonText: $$$("No, cancel plx!"),
                closeOnConfirm: false,
                closeOnCancel: false,
                showLoaderOnConfirm: true
            }, function (isConfirm) {
                if (isConfirm) {
                    LetterPrevService.deleteForEver(letter.id).then(function (data) {
                        swal($$$("Removed!"), $$$("Selected letter successfully removed to trash ."), "success");
                        $rootScope.$broadcast("callInboxItems", {});
                    });
                } else {
                    swal($$$("Cancelled"), $$$("Operation canceled"), "error");
                }
            });
        };
        $scope.MoveToArchive = function () {
            LetterPrevService.moveToArchive($stateParams.inboxID).then(function (data) {
                $rootScope.$broadcast("callInboxItems", {});
                $scope.showActionToast("Archived");
                $scope.CurrentLetter.itemPlace = 2;
            }).catch(function () {

            })
        };


        var last = {
            bottom: false,
            top: true,
            left: false,
            right: true
        };
        $scope.toastPosition = angular.extend({}, last);
        $scope.getToastPosition = function () {
            sanitizePosition();
            return Object.keys($scope.toastPosition)
                .filter(function (pos) {
                    return $scope.toastPosition[pos];
                })
                .join(' ');
        };

        function sanitizePosition() {
            var current = $scope.toastPosition;
            if (current.bottom && last.top) current.top = false;
            if (current.top && last.bottom) current.bottom = false;
            if (current.right && last.left) current.left = false;
            if (current.left && last.right) current.right = false;
            last = angular.extend({}, current);
        }

        $scope.showActionToast = function (msg) {
            var toast = $mdToast.simple()
                .textContent(msg)
                .action('OK')
                .highlightAction(false)
                .position($scope.getToastPosition());
            $mdToast.show(toast).then(function (response) {
                if (response == 'ok') {

                }
            });
        };


        $scope.MoveFromArchive = function () {
            LetterPrevService.moveFromArchive($stateParams.inboxID).then(function (data) {
                $rootScope.$broadcast("callInboxItems", {});
                $scope.showActionToast('Send to Inbox');
                $scope.CurrentLetter.itemPlace = 1;
            }).catch(function () {

            })
        };
        $scope.letterHistory = {};

        $scope.RemoveFromRecInbox = function (historyItem) {
            $http.post("/api/v1/inbox/" + $stateParams.inboxID + "/removeHistoryUnseen/", historyItem).then(function (data) {
                $scope.OpenHistory($scope.CurrentLetterHistory);
            });
        };

        $scope.CurrentLetterHistory = {};
        $scope.isHistoryProccessing = false;
        $scope.OpenHistory = function (letter) {
            $scope.isHistoryProccessing = true;
            $scope.CurrentLetterHistory = letter;
            $(".letter-body-prev").fadeOut(100, function () {
                $(".letterHistory").fadeIn(50, function () {
                    //////console.log(letter);
                    $http.get("/api/v1/inbox/" + $stateParams.inboxID + "/history/").then(function (data) {
                        $scope.isHistoryProccessing = false;
                        $scope.letterHistory = data.data;
                    }).catch(function () {
                        $scope.isHistoryProccessing = false;

                    });
                });
            })
        };


        $scope.BackToInbox = function () {
            $(".letterHistory").fadeOut(100, function () {
                $(".letter-body-prev").fadeIn(50);
            });
        }
        $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {


        });
        $scope.RemoveFromFolders = function (index, item, folderItem) {
            swal({
                title: $$$("Remove from folder"),
                text: $$$("Are you sure to remove this letter from the folder ?"),
                type: "warning",
                showCancelButton: true,
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                var q = {
                    inboxID: $stateParams.inboxID,
                    folderID: folderItem.id
                };
                $http.post("/api/v1/inboxFolders/RemoveFromLetter/", q).then(function (data) {
                    $rootScope.$broadcast("GetInboxDynamicFoldersCount");
                    item.folders.splice(index, 1);
                    //$scope.GetFoldersJson();
                    swal($$$("Completely Removed"), $$$("removed from folder"), "success");
                });
            });
        };

        $scope.MakeLetterUnRead = function (CurrentLetter) {

            $rootScope.$broadcast("notifyconnected");
            return $http.get("/api/v1/inbox/unreadLetter/?id=" + CurrentLetter.id).then(function (data) {
                $rootScope.$broadcast("callInboxItems", {});
                $location.path("/dashboard/Letter/Inbox/List");
            })
        };
        $scope.ForwardSelected = function () {
            $rootScope.$broadcast("setSelectMemProp", {
                prevDivName: "divPrev",
                currDivName: "divForward",
                thisListIsFor: 3, // forward selected letter
                selectedInboxID: $stateParams.inboxID
            });
            $("#divPrev").fadeOut(function () {
                $("#divForward").fadeIn();
            });
        };
        $scope.ForwardSelectedArchive = function () {
            $rootScope.$broadcast("setSelectMemProp", {
                prevDivName: "divPrev",
                currDivName: "divForward",
                thisListIsFor: 5, // forward selected letter and archive
                selectedInboxID: $stateParams.inboxID
            });
            $("#divPrev").fadeOut(function () {
                $("#divForward").fadeIn();
            });
        };

        $scope.loadingComposeLetter = false;
        $scope.NewLetter = function () {
            if ($scope.loadingComposeLetter) {
                return
            }
            $scope.loadingComposeLetter = true;
            var letter = {};
            //$scope.letter.itemType = 1;
            // in the server
            // backend automatically change item mode to 7 for first send and
            // put 1 to other
            // to show in send items
            letter.itemType = 7;
            letter.itemMode = 4;
            letter.itemPlace = 1;

            letter.letterType = 7;
            letter.letterMode = 4;
            letter.letterPlace = 1;
            letter.body = " ";
            letter.subject = " ";
            letter.selectedMembers = [];
            $http.post("/api/v1/letter/", letter).then(function (data) {
                $scope.loadingComposeLetter = false;
                $location.path('/dashboard/Letter/' + data.data.id + '/compose');
            });
        };


        $scope.OpenReplay = function () {
            if ($scope.loadingComposeLetter) {
                return
            }
            // debugger;
            // let s = $stateParams;
            $scope.loadingComposeLetter = true;
            var letter = {};
            //$scope.letter.itemType = 1;
            // in the server
            // backend automatically change item mode to 7 for first send and
            // put 1 to other
            // to show in send items
            let is_letter_loaded = true;
            if ($scope.CurrentLetter === undefined) {
                is_letter_loaded = false;
            }

            if ($scope.CurrentLetter !== undefined) {
                if ($scope.CurrentLetter.letter === undefined) {
                    is_letter_loaded = false;
                }
            }


            letter.itemType = 7;
            letter.itemMode = 4;
            letter.itemPlace = 1;

            letter.letterType = 7;
            letter.letterMode = 4;
            letter.letterPlace = 1;
            letter.body = " ";

            // is_letter_loaded = false;
            if (is_letter_loaded === false) {
                $http.get("/api/v1/inbox/getLetterPrev/?id=" + $stateParams.inboxID).then(function (data) {
                    letter.subject = "پاسخ به :" + data.data.letter.subject;
                    data.data.sender.option = {};
                    letter.recievers = [data.data.sender];
                    $http.post("/api/v1/letter/", letter).then(function (__data) {
                        $scope.loadingComposeLetter = false;
                        $state.go("compose", {'letterID': __data.data.id});
                    });
                })
            } else {
                letter.subject = "پاسخ به :" + $scope.CurrentLetter.letter.subject;
                $scope.CurrentLetter.sender.option = {};
                letter.recievers = [$scope.CurrentLetter.sender];
                $http.post("/api/v1/letter/", letter).then(function (data) {
                    $scope.loadingComposeLetter = false;
                    $state.go("compose", {'letterID': data.data.id});
                });
            }

            ////////console.log($scope.CurrentLetter);
            // letter.subject = "پاسخ به :" + $scope.CurrentLetter.letter.subject;
            // //letter.oldLetter = $scope.CurrentLetter;
            // $scope.CurrentLetter.sender.option = {};
            // letter.recievers = [$scope.CurrentLetter.sender];
            // $http.post("/api/v1/letter/", letter).then(function (data) {
            //     $scope.loadingComposeLetter = false;
            //     $state.go("compose", {'letterID': $stateParams.inboxID});
            // });
            // //$rootScope.$broadcast("ReplayTo", {prevLetter: $scope.CurrentLetter});
        };

        $scope.$on("UpdateRecievers", function (event, args) {
            ////////console.log(args);
        });


        $scope.RemoveFromLabels = function (index, item, labelItem) {
            swal({
                title: $$$("Remove from labels"),
                text: $$$("Are you sure to remove this letter from the label ?"),
                type: "warning",
                showCancelButton: true,
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function () {
                var q = {
                    inboxID: $stateParams.inboxID,
                    labelID: labelItem.id
                };
                $http.post("/api/v1/inboxLabels/RemoveFromLetter/", q).then(function (data) {
                    $rootScope.$broadcast("GetInboxDynamicLabelsCount");
                    item.labels.splice(index, 1);
                    //$scope.GetFoldersJson();
                    swal($$$("Completely Removed"), $$$("removed from labels"), "success");

                });


            });


        };

    }
)
;


function getHistory(inboxID) {
    d3.select("#divD3HistoryContainer svg").remove();
    var margin = {top: 20, right: 120, bottom: 20, left: 120},
        width = 960 - margin.right - margin.left,
        height = 500 - margin.top - margin.bottom;

    var i = 0,
        duration = 750,
        root;

    var tree = d3.layout.tree()
        .size([height, width]);

    var diagonal = d3.svg.diagonal()
        .projection(function (d) {
            return [d.y, d.x];
        });
    var svgMain = d3.select("#divD3HistoryContainer").append("svg")
        .attr("width", width + margin.right + margin.left)
        .attr("height", height + margin.top + margin.bottom);
    var clippedpath = svgMain.append("defs").append("clipPath").attr("id", "clip");
    clippedpath.append("circle").attr("cx", "0").attr("cy", "0").attr("r", "15");

    var svg = svgMain
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
///api/v1/inbox/564b23ef9c6e101424268107/history/
//var prevScope = angular.element($("#divLetterPrvController")).scope();

    function collapse(d) {
        if (d._children) {
            d.children = d.children;
            d.children.forEach(collapse);
            d._children = null;
        }
    }


    d3.json("/api/v1/inbox/" + inboxID + "/history/", function (error, flare) {
        ////////console.log(flare);
        if (error) throw error;

        root = flare;
        root.x0 = height / 2;
        root.y0 = 0;


        root.children.forEach(collapse);
        update(root);
        d3.select(self.frameElement).style("height", "800px");
    });


    function update(source) {

        // Compute the new tree layout.
        var nodes = tree.nodes(root).reverse(),
            links = tree.links(nodes);

        // Normalize for fixed-depth.
        nodes.forEach(function (d) {
            d.y = d.depth * 180;
        });

        // Update the nodes…
        var node = svg.selectAll("g.node")
            .data(nodes, function (d) {
                return d.id || (d.id = ++i);
            });

        // Enter any new nodes at the parent's previous position.
        var nodeEnter = node.enter().append("g")
            .attr("class", "node")
            .attr("transform", function (d) {
                return "translate(" + source.y0 + "," + source.x0 + ")";
            })
            .on("click", click);

        nodeEnter.append("circle")
            .attr("r", 1e-6)
            .style("fill", function (d) {
                return d._children ? "lightsteelblue" : "#fff";
            });

        nodeEnter.append("image")
            .attr("xlink:href", function (d) {
                return d.recieverDetail.avatar.replace('q=', 'q=thmum100_');
            })
            .attr("width", "50px")
            .attr("height", "50px")
            .attr('x', -20)
            .attr('y', -20)
            .attr("clip-path", "url(#clip)");


        nodeEnter.append("text")
            .attr("x", function (d) {
                return d.children || d._children ? -10 : 10;
            })
            .attr("dy", ".35em")
            .attr("class", "letter-history-items")
            .attr("text-anchor", function (d) {
                return d.children || d._children ? "end" : "start";
            })
            .text(function (d) {
                var txtComp = " خوانده نشده ";
                if (d.recieverDetail.seen) {
                    txtComp = " خوانده شده ";
                }
                return moment(d.recieverDetail.dateOfObservable).format('jYYYY-jMM-jDD hh:mm:ss') + " - " + txtComp;
            })
            .style("fill-opacity", 1e-6);

        nodeEnter.append("text")
            .attr("x", function (d) {
                return d.children || d._children ? -10 : 10;
            })
            .attr("dy", "1.5em")
            .attr("class", "letter-history-items")
            .attr("text-anchor", function (d) {
                return d.children || d._children ? "end" : "start";
            })
            .text(function (d) {
                return d.recieverDetail.name + " - " + d.recieverDetail.chart
            })
            .style("fill-opacity", 1);

        // Transition nodes to their new position.
        var nodeUpdate = node.transition()
            .duration(duration)
            .attr("transform", function (d) {
                return "translate(" + d.y + "," + d.x + ")";
            });

        nodeUpdate.select("circle")
            .attr("r", 4.5)
            .style("fill", function (d) {
                return d._children ? "lightsteelblue" : "#fff";
            });

        nodeUpdate.select("text")
            .style("fill-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function (d) {
                return "translate(" + source.y + "," + source.x + ")";
            })
            .remove();

        nodeExit.select("circle")
            .attr("r", 1e-6);

        nodeExit.select("text")
            .style("fill-opacity", 1e-6);

        // Update the links…
        var link = svg.selectAll("path.link")
            .data(links, function (d) {
                return d.target.id;
            });

        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", function (d) {
                var o = {x: source.x0, y: source.y0};
                return diagonal({source: o, target: o});
            });

        // Transition links to their new position.
        link.transition()
            .duration(duration)
            .attr("d", diagonal);

        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
            .duration(duration)
            .attr("d", function (d) {
                var o = {x: source.x, y: source.y};
                return diagonal({source: o, target: o});
            })
            .remove();

        // Stash the old positions for transition.
        nodes.forEach(function (d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }

// Toggle children on click.
    function click(d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
        update(d);
    }
}