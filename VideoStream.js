var arDrone = require('ar-drone')
var cv      = require('opencv')
var fs      = require('fs')
var io      = require('socket.io').listen(5001)
var dl      = require('delivery')
var watch   = require('watch')
var EventEm = require('events').EventEmitter

console.log('Connecting png stream ...')

var client    = arDrone.createClient()
var pngStream = client.getPngStream()
var emitter   = new EventEm()
var count = 1

var currentFrame                            // Current frame of the video stream

pngStream
    .on('error', console.log)
    .on('data', function(pngBuffer) {
       currentFrame = pngBuffer
       fs.writeFile('./currentFrame.png', currentFrame, function(error){
           if (error) {
               console.error("Error writing file: " + error.message)
           } else {
               console.log("File create successfully")
               emitter.emit('frameUpdate')
           }
       })
  })

io.sockets.on('connection', function(socket) {
    console.log("Connected")
    var delivery = dl.listen(socket)
    delivery.on('delivery.connect', function(delivery) {
        connected = true
        console.log("connected")

        emitter.on('frameUpdate', function() {
            console.log("Sending file")
            delivery.send({
                name: 'currentFrame.png',
                path: './currentFrame.png'
            })
            console.log(count)
            count++
        })

        delivery.on('send.success', function(file){
            console.log("File successfully sent to client")
        })

    })
})
