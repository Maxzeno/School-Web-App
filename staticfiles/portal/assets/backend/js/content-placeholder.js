$(document).ajaxStart(function(e) {
  //$('.content-main').hide();
  $('.content-placeholder').show();
});

$(document).ajaxStop(function(e) {
  setTimeout(
    function()
    {
      $('.content-placeholder').hide();
      //$('.content-main').fadeIn();
    }, 300);

});
