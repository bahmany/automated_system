'use strict';

angular
    .module('AniTheme')
    .service('InboxListService',
    ['$cookies', '$http', '$location','$rootScope',
        function ($cookies, $http, $location,$rootScope) {


            var PagerUrl = "/search/inbox/";
            this.GetInboxListByPager = function (addr) {
                return $http.get(addr);
            };

            this.GetInboxList = function (q, position) {
                return $http.get(PagerUrl + "?" + q + "&p=" + position.toString())
            };

            this.MakeLetterRead = function (inboxID) {
                $rootScope.$broadcast("notifyconnected");
                return $http.get("/api/v1/inbox/readLetter/?id=" + inboxID)
            };

            this.GetInboxListBy = function (q,folderID, labelID) {
                return $http.get(PagerUrl + "?q=" + q + "&fi=" + folderID + "&li=" + labelID);
            }
        }]);






