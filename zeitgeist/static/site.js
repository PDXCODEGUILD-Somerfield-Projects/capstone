/**
 * Created by sydneysomerfield on 4/22/17.
 */

'use strict';


function logIn(result) {
    return new Promise(function(resolve, reject) {
        var username = $("#username").val();
        var password = $("#password").val();
        //console.log(username, password);
        $.post('/login/', {username: username, password: password}, function(result) {
            resolve(result);
        });
    })
}


function updateUser(result) {
    var message = result.message;
    //console.log(result);
    if (message === 'login successful') {
        var first_name = result.first_name;
        $("#loginform").hide();
        $("#loginmessage").hide();
        $("#firstname").text(first_name);
        $("#loggedin").show();
    } else {
        $("#username").val("");
        $("#password").val("");
        if ($("#loginmessage").text() !== 'invalid login') {
            $("#loginmessage").text(message);
        }
    }
}


function getUserLocation(result) {
    return new Promise(function(resolve, reject) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            var latLongArray = [latitude, longitude];
            if (latLongArray !== undefined) {
                resolve(latLongArray);
                return latLongArray;
            } else {
                reject(Error('Error--can\'t get position'));
            }
        }, function(error) {
           console.log(error)
        });
    });
}


$(document).ready(function() {
    $("#loginbutton").click(function() {
       logIn().then(updateUser);
    })
});


$(document).ready(function() {
    $("#startbutton").click(function() {
        $('#testdata').empty();
        $('#loading').show();
        getUserLocation().then(passLatLong);
    })
});

