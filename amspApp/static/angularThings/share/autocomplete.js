function setupAutoComplete($scope, $http, $q, $log, modelName) {


    $scope[modelName + "_simulateQuery"] = false;
    $scope[modelName + "_isDisabled"] = false;
    $scope[modelName + "_HamkaranItems"] = [];

    $scope[modelName + "_repos"] = function () {
        var deferred = $q.defer();
        var hamk = $http.get("/api/v1/salesItems/getItemsFromHamkaran/?search=" + $scope[modelName + "_searchText"]);
        hamk.then(function (data) {
            deferred.resolve(data.map(function (repo) {
                repo.value = repo.PartCode + " " + repo.PartName;
                return repo;
            }));
        });
        return deferred.promise;
    }

    $scope[modelName + "_querySearch"] = function (query) {
        var deferred = $q.defer();
        var result = query ? $scope[modelName + "_repos"]().then(function (data) {
            deferred.resolve(data.data.filter($scope[modelName + "_createFilterFor"](query)));
        }) : $scope[modelName + "_repos"]();
        return deferred.promise;
    }

    $scope[modelName] = {};
    $scope[modelName + "_searchTextChange"] = function (text) {
    }

    $scope[modelName + "_selectedItemChange"] = function (item) {
        if (item) {
            $scope[modelName] = item;
        }

    }

    $scope[modelName + "_createFilterFor"] = function (query) {
        var lowercaseQuery = angular.lowercase(query);
        return function filterFn(item) {
            return (item.value.indexOf(lowercaseQuery) != -1);
        };

    }


}


