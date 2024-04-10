'use strict';

angular
    .module('AniTheme')
    .service('LetterPrevService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {

            this.GetInboxItem = function (ID) {
                return $http.get("/api/v1/inbox/getLetterPrev/?id=" + ID);
            }

            this.moveToTrash = function (ID) {
                return $http.get("/api/v1/inbox/" + ID + "/moveToTrash/");

            }

            this.moveToArchive = function (InboxID) {
                return $http.get("/api/v1/inbox/" + InboxID + "/moveToArchive/");
            }
            this.moveFromArchive = function (InboxID) {
                return $http.get("/api/v1/inbox/" + InboxID + "/moveFromArchive/");
            }
            this.deleteForEver = function (ID) {
                return $http.get("/api/v1/inbox/" + ID + "/deleteForEver/");
            }

            this.OpenHistory = function (inboxID) {
                return $http.get("/api/v1/inbox/" + inboxID + "/history/");

            }

        }]);






