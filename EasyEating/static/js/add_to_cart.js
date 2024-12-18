// $(document).ready(function() {
//     $('.add-to-cart-form').on('submit', function(event) {
//         event.preventDefault(); // Formun normal submit işlemini engelle
//         var form = $(this);
//         var url = form.attr('action'); // Formun gönderileceği URL
//         var productId = form.data('product-id'); // Ürün ID'sini al
//         var quantity = form.find('input[name="quantity"]').val(); // Adeti al

//         // CSRF belirtecini al
//         var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

//         // Veri nesnesini oluştur
//         var data = {
//             'csrfmiddlewaretoken': csrfToken,
//             'produce_id': productId,
//             'quantity': quantity
//         };

//         $.ajax({
//             type: 'POST', // POST isteği yapılacak
//             url: url, // Formun gönderileceği URL
//             data: data, // Form verileri
//             success: function(response) {
//                 // Başarılı bir şekilde eklendiğinde yapılacak işlemler
//                 alert('Ürün sepete eklendi!');
//             },
//             error: function(xhr, status, error) {
//                 // Hata durumunda yapılacak işlemler
//                 alert('Ürün sepete eklenirken bir hata oluştu.');
//             }
//         });
//     });
// });
$(document).ready(function() {
    $('.add-to-cart-form').on('submit', function(event) {
        event.preventDefault(); // Formun normal submit işlemini engelle
        var form = $(this);
        var url = form.attr('action'); // Formun gönderileceği URL
        var productId = form.data('product-id'); // Ürün ID'sini al
        var quantity = form.find('input[name="quantity"]').val(); // Adeti al

        // CSRF belirtecini al
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        // Veri nesnesini oluştur
        var data = {
            'csrfmiddlewaretoken': csrfToken,
            'produce_id': productId,
            'quantity': quantity
        };

        // AJAX isteği yerine formun POST isteği yapması
        $.post(url, data)
            .done(function(response) {
                // Başarılı bir şekilde eklendiğinde yapılacak işlemler
                alert('Ürün sepete eklendi!');
            })
            .fail(function(xhr, status, error) {
                // Hata durumunda yapılacak işlemler
                alert('Ürün sepete eklenirken bir hata oluştu.');
            });
    });
});