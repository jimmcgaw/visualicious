var Visualicious = Visualicious || {};

Visualicious.load_bookmarks = function(){
  var bookmark_div = jQuery("#bookmarks");
  jQuery.ajax({
    url: '/load_bookmarks/',
    method: 'get',
    success: function(response_json){
      //response_json = jQuery.parseJSON(response_json);
      if (response_json && response_json.bookmarks_html){
        bookmark_div.html(response_json.bookmarks_html);
      }
    }
  });
};

jQuery(document).ready(function(){
  Visualicious.load_bookmarks();
  
  var form = jQuery("form");
  form.submit(function(){
    var progress = jQuery("#progress");
    var submit = jQuery("#submit");
    progress.toggleClass("hidden");
    submit.toggleClass("hidden");
  });
});