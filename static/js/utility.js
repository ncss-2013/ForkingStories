    /* password checker */
function validate_passwords(pass1, pass2){
    $('#' + pass2 + ', #' + pass1).change(function(){
        var password = $('#' + pass1).val();
        var passwordrepeat = $('#' + pass2).val();
        if (password == '' || passwordrepeat == ''){
            $('#' + pass2 + ', #' + pass1).removeClass('valid-input invalid-input');
        } else if (password != passwordrepeat){
            $('#' + pass2 + ', #' + pass1).switchClass('valid-input', 'invalid-input',0);
        } else {
            $('#' + pass2 + ', #' + pass1).switchClass('invalid-input', 'valid-input',0);
        }
    })
}

/*
    Form Validation
    Takes a jQuery form object, and ensures that all fields in
    the form are valid before submission.
*/
function validate_form($form, $output) {
    $form.submit(function(){
        if ($form.find('.invalid-input').length != 0) {
            $output.text('Invalid-form');
            return false;
        }
        return true;
    })
}


