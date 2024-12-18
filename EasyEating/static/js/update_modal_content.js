$(document).ready(function() {
    // Her form için submit olayını dinle
    $('[id^="update-form"]').submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var produceId = form.attr('id').split('-')[2]; // Formun benzersiz ID'sinden ürün ID'sini al
        var successMsgDiv = $('#modal-success-msg-' + produceId); // İlgili modalın başarı mesaj div'ini hedefle
        var errorMsgDiv = $('#modal-error-msg-' + produceId); // İlgili modalın hata mesaj div'ini hedefle

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            dataType: 'json',

            success: function(response) {
                console.log(response)
                if (response.success) {
                    errorMsgDiv.hide();
                    successMsgDiv.html('<p>' + response.message + '</p>')
                    successMsgDiv.show();

                } else {
                    successMsgDiv.hide();
                    errorMsgDiv.html('<p>' + response.error_msg + '</p>');
                    errorMsgDiv.show();

                }
            }
        });
    });
});