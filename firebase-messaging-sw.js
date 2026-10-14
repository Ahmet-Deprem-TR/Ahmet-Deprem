importScripts('https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.8.0/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey: "SENIN_API_KEY",
    authDomain: "SENIN_PROJECT_ID.firebaseapp.com",
    projectId: "SENIN_PROJECT_ID",
    storageBucket: "SENIN_PROJECT_ID.appspot.com",
    messagingSenderId: "SENIN_SENDER_ID",
    appId: "SENIN_APP_ID"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log('Arka plan bildirimi geldi:', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: 'Dprmauresim.png'
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
