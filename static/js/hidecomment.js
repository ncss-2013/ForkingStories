$(function() {
    $('#hidecomment').click( function(event){
            if ($('#comment').is(':visible')){
                $('#hidecomment').val('Leave a comment');
            }
            else {
                $('#hidecomment').val('Leave a comment');
            }
            $('#comment').toggle();

    });
});
