var timer = new Timer();

if($('#invalidFile').val()!==''){
    $('#invalidFile').fadeTo(4000, 500).slideUp(500, function(){
        $("#success-alert").slideUp(500);
    });
}

$('#record').click(function(){

    if($("#record").attr("name")=='record'){
        
        $.ajax({
            type: 'GET',
            url: 'http://localhost:3000/record/start'
        }).done(function(response) {
    
            timer.start();
            timer.addEventListener('secondsUpdated', function (e) {
                $('#timer').html(timer.getTimeValues().toString());
            });
            $('#record').html("Stop");
            $("#record").attr("name","stop");
        });
    
        
    }

    else if($("#record").attr("name")=='stop'){
        
        $.ajax({
            type: 'GET',
            url: 'http://localhost:3000/record/stop'
        }).done(function(response) {
    
            timer.stop();
            $("#record").attr("name","record");
            $('#record').html("Record");
            console.log(response);

            $.ajax({type: 'GET',url: 'http://localhost:3000/record/print'}).done(function(res){
                $('#textarea').val(res);
                console.log('Response Received.');
            });
            
        });

    }
 

});

$('#clear').click(function(){
    $('#textarea').val('');
    $('#results').css('display','none');

});

$('#btnurl').click(function(){ 
    var urltext = $('#texturl').val();
    $.ajax({
        type: 'POST',
        url: 'http://localhost:3000/getyoutube',
        data: {url:urltext}
    });
    //alert(urltext);
});

$('#detect').click(function (event) {

    if($('#textarea').val()!==''){
        var data_input = JSON.stringify({"sentence":$('#textarea').val()});
        if(!$('#textarea').val().match(/^[ A-Za-z0-9`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]+$/)){
            //قادیانی کافر ہیں
            $.ajax({
                type: 'POST',
                url: 'http://localhost:8000/hatespeech/api/',
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                data: data_input
            }).done(function (response) {

                if(response.hate_label==='Not-Hate-Speech' && response.hate_level==='Not-Hate-Speech'){

                    $('#panel1').removeClass('panel-danger');
                    $('#panel2').removeClass('panel-danger');
                    
                    $('#panel1').addClass('panel-success');
                    $('#panel2').addClass('panel-success');
                    

                }else{
                    $('#panel1').removeClass('panel-success');
                    $('#panel2').removeClass('panel-success');

                    $('#panel1').addClass('panel-danger');
                    $('#panel2').addClass('panel-danger');
                }
                
                if(response.offensive_label==='Non Offensive'){
                    $('#panel3').removeClass('panel-danger');
                    $('#panel3').addClass('panel-success');
                }else{
                    $('#panel3').removeClass('panel-success');
                    $('#panel3').addClass('panel-danger');
                }

                $('#results').css('display','block');
                $('#category').html(" "+response.hate_label);
                $('#level').html(" "+response.hate_level);
                $('#offensive').html(" "+response.offensive_label);

                console.log(response);
            });
        }
        else{
            $('#err').text('Input must be in Urdu');
            $('#err').fadeTo(3000, 500).slideUp(500, function(){
                $("#success-alert").slideUp(500);
            });
        }
    }
    else{
        $('#err').text('This field is required.');
        $('#err').fadeTo(2000, 500).slideUp(500, function(){
            $("#success-alert").slideUp(500);
        });
    }
});
