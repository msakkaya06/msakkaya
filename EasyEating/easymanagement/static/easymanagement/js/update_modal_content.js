// update_modal_content.js

function loadProduceUpdateModal(produceId) {
    $.ajax({
        url: '/produce_update/' + produceId + '/',
        type: 'GET',
        success: function(data) {
            $('.modal-content').html(data);
        }
    });
}