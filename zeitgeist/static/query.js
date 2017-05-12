/**
 * Created by sydneysomerfield on 5/11/17.
 */


$(document).ready(function() {
    $("#deletequery").click(function(event) {
        var checkValues = $('.todelete:checked').map(function() {
            return this.value;
        }).get();
        if (checkValues.length > 0){
                console.log(checkValues);
            $.post('/deletequery/', {'checks': checkValues})
                .done(function(response) {
                    if (response.message === 'success') {
                       window.location.reload();
                    } else {
                       $('#querydata').text('Something went wrong...');
                    }
                })
                .fail(function() {
                    $('#querydata').text('Something went wrong...');
                });
        }
    })
});

$('#checkall').change(function() {
    $("input:checkbox").prop('checked', $(this).prop('checked'));
});