$( document ).ready(function() {
  var $credit_by_date = $("#account-credit");
        $.ajax({
          url: $credit_by_date.data("url"),
          success: function (data) {

            var ctx = $credit_by_date[0].getContext("2d");

            new Chart(ctx, {
              type: 'bar',
              data: {
                labels: data.labels,
                datasets: [{
                  label: 'Money spent',
                  backgroundColor: 'blue',
                  data: data.data,
                  barPercentage: 0.5
                }]
              },
              options: {
                responsive: true,
                legend: {
                  position: 'top',
                },
              }
            });

          }
        });

});
