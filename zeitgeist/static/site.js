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
        var twitter_data = coordinates.twitter;
        console.log(twitter_data);


        var diameter = 960;
            // color = d3.scaleOrdinal(d3.schemeCategory20c);

        var color1 = d3.scaleLinear()
                .domain([1, 10])
                .range(['#CCFFDD','#00B33C'])
                .interpolate(d3.interpolateHcl),
            color2 = d3.scaleLinear()
                .range(['#FFF0E6', 'FF6600'])
                .interpolate(d3.interpolateHcl)
                .domain([1, 10]),
            color3 = d3.scaleLinear()
                .range(['#C2D1F0', '#3366CC'])
                .interpolate(d3.interpolateHcl)
                .domain([1, 10]);

        var pack = d3.pack()
            .size([diameter, diameter])
            .padding(1.5);

        var svg = d3.select("#testdata").append("svg")
            .attr("width", diameter)
            .attr("height", diameter)
            .attr("class", "bubble");

        var root = d3
            .hierarchy({children:twitter_data})
            .sum(function (d) {
                return d.count;
            })
            .sort(function (a, b) {
                return b.count - a.count;
            });

        d3.pack(root);

        var node = svg.selectAll(".node")
            .data(pack(root).leaves())
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });

        node.append("circle")
            .attr("r", function (d) {
                return d.r;
            })
            .style("fill", function (d) {
                if (d.data.parcel === 'hashtag') {
                    return color1(d.data.count);
                } else if (d.data.parcel === 'user_mention') {
                    return color2(d.data.count);
                } else {
                    return color3(d.data.count);
                }
            });

        node.append("text")
            .attr("dy", ".3em")
            .style("text-anchor", "middle")
            .text(function (d) {
                if (d.data.parcel === 'hashtag'){
                    return "#" + d.data.text;
                } else if (d.data.parcel === 'user_mention') {
                    return "@" + d.data.text;
                } else {
                    return d.data.text;
                }
            });


        $('#bubbles').after('<p>lat: ' + coordinates['lat'] + '</p>'
            + '<p>' + 'lng: ' + coordinates['lng'] + '</p>');
        });
    }


$(document).ready(function() {
    $("#startbutton").click(function() {
        getUserLocation().then(passLatLong);
    })
});
