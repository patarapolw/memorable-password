$(document).ready(function(){
    $('#sentence-display').html(sentence);
    $('#password-display').html(password);
    $('input[name="generate"]').click(function(){
        if($(this).val() === 'sentence'){
            $('#sentence-header').removeClass('disabled');
            $('select[name="from"]').attr('disabled', false);
            $('#material').attr('disabled', false);
        } else {
            $('#sentence-header').addClass('disabled');
            $('select[name="from"]').attr('disabled', true);
            $('#material').attr('disabled', true);
        }
    });
    $('select[name="from"]').click(function(){
        var value = $(this).val()
        var $material = $('#material');
        if(value === 'random'){
            $material.attr('placeholder', '').attr('disabled', true);
        } else {
            $material.attr('disabled', false);
            if(value === 'keywords'){
                $material.attr('placeholder', 'Please input your keywords, separated by comma.');
            } else if(value === 'initials'){
                $material.attr('placeholder', 'Please input your initials.');
            } else {
                $material.attr('placeholder', 'Please input your PIN.');
            }
        }
    });
    $('input[name="type"]').click(function(){
        if($(this).val() === 'password'){
            console.log('type-password selected');
        } else {
            console.log('type-pin selected');
        }
    });
    $('#password-generator').submit(function(e){
        e.preventDefault();
        $.post('/', $(this).serialize())
            .done(function(data){
            $('#password-display').html(data.password);
            $('#sentence-display').html(data.sentence);
        })
    })
});