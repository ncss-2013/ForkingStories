
/* this global variable will contain the HTML element with a message in it
   when people enter the wrong password */
var tooltip = null;

/* password checker */
function validate_passwords(pass1, pass2){
    $('#' + pass2 + ', #' + pass1).change(function(){
        var password = $('#' + pass1).val();
        var passwordrepeat = $('#' + pass2).val();
        
        // remove old tooltips
        if (tooltip)
            tooltip.remove();
        
        if (password == '' || passwordrepeat == ''){
            $('#' + pass2 + ', #' + pass1).removeClass('valid-input invalid-input');
            tooltip = $("<div class='tooltip'>").text("Please enter a password");
        } else if (password != passwordrepeat){
            $('#' + pass2 + ', #' + pass1).switchClass('valid-input', 'invalid-input',0);
            tooltip = $("<div class='tooltip'>").text("Make sure your passwords match");
        } else {
            $('#' + pass2 + ', #' + pass1).switchClass('invalid-input', 'valid-input',0);
            tooltip = null;
        }
        
        if (tooltip)
            $("body").append(tooltip
            
                .css({
                    top: "378px",
                    left: "589px"
                })
            );
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


