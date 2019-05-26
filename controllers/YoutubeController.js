const stt_converter = require('../controllers/SpeechToTextController.js');
const convert = require('../config/audioConverter.js');
const spawn = require('child_process').spawn;
const getYouTubeID = require('get-youtube-id');
const fs = require('fs');
const path = require('path');

//ytdl http://www.youtube.com/watch?v=_HSylqgVYQI | ffmpeg -i pipe:0 -b:a 192K -vn myfile.mp3

exports.getAudio = function(req,res){

    //Current Directory path from root
    let appDir = path.dirname(require.main.filename);

    // stream = ytdl(url)

    // proc = new ffmpeg({source:stream})
    // proc.setFfmpegPath('/Applications/ffmpeg')
    // proc.saveToFile(mp3, (stdout, stderr)=>{

    // });

    var pathToSave = appDir+"/youtubemp3/";
    var vid = getYouTubeID(req.body.url);
    //console.log(id);
    var cmd2 = spawn('ytdl',[req.body.url]);
    var proc = spawn('ffmpeg',['-i', 'pipe:0', '-b:a', '192k', '-vn', pathToSave+vid+'.mp3']);
    cmd2.stdout.pipe(proc.stdin)

    // proc.stdout.on('data', function(data) {
    //     console.log(data);
    // });

    // proc.stderr.on('data', function(data) {
    //     console.log(data);
    // });

    proc.on('close', function() {
        console.log('finished');
     
        var fileName = vid+'.mp3';
        //var rs = fs.createReadStream(file);

        // rs.once('readable', function() {
        //     var buff = rs.read(8); //Read first 8 bytes only once
        // });
        //stt_converter.speechToText();
        var textvalue = convert.audiConverter(fileName,vid);
        res.render('index',{text:textvalue});

    });

}