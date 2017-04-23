/**
 * Created by sydneysomerfield on 4/22/17.
 */

'use strict';


function getUserLocation(result) {
    return new Promise(function(resolve, reject) {
        navigator.geolocation.getCurrentPosition((function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            var latLongArray = [latitude, longitude];
            if (latLongArray !== undefined) {
                resolve(latLongArray);
                return latLongArray;
            } else {
                reject(Error('Error--can\'t get position'));
            }
        }));
    });
}


function passLatLong(result) {
    var latitude = result[0];
    var longitude = result[1];
    $.get('/coordinates/', {lat: latitude, lng: longitude}, function(coordinates) {
        $('#testdata').append('lat: ' + coordinates['lat']
            + '<p>' + 'lng: ' + coordinates['lng'] + '</p>');
    });
}


$(document).ready(function() {
    $("#startbutton").click(function() {
        getUserLocation().then(passLatLong);
    })
});
