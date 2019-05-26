const express = require('express');
const port = process.env.PORT || 3000;
const path = require('path');
const fileUpload = require('express-fileupload');
const bodyParser = require('body-parser');
const cors = require('cors');
//const mongoose =  require('mongoose');
//const db_url = 'mongodb://localhost/mvc';
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.set('views', path.join(__dirname, 'views'));
app.set('view engine','pug');
app.use(express.static(path.join(__dirname, 'public')));
app.use(fileUpload({
    limits: { fileSize: 5 * 1024 * 1024 },
}));
app.use(cors());



//Requring Routes
require('./config/routes')(app);

//Connecting Database
/*mongoose.connect(db_url);
let db = mongoose.connection;

db.on('error',function(err){
    if(err){
        console.log(err);
    }
});
db.once('open',function(){
    console.log('DB Connected Successfully');
});*/




app.listen(port, () => {
    console.log('Server started on port '+port);
});