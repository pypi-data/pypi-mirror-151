
ManagerSelect = function (params) {

    var $field = params.$field,
        url = params.url;

    $field.select2({
        language: 'uk'
    });

    function handleFieldChange() {
        var managerId = $field.val(),
            data = {manager: managerId};

        $field.prop('disabled', true);

        $.post(url, data, handleManagerSet);
    }

    function handleManagerSet(response) {
        $field.prop('disabled', false);
        $.notify({message: response.message}, {type: 'success'});
        $(window).trigger('product-total-updated', response.total);
    }

    function handleManagerCreated(event, manager) {
        var $option = $('<option />');

        $option.text(manager.name);
        $option.prop('value', manager.id);

        $field.append($option);
        $field.val(manager.id);

        handleFieldChange();
    }

    $field.on('change', handleFieldChange);
    $(window).on('manager-created', handleManagerCreated);

};
