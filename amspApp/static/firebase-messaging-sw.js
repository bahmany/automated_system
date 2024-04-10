'use strict';

importScripts('/static/bower_components/google-firebase/firebase-app.js');
importScripts('/static/bower_components/google-firebase/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.


var firebaseConfig = {
    apiKey: "AIzaSyCslK7cJxUGyStpiMNj_uyGaDPAdJbufrE",
    authDomain: "rahsoon-66afd.firebaseapp.com",
    databaseURL: "https://rahsoon-66afd.firebaseio.com",
    projectId: "rahsoon-66afd",
    storageBucket: "rahsoon-66afd.appspot.com",
    messagingSenderId: "731814768196",
    appId: "1:731814768196:web:6d3bfdda9ad31a89db9611"
};


firebase.initializeApp(firebaseConfig);

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function (payload) {
    // console.log('[firebase-messaging-sw.js] Received background message ', payload);
    var obj = JSON.parse(payload.data.message);
    obj = obj.notification;

    // Customize notification here
    const notificationTitle = obj.title;
    const notificationOptions = {
        body: obj.body,
        data: {url: obj.click_action},
        actions: [{action: "open_url", title: "مشاهده"}]
    };


    self.addEventListener('notificationclick', function (event) {
        event.notification.close();
        event.waitUntil(self.clients.openWindow(event.notification.data.url));
        event.notification.close();
    });


    return self.registration.showNotification(notificationTitle,
        notificationOptions);
});

