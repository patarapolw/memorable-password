$(document).ready(function(){
    $('#keywords').text(content.keywords.join(' '));
    $('#password').val(content.password);

    $('.type[value=' + content.type + ']').prop("checked", true);

    viewPassword($('.type:checked').val());

    $('img').attr('src', content.image);

    $('.type').on('click', function(){
        viewPassword($(this).val());
    });

    function viewPassword(passwordType){
        switch(passwordType){
            case 'pin':
                if(content.generate == 'password'){
                    $('#password').val(content.PIN);
                } else {
                    $('#password').val(content.password);
                }
                break;
            case 'simple':
                $('#password').val(content.keywords.join(''));
                break;
            case 'leetspeak':
                $('#password').val(content.leetspeak);
        }
    }
});