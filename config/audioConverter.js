const spawn = require('child_process').spawn;
const recognize = require('../config/speechRecognition.js')
exports.audiConverter = function (fileName,fileNameWithoutExt){

            

    var cmd = 'ffmpeg';

    var pathToSave = "/media/gulshair/AE98361E9835E58D/Development/FYP/hateSpeechDetection/";


    var args = [
        '-y', 
        '-i', pathToSave+'youtubemp3/'+fileName,
        '-acodec' , 'pcm_s16le', 
        '-ac', '1',
        '-ar', '16000', 
        '-f', 'wav', pathToSave+'uploads/'+fileNameWithoutExt+'.wav'
    ];

    var proc = spawn(cmd, args);

    /*proc.stdout.on('data', function(data) {
        console.log(data);
    });

    proc.stderr.on('data', function(data) {
        console.log(data);
    });*/

    proc.on('close', function() {
        console.log('finished');
        recognize.sendRequest('uploads/'+fileNameWithoutExt+'.wav').then(value => {
            return value;
            //res.render('index',{text:value});
            //console.log(value);   
        });
    });

    
    //console.log(filePath);

}