/**
 * Created by sydneysomerfield on 5/11/17.
 */


//creates zero padding for date format
function pad(n, width) {
  n = n + '';
  if (n.length >= width) {
      return n;
  } else {
      return new Array(width - n.length + 1).join(0) + n;
  }
}

//formats datetime string to the browser timezone
$(document).ready(function() {
    $('.timestamp').each(function(index, item) {
        var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'];
        var queryDate = Date.parse($(item).text().replace('.', '')+ ' UTC');
        var newDate = new Date(queryDate);
        var m = newDate.getMonth();
        var d = pad(newDate.getDate(), 2);
        var y = newDate.getFullYear();
        var h = pad(newDate.getHours(), 2);
        var min = pad(newDate.getMinutes(), 2);
        var s = pad(newDate.getSeconds(), 2);
        $(item).text(monthNames[m] + ' ' + d + ', ' + y + ', ' + h + ':' + min + ':' + s);
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
                // $('#close').show();
                $('#close').css('display', 'block');
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