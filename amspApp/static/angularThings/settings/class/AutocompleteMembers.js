function setUpMemberAutocomplement(angularModel,companyID,  Service){
        angularModel.isDisabled = false;
        //angularModel.selectedItem = null;
        //angularModel.searchText = null;
        angularModel.list = [];
        angularModel.selectItem = function (item) {
            angularModel.selectedItem = item;
        };
        angularModel.querySearch = function (query) {
            return Service.GetMembers(
                query,
                20,
                companyID
            ).then(function (data) {
                    return angularModel.mapData(data.data.results);
                });
        };
        angularModel.mapData = function (data) {
            return data.map(function (state) {
                return {
                    value: state.id,
                    display: state.profileName + " - " + state.chartName
                }
            });
        };

        angularModel.GetMembers = function () {

            Service.GetMembers(
                angularModel.MembersTableSearch,
                30,
                companyID
            ).then(function (data) {
                    angularModel.Members = data.data;
                });
        };


}