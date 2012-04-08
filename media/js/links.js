jQuery(document).ready(function(){
  var form = jQuery("form");
  form.submit(function(){
    var progress = jQuery("#progress");
    var submit = jQuery("#submit");
    progress.toggleClass("hidden");
    submit.toggleClass("hidden");
  });
});