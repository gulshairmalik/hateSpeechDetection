var HomeController =  require('../controllers/HomeController.js');
var SpeechToTextController =  require('../controllers/SpeechToTextController.js');
var RecordController =  require('../controllers/RecordController.js');
var YoutubeController = require('../controllers/YoutubeController.js')

module.exports = function(app){
    app.get('/',HomeController.Index);
    app.get('/text',HomeController.Index);
    app.post('/text',SpeechToTextController.speechToText);
    app.get('/record/:status',RecordController.recordAudio);
    app.post('/getyoutube',YoutubeController.getAudio);
}