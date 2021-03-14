$( document ).ready(function() {
  var $transactionChart = $("#transaction-amount-chart");
  $.ajax({
    url: $transactionChart.data("url"),
    success: function (data) {

      var ctx = $transactionChart[0].getContext("2d");

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [{
            label: 'Amount',
            backgroundColor: 'blue',
            data: data.data
          }]
        },
        options: {
          responsive: true,
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Transaction amount chart'
          }
        }
      });

    }
  });

});
