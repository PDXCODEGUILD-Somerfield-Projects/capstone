/**
 * Created by sydneysomerfield on 5/11/17.
 */


$(document).ready(function() {
    $('.timestamp').each(function(index, item) {
        var query_date = Date.parse($(item).text().replace('.', '')+ ' UTC');
        var new_date = new Date(query_date);
        $(item).text(new_date);
    });

});


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


$(document).ready(function() {
    $('.runbutton').click(function(event) {
        var buttonId = (event.target.id).replace('run', '');
        $.get('/rerun/', {'id': buttonId})
            .done(function(response) {
                $('#querydata').hide();
                $('#testdata').show();
                $('#close').show();
                makeBubbles(response);
            })
            .fail(function() {
                $('#querydata').text('There was a problem running this query...');
            });
    })
});


$(document).ready(function() {
    $('#close').click(function() {
        $('#testdata').hide();
        $('#close').hide();
        $('#querydata').show();
    })
});


$('#checkall').change(function() {
    $("input:checkbox").prop('checked', $(this).prop('checked'));
});