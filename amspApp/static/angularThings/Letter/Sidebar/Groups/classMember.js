'use strict';


function memberInbox($scope, $http) {


//-------------------------------- services
    var listMember = function (companyId, query) {
        return $http.get("/search/company/members?cid=" + companyId + "&q=" + query)
    };
    var MembersPageTo = function (SearchChartList, PagerUrl) {
        var qurl = PagerUrl + "&q=" + SearchChartList;

        if (qurl.split("?").length == 1) {
            qurl = qurl.replace("&", "?");
        }
        return $http.get(qurl);
    };
//--------------------------------


    $scope.members = [];
    $scope.MembersSearchText = "";
    $scope.isSearchCallbackCompleted = true;
    $scope.getMembersList = function () {
        $scope.isSearchCallbackCompleted = false;
        listMember('drede23fa', $scope.MembersSearchText).then(function (data) {
            $scope.members = data.data;
            $scope.isSearchCallbackCompleted = true;
        }).catch(function (data) {
            $scope.isSearchCallbackCompleted = true;
        })
    };
    $scope.getMembersList();
    $scope.$watch("MembersSearchText", function () {
        $scope.getMembersList();
    });
    $scope.selects = [];
    $scope.addToSelected = function (member) {
        var hasBefore = false;
        for (var i = 0; $scope.selects.length > i; i++) {
            if ($scope.selects[i].id == member.id) {
                hasBefore = true;
            }
        }
        if (!hasBefore) {
            $scope.selects.push(member);
        }
    };
    $scope.removeSelected = function (member, index) {
        $scope.selects.splice(index, 1);
    };
    $scope.OpenSearch = function (name) {
        $(".searchmem").hide();
        $("#" + name).show();
    };
    $scope.OpenSearch("companymemberselectdiv");
    $scope.MemberPageTo = function (PageUrl) {
        $scope.isSearchCallbackCompleted = false;
        MembersPageTo($scope.ProfileSearch, PageUrl).then(function (data) {
            $scope.isSearchCallbackCompleted = true;
            $scope.SearchPersons = data.data;
        }).catch(function (data) {
            $scope.isSearchCallbackCompleted = true;
        });
    };
    $scope.RemovePersonFromSelected = function (index) {
        $scope.letter.selectedMembers.splice(index, 1);
    };

    $scope.hidePerRecDetails = function (event) {
        $(event.target).parent().parent().parent().find(".send-detail-per-rec").hide();
        $(event.target).parent().parent().parent().find(".show-detail-per-rec").show();
    };
    $scope.ShowSentDetail = function () {
        $("#divShowSentDetailbtn").hide();
        $("#divSentDetail").show();
    };
    $scope.HideSentDetail = function () {
        $("#divSentDetail").hide();
        $("#divShowSentDetailbtn").show();
    };
}