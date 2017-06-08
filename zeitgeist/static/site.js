/**
 * Created by sydneysomerfield on 4/22/17.
 */

'use strict';


function logOut() {
    return new Promise(function(resolve, reject) {
        $.get('/logout/')
            .done(function(response) {
                console.log('This worked');
                resolve();
            })
            .fail(function() {
                reject(result);
                console.log('The promise call failed on logout.');
            });
    })
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
    $("#startbutton").click(function() {
        $('#testdata').empty();
        $('#lat-long-display').remove();
        $('#loading').show();
        getUserLocation().then(passLatLong);
    })
});


$(document).ready(function() {
    $("#logoutbutton").click(function() {
        logOut().then(function() {
            window.location.replace('https://twitter.com/logout');
        })
    })
});