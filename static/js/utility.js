
/* this global variable will contain the HTML element with a message in it
   when people enter the wrong password */
var password_tooltip = null;
var username_tooltip = null;

function validate_passwords(pass1, pass2){
    $('#' + pass2 + ', #' + pass1).change(function(){
        var password = $('#' + pass1).val();
        var passwordrepeat = $('#' + pass2).val();

        // remove old tooltips
        if (password_tooltip)
            password_tooltip.remove();

        if (password === '' || passwordrepeat === ''){
            $('#' + pass2 + ', #' + pass1).removeClass('valid-input invalid-input');
            password_tooltip = $("<div class='tooltip'>").text("Please enter a password");
        } else if (password != passwordrepeat){
            $('#' + pass2 + ', #' + pass1).switchClass('valid-input', 'invalid-input',0);
            password_tooltip = $("<div class='tooltip'>").text("Make sure your passwords match");
        } else {
            $('#' + pass2 + ', #' + pass1).switchClass('invalid-input', 'valid-input',0);
            password_tooltip = null;
        }

        if (password_tooltip)
            $("body").append(password_tooltip
                .css({
                    top: ($("#" + pass2).position().top - 29) + "px",
                    left: ($("#" + pass2).position().left + $("#" + pass2).width() + 29) + "px"
                })
            );
    });
}

/*
    Form Validation
    Takes a jQuery form object, and ensures that all fields in
    the form are valid before submission.
*/
function validate_form($form, $output) {
    $form.submit(function(){
        if ($form.find('.invalid-input').length !== 0) {
            $output.text('Invalid-form');
            return false;
        }
        return true;
    });
}

/* This weil create password restrictions
   hopefully this will check with the database to see if the name has been taken
   if not don't shoot us */

function validate_username(new_user) {
    $this = $("#" + new_user);
    $this.change(function() {
        var unametest = $this.val();
        if (unametest === '') {
            $this.removeClass("valid-input invalid-input");
        } else {
            console.log(unametest);
            $.get('check_username/' + unametest,
                    function (data, textStatus, jqXHR) {

                    if (username_tooltip)
                        username_tooltip.remove();

                    if (data['username_available']) {
                        //alert('Username Available');
                        $this.switchClass('invalid-input','valid-input', 0);
                    } else {
                        //alert('Username not Available');
                        $this.switchClass('valid-input','invalid-input', 0);
                        username_tooltip = $("<div class='tooltip'>").text("Username " + unametest + " is not available.");

                        $("body").append(username_tooltip
                            .css({
                                top: ($this.position().top - 29) + "px",
                                left: ($this.position().left + $this.width() + 29) + "px"
                            })
                        );
                    }
                },"json");
        }
    });
}
