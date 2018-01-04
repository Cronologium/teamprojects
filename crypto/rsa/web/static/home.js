$(document).ready(function(){
    $('#decryption-text').on('input',function(e){
        var data = {
            'text': $(this).val(),
            'n': $('#public-key-n').val(),
            'd': $('#private-key').val(),
            'csrfmiddlewaretoken': $('form input').val()
        };
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: '/decrypt',
            data: data,
            success: function(data) {
                $('#encryption-text').val(data['msg']);
            }
        });
    });

    $('#encryption-text').on('input',function(e){
        var data = {
            'text': $(this).val(),
            'n': $('#public-key-n').val(),
            'e': $('#public-key-e').val(),
            'csrfmiddlewaretoken': $('form input').val()
        };
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: '/encrypt',
            data: data,
            success: function(data) {
                $('#decryption-text').val(data['msg']);
            }
        });
    });
});