$(document).ready(function(){
    $('#password-display').html(password);
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
    $('#password-generator').submit(function(e){
        e.preventDefault();
        $.post('/', $(this).serialize())
            .done(function(data){
            $('#password-display').html(data.password);
            $('#sentence-display').html(data.sentence);
        })
    });

    $(document).ajaxSend(function( event, xhr, settings ){
        if ( settings.url === "/" ){
            $('.loading-container').show();
        }
    }).ajaxComplete(function( event, xhr, settings ){
        if ( settings.url === "/" ){
            $('.loading-container').hide();
        }
    });

    $('#password-generator').submit();
});