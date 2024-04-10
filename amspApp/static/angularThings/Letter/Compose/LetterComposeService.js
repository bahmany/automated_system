'use strict';

angular
    .module('AniTheme')
    .service('LetterComposeService',
    ['$cookies', '$http', '$location',
        function ($cookies, $http, $location) {


            this.SendLetter = function (letter) {
                if (
                    letter.hasOwnProperty("id") && letter.itemType == 7
                ) {
                    //delete letter.id;
                    return $http.put("/api/v1/letter/" + letter.id+"/", letter);
                }
                return $http.post("/api/v1/letter/", letter)
            }


        }]);






