load = function() {
  jQuery(document).ready(function($){
      $('#id_date').datepicker({
          format: "yyyy-mm-dd",
          language: "ru"
      });
  });
}

setTimeout(load, 1000);
