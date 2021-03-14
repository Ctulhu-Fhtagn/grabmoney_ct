$( document ).ready(function() {
    var $balance_by_date = $("#balance-by-date");
          $.ajax({
            url: $balance_by_date.data("url"),
            success: function (data) {

              var ctx = $balance_by_date[0].getContext("2d");

              new Chart(ctx, {
                type: 'bar',
                data: {
                  labels: data.labels,
                  datasets: [{
                    label: 'Amount',
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
                  title: {
                    display: true,
                    text: 'Balance by date'
                  }
                }
              });

            }
          });

  });
