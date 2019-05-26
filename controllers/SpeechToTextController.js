const recognize = require('../config/speechRecognition.js');
const path = require('path');
var spawn = require('child_process').spawn;

exports.speechToText = function(req,res){

    //Current Directory path from root
    let appDir = path.dirname(require.main.filename);

    let File = req.files.file;

    //Getting Filename
    let validExtension = ['.mp3','.wav','.mp4'];
    let fileName = File.name;
    let filExtension = fileName.substring(fileName.length-4,fileName.length)
    let fileNameWithoutExt = fileName.substring(0, fileName.length-4);

    if(validExtension.includes(filExtension)){
        File.mv('./mp3files/'+fileName, function(err) {
            if (err){
                res.render('index',{err:err});
            }
            else{
                
    
                var cmd = 'ffmpeg';
                var pathToSave = appDir;
    
                var args = [
                    '-y', 
                    '-i', pathToSave+'mp3files/'+fileName,
                    '-acodec' , 'pcm_s16le', 
                    '-ac', '1',
                    '-ar', '16000', 
                    '-f', 'wav', pathToSave+'/uploads/'+fileNameWithoutExt+'.wav'
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
                        res.render('index',{text:value});
                        //console.log(value);   
                    }).catch(err=>{console.log(err);});
                });
            }  
        });
    } 
    else{
        res.render('index',{error:'Invalid file. Please upload in mp3, wav or mp4 format.'});
    }   
}

