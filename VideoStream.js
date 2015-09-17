//
//
//
// var arDrone = require('ar-drone')
// var cv      = require('opencv')
// var http    = require('http')
// var output  = require('fs').createWriteStream('./vid.h264');
//
// console.log("Connecting video stream")
//
// var client = arDrone.createClient();
// client.config('general:navdata_demo', 'FALSE');
//
// // var PaVEParser = require('ar-drone/lib/video/PaVEParser');
//
// //
// var video = arDrone.createClient().getVideoStream();
// // var parser = new PaVEParser();
// //
// // parser
// //   .on('data', function(data) {
// //     output.write(data.payload);
// //   })
// //   .on('end', function() {
// //     output.end();
// //   });
// //
// // video.pipe(parser);
//
// client.disableEmergency()
//
// console.log("no")
//
// client.takeoff(function() {
//     console.log("k")
//     client.land(function() {
//         console.log("Tyler")
//     })
// })


// Run this to receive a png image stream from your drone.

var arDrone = require('ar-drone')
var cv      = require('opencv')
var http    = require('http')
var fs      = require('fs')

var currentFrame

//var stream  = arDrone.createUdpNavdataStream();
var client = arDrone.createClient()
var videoStream = client.getVideoStream()

videoStream
    .on('error', console.log)
    .on('data', function(videoBuffer) {
        currentFrame = videoBuffer
        console.log(videoBuffer)
    })
