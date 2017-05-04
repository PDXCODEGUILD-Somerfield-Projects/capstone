/**
 * Created by sydneysomerfield on 4/22/17.
 */

'use strict';


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

// function testForNow(result){
//     return new Promise(function(resolve, reject) {
//     var latitude = '45.523062';
//     var longitude = '-122.676482';
//     var latLongArray = [latitude, longitude];
//     resolve(latLongArray);
//         })
// }


function passLatLong(result) {
    console.log(result);
    var latitude = result[0];
    var longitude = result[1];
    $.get('/coordinates/', {lat: latitude, lng: longitude}, function(coordinates) {
        console.log(coordinates);
        var hashtag_data = coordinates.hashtags;
        var hashtag_array = hashtag_data;
        document.getElementById('bubbles').setAttribute("width", 400);
        document.getElementById('bubbles').setAttribute("height", 400);

        console.log(hashtag_data);

        var data_blob = [{'tag': 'Portland', 'count': 2}, {'tag': 'CyberSpaceWar', 'count': 3},
            {'tag': 'AlaskaAirlines', 'count': 1}, {'tag': 'solidarity', 'count': 4}];

        var svg = d3.select("svg"),
            width =+svg.attr('width'),
            height = +svg.attr('height');

        var color =  d3.scaleOrdinal(d3.schemeCategory20c);

        // d3.json(coordinates, function(data) {console.log(data);});

        var node = svg.selectAll(".node")
            .data(hashtag_data)
            .enter()
            .append("g")
            .attr("class", "node");


        node.append("circle")
            .attr("id", function(d) {return d.hashtag;})
            .attr("cx", function() {return Math.random() * width})
            .attr("cy", function() {return Math.random() * height})
            .attr("r", function(d) {return d.count * 15})
            .attr("fill", function (d) {return color(d.count);});

        node.append("text")
            .attr("x", function(d) {return d3.select("#" + d.hashtag).attr("cx")})
            .attr("y", function(d) {return d3.select("#" + d.hashtag).attr("cy")})
            .attr("text-anchor", "middle")
            .text(function(d) {return d.hashtag});


        $('#bubbles').after('<p>lat: ' + coordinates['lat'] + '</p>'
            + '<p>' + 'lng: ' + coordinates['lng'] + '</p>');
        });
    }


$(document).ready(function() {
    $("#startbutton").click(function() {
        getUserLocation().then(passLatLong);
    })
});
