'use strict';

angular
    .module('AniTheme')
    .service('LetterForwardService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {
            this.ForwardTo = function (inboxID, selectedList) {
                return $http.post("/api/v1/inbox/forward/"+inboxID+"/send/", selectedList);
            }
        }]);






