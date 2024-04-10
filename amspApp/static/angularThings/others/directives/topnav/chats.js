function loadChat($scope, $http) {
    $scope.chatters = {};
    $scope.chatters.results = [];
    $scope.filter = {};
    $scope.filter.q = '';
    $scope.chatListLoading = false;
    $scope.updateChattersList = function (data) {
        var found = false;
        var i_index, x_index = -1;
        if (data) {
            if (data.results) {
                for (var i = 0; data.results.length > i; i++) {
                    for (var x = 0; $scope.chatters.results.length > x; x++) {
                        if ($scope.chatters.results[x]) {
                            if ($scope.chatters.results[x].positionID) {
                                if (data.results[i].positionID == $scope.chatters.results[x].positionID) {
                                    found = true;
                                    i_index = i;
                                    x_index = x;
                                }
                            }
                        }
                    }
                    if (found) {
                        $scope.chatters.results[x_index] = data.results[i];
                    } else {
                        $scope.chatters.results.push(data.results[i]);
                    }
                }
            }
        }

        // $scope.chatters = data;

    }

    $scope.$watch('chattersText', function () {
        $scope.getRelatedChatters(false);
    })

    $scope.getRelatedChatters = function (partialUpdate) {
        if (partialUpdate) {
            $scope.chatListLoading = true;
        }
        $http.get("/api/v1/chat/getRelatedChatters/?q=" + $scope.chattersText).then(function (data) {
            $scope.chatListLoading = false;
            if (partialUpdate) {
                $scope.updateChattersList(data.data);
            } else {
                $scope.chatters = data.data;
            }

        }).catch(function () {
            $scope.chatListLoading = false;
        })
    };
    $scope.BackToChatList = function () {
        // $("#divChat").removeClass("chatters-show-panel").addClass("chatters-hide-panel");
        //
        $("#divChat").fadeOut(function () {
            $("#divChatterList").fadeIn();
            $scope.updateChattersList();
            $scope.chatMessagesPanelisVisible = false;
        });
    }
    $scope.singleChatter = {};


    $scope.chatMessagesPanelisVisible = false;
    $scope.openChat = function (item) {
        $scope.singleChatter = item;
        $("#divChatterList").fadeOut(function () {
            $("#divChat").fadeIn();
            $scope.chatMessagesPanelisVisible = true;
        });
        $scope.getChats();
    };
    $scope.chatSignleLoading = false;

    $scope.scrollToChatEnd = function () {
        $("#divSigleChats").scrollTop($("#divSigleChats")[0].scrollHeight);

    }

    $scope.getChats = function () {
        $scope.chatSignleLoading = true;

        $http.get("/api/v1/chat/" + $scope.singleChatter.positionID + "/getSingleChat/").then(function (data) {
            if (data.data.msg) {
                $scope.chatSignleLoading = false;
                $scope.singleChats = data.data;

            }
        }).catch(function () {
            $scope.chatSignleLoading = false;

        });
    };
    $scope.updateChats = function () {
        var haveWeSomeChats = false;
        if ($scope.singleChats.results) {
            if (($scope.singleChats.results.length) > 0) {
                haveWeSomeChats = true;
            }
        }
        if (haveWeSomeChats) {
            $http.get("/api/v1/chat/" + $scope.singleChatter.positionID + "/updateChats/?li=" + $scope.singleChats.results[$scope.singleChats.results.length - 1].id + "").then(function (data) {
                if (data.data.msg) {
                    $scope.singleChats.results.pushArray(data.data.results);

                    // $scope.chatSignleLoading = false;
                    // $scope.singleChats = data;

                }
            }).catch(function () {
                // $scope.chatSignleLoading = false;

            });
        } else {
            $scope.getChats();
        }
    }

    $scope.newChat = {};
    $scope.postSingle = function () {
        $scope.newChat.chatType = 1;
        $scope.newChat.dest_positionID = $scope.singleChatter.positionID;

        $("#btnSendChat").attr("disabled", "true").text("در حال ارسال");

        $http.post("/api/v1/chat/", $scope.newChat).then(function (data) {
            // $scope.getChats();
            $("#btnSendChat").removeAttr("disabled", null).text("ارسال");
            if (data.data.id) {
                $("#divSigleChats").scrollTop($("#divSigleChats")[0].scrollHeight);
                // var objDiv = document.getElementById("btnSendChat");
                // objDiv.scrollTop = objDiv.scrollHeight;

                $scope.singleChats.results.push(data.data);
                $scope.newChat = {};

            }
        })
    };
    $scope.isRightBarOpen = false;
    $scope.OpenRightBar = function () {
        $("#quickview-sidebar").removeClass("right-side-closed").addClass("right-side-opened");
        $scope.isRightBarOpen = true;
        $scope.getRelatedChatters(true);

    }
    $scope.CloseRightBar = function () {
        $("#quickview-sidebar").removeClass("right-side-opened").addClass("right-side-closed");
        $scope.isRightBarOpen = false;
    }
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
    /*

     msg == 1 : new chat
     msg == 2 : new msg red
     */
    //

    $scope.unreadCounts = {};
    $scope.getUnreadChatsCount = function () {
        $http.get("api/v1/chat/getUnreadChatsCount/").then(function (data) {
            if (data.data.msg == "ok") {
                $scope.unreadCounts = data.data;

            } else {
                $scope.unreadCounts.unreadCounts = -1;

            }
        })
    };
    $scope.getUnreadChatsCount();


    $scope.updatechats = function () {
        // if sidebar is not open then show this in alert icon
        // if (!($scope.isRightBarOpen)) {
        $scope.getUnreadChatsCount();
        // getting not read chats
        // }

        if ($scope.isRightBarOpen) {
            $scope.getRelatedChatters(false);
        }


        // $scope.getChats();

    }
}