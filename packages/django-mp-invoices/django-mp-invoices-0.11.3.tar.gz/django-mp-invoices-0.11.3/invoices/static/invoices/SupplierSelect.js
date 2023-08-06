
SupplierSelect = function (params) {

    var $field = params.$field,
        url = params.url;

    $field.select2({
        language: 'uk',
        width: '100%'
    });

    function handleFieldChange() {
        var supplierId = $field.val(),
            data = {supplier: supplierId};

        $field.prop('disabled', true);

        $.post(url, data, handleSupplierSet);
    }

    function handleSupplierSet(response) {
        $field.prop('disabled', false);
        $.notify({message: response.message}, {type: 'success'});
        $(window).trigger('product-total-updated', response.total);
    }

    function handleSupplierCreated(event, supplier) {
        var $option = $('<option />');

        $option.text(supplier.name);
        $option.prop('value', supplier.id);

        $field.append($option);
        $field.val(supplier.id);

        handleFieldChange();
    }

    $field.on('change', handleFieldChange);
    $(window).on('supplier-created', handleSupplierCreated);

};
