// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA7BR_yOa-jq_IK79T4yiVAqfDGe8zNHqA",
  authDomain: "hdbdatabase.firebaseapp.com",
  projectId: "hdbdatabase",
  storageBucket: "hdbdatabase.appspot.com",
  messagingSenderId: "496286911369",
  appId: "1:496286911369:web:f2e7253c0ee86e1c48af58",
  measurementId: "G-L3YRR931NL"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);