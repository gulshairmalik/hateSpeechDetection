const recognize = require('../config/speechRecognition.js');
const AudioRecorder = require('node-audiorecorder');
const fs = require('fs');
const path = require('path');

// Initialize recorder and file stream.
const audioRecorder = new AudioRecorder({
    program: process.platform === `win32` ? `sox` : `rec`,
    silence: 0
});
var fileName;

exports.recordAudio = (req,res) => {
   
    if(req.params.status=='start'){
        res.send('Recording Started');

        const DIRECTORY = './recordings';

        // Create path to write recordings to.
        if (!fs.existsSync(DIRECTORY)){
            fs.mkdirSync(DIRECTORY);
        }

        // Create file path with random name.
        fileName = path.join(DIRECTORY, Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 4).concat('.wav'));
        console.log(`Writing new recording file at: `, fileName);
        console.log('Recording Start');

        // Create write stream.
        const fileStream = fs.createWriteStream(fileName, { encoding: `binary` });
        // Start and write to the file.
        audioRecorder.start().stream().pipe(fileStream);

    }

    if(req.params.status=='stop'){
        res.send('Recoding Stoped.');
        audioRecorder.stop();
        console.log('Recording Stop');
        //recognize.sendRequest(fileName).then(console.log)
    }

    if(req.params.status=='print'){
        recognize.sendRequest(fileName).then(value => {
            //res.render('index',{text:value});
            //console.log(value);
            res.send(value);     
        });
    }

    
}