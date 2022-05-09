// get data and open modal on thread preview click
$(document).ready(function(){
    $('.create_diary').click(function(){
        var id = $(this).data('id');
        $.ajax({
            url: '/create_diary',
            type: 'post',
            data: {id: id},
            success: function(data){
                $('.modal-body').html(data);
                $('.modal-body').append(data.htmlresponse);
                $('#Modal').modal('show');
            }
        });
    });
});

//escape key close popup
$(document).keydown(function(event) {
  if (event.keyCode == 27) {
    $('#Modal').modal('hide');
  }
});

$(document).ready(function(){
  $(.'open_diary').click(function(){
    $('.open_diary').hide();
    var id = $(this).data('diary_id'):
    $.ajax({
      url: '/open_diary',
      type: 'post',
      data: {id: id},
      success: function(data){
      }
    })
  })
})
