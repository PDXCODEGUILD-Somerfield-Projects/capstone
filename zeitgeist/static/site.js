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
        // document.getElementById('bubbles').setAttribute("width", 400);
        // document.getElementById('bubbles').setAttribute("height", 400);

        console.log(hashtag_data);
        var diameter = 400;

        var bubble = d3.pack()
            .size([diameter, diameter])
            .padding(1.5);

        var svg = d3.select("#testdata")
            .append("svg")
            .attr("width", diameter)
            .attr("height", diameter)
            .attr("class", "bubble");


        var bubbles = svg.append("g")
            .attr("transform", "translate(0,0)")
            .selectAll(".bubble")
            .data([{'tag': 'Portland', 'count': 2}, {'tag': 'CyberSpaceWar', 'count': 3},
            {'tag': 'AlaskaAirlines', 'count': 1}, {'tag': 'solidarity', 'count': 4}])
            .enter();

        bubbles.append("circle")
            .attr("r", function(d) {return d.count*15})
            .attr("cx", function() {return Math.random() *300 ;})
            .attr("cy", function() {return Math.random() *300 ;})
            .style("fill", function(d) {return color(d.count);});

        bubbles.append("text")
        .attr("x", function(d){ return d.x; })
        .attr("y", function(d){ return d.y + 5; })
        .attr("text-anchor", "middle")
        .text(function(d){ return d.tag; });

        // var svg = d3.select("#bubbles")
        //     .selectAll("circle")
        //     .data([{'tag': 'Portland', 'count': 2}, {'tag': 'CyberSpaceWar', 'count': 3},
        //         {'tag': 'AlaskaAirlines', 'count': 1}, {'tag': 'solidarity', 'count': 4}])
        //     .enter()
        //     .append("circle")
        //     .attr("cy", function() {return Math.random() * 400; })
        //     .attr("cx", function() {return Math.random() * 400; })
        //     .attr("r", function(d) {return Math.sqrt(d.count*3000)})
        //     .append("title")
        //     // // .attr("x", function(d) {return d.x; })
        //     // // .attr("y", function(d) {return d.y +5;})
        //     // .attr("text-anchor", "middle")
        //     .text(function(d) {return d.tag;});





        $('#bubbles').after('<p>lat: ' + coordinates['lat'] + '</p>'
            + '<p>' + 'lng: ' + coordinates['lng'] + '</p>');
        });
    }


$(document).ready(function() {
    $("#startbutton").click(function() {
        getUserLocation().then(passLatLong);
    })
});
