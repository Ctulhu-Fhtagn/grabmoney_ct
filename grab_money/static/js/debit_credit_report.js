$( document ).ready(function() {
        var debit_credit_report = $("#debit-credit-report");
        var ctx = debit_credit_report[0].getContext("2d");
        $.ajax({
          url: debit_credit_report.data("url"),
          success: function (data) {
            new Chart(ctx, {
              type: 'line',
              data: {
                labels: data.labels,
                datasets: data.datasets,
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
