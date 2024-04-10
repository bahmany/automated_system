function loadNotification($scope, $http) {

    $scope.pool = function (msg) {

        // new chat posted
        if (msg == "1") {
            $scope.getUnreadChatsCount(); // updating alarm counts
            if ($scope.chatMessagesPanelisVisible) {
                $scope.updateChats();
            } else {

                $scope.getChats();

            }
        }

    }
    $scope.sendMessage = function () {
        $scope.ws4redis.send_message('A message');
    }
    $scope.on_connecting = function () {
        console.log('Websocket is connecting...');
    }
    $scope.on_connected = function () {

    }
    $scope.on_disconnected = function (evt) {
        console.log('Websocket was disconnected: ' + JSON.stringify(evt));
    }
    $scope.receiveMessage = function (msg) {
        // debugger;
        // console.log('Message from Websocket ----------------- : ' + msg);
        $scope.pool(msg);
    }
    var heartbeat_msg = '1', heartbeat_interval = null, missed_heartbeats = 0;
    $scope.ws4redis = {};
    // $scope.ws4redis = WS4Redis({
    //     // uri: 'ws://localhost:8000/ws/foobar?subscribe-broadcast&publish-broadcast&echo',
    //     uri: 'ws://' + location.hostname + (location.port ? ':' + location.port : '') + '/ws/foobar?subscribe-user',
    //     connecting: $scope.on_connecting,
    //     connected: $scope.on_connected,
    //     receive_message: $scope.receiveMessage,
    //     disconnected: $scope.on_disconnected,
    //     attempts:5,
    //     timer:5000
    //     // heartbeat_msg: "1"
    //
    // });
    $scope.SendWS = function () {
        $scope.sendMessage();
    };
}