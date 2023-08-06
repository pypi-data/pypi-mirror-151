
CustomerSelect = function (params) {

    var $field = params.$field,
        url = params.url;

    $field.select2({
        language: 'uk',
        width: '100%'
    });

    function handleFieldChange() {
        var customerId = $field.val(),
            data = {customer: customerId};

        $field.prop('disabled', true);

        $.post(url, data, handleCustomerSet);
    }

    function handleCustomerSet(response) {
        $field.prop('disabled', false);
        $.notify({message: response.message}, {type: 'success'});
        $(window).trigger('product-total-updated', response.total);
    }

    function handleCustomerCreated(event, customer) {
        var $option = $('<option />');

        $option.text(customer.name);
        $option.prop('value', customer.id);

        $field.append($option);
        $field.val(customer.id);

        handleFieldChange();
    }

    $field.on('change', handleFieldChange);
    $(window).on('customer-created', handleCustomerCreated);

};
