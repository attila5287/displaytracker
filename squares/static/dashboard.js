  gaugeMeUp(1);
  bubbleMeup(1);
  pieMeUp(1);  
  histogramMeUp(1);
  var $squareSelect = document.getElementById("opts");

  $squareSelect.onchange = function () {
    dropdownSelected = $squareSelect.value;
    gaugeMeUp(dropdownSelected);
    bubbleMeup(dropdownSelected);
    pieMeUp(dropdownSelected);
    histogramMeUp(dropdownSelected);
    fetch('/fetch/square/info/'+dropdownSelected)
                .then((response) => {
                  return response.json();
                })
      .then((data) => {
                  console.log('data');
                  console.log(data);
                });

  }

  function gaugeMeUp(square) {
      Plotly.d3.json(`/fetch/main/avlb/` + square, function (error, percAvlb) {
        console.log(percAvlb)
        var data = [{
          type: "indicator",
          mode: "gauge+number+delta",
          value: percAvlb,
          title: {
            text: "Main-Item-Avlbty-%",
            font: {
              size: 16
            }
          },
          delta: {
            reference: 50,
            increasing: {
              color: "rgb(0, 43, 54)"
            }
          },
          gauge: {
            axis: {
              range: [null, 100],
              tickwidth: 1,
              tickcolor: "#B58900"
            },
            bar: {
              color: "#6610f2",
              line: {
                color: "#002B36",
                width: 4
              },
            },
            bgcolor: "#002B36",
            borderwidth: 3,
            bordercolor: "#B58900",
            steps: [{
              range: [0, 30],
              color: "#6f42c1"
            },
            {
              range: [30, 50],
              color: "#268BD2"
            }
            ],
            threshold: {
              line: {
                color: "#B58900",
                width: 8
              },
              thickness: 0.75,
              value: 100
            }
          }
        }];
        var layout = {
          plot_bgcolor: "#002B36",
          paper_bgcolor: "#002B36",
          responsive: true,
          margin: {
            t: 25,
            r: 25,
            l: 25,
            b: 25
          },
          font: {
            color: "#B58900",
            family: "monospace"
          }
        };
        $gauge = document.getElementById('avlb-gauge');
        Plotly.newPlot($gauge, data, layout);
      });
    }
  

  function bubbleMeup(square) {
  Plotly.d3.json('/itemattr/bubble/'+square, function (error, data) {
    if (error)
      return console.warn(error);
    // Create the Trace
    var trace1 = {
      x: data[0]["x"],
      y: data[0]["y"],
      mode: 'markers',
      marker: {
        size: data[0]["y"],
        sizemode: 'diameter',
        color: 'rgba(190, 47, 195, 0.631);',
        opacity: 0.99,
        sizeref: 0.8,
        line: {
          color: '#268BD2',
          width: 2
        }
      }
    };
    var layout = {
      plot_bgcolor: "#002B36",
      paper_bgcolor: "#002B36",
      showlegend: false,
      responsive: true,
      margin: {
        t: 12
      },
      padding: 1,
      type: "bar",
      responsive: true,
      xaxis: {
        tickfont: {
          size: 10,
          color: '#B58900',
        },
        showgrid: true,
        zeroline: false,
        showline: false,
        mirror: 'ticks',
        gridcolor: '#073642',
        gridwidth: 0.05,
        zerolinecolor: '#002B36',
        zerolinewidth: 0.25,
        linecolor: '#B58900',
        linewidth: 0.25,
      },
      yaxis: {
        tickfont: {
          size: 10,
          color: '#B58900',
        },
        showgrid: true,
        zeroline: false,
        showline: false,
        mirror: 'ticks',
        gridcolor: '#073642',
        gridwidth: 0.05,
        zerolinecolor: '#002B36',
        zerolinewidth: 0.25,
        linecolor: '#B58900',
        linewidth: 0.25,
      },
    };
    var data = [trace1];
    var $bubble = document.getElementById('item-bubble');
    Plotly.newPlot($bubble, data, layout);
  });
}


  function pieMeUp(square) {
    Plotly.d3.json('/manuf/pie/' + square, function (error, data) {
      if (error)
      return console.warn(error);
      var trace1 = {
      labels: data[0]["labels"],
      values: data[0]["values"],
      type: "pie",
      marker: {
        colors: [
          '#268BD2',
          '#6f42c1',
          '#D33682',
          '#2AA198',
          '#CB4B16',
          '#FDF6E3',
          '#073642',
        ],
        opacity: 0.99,
        line: {
          color: '#002B36',
          width: 8
        }
      }
    };
      var layout = {
      plot_bgcolor: "#002B36",
      paper_bgcolor: "#002B36",
      responsive: true,
      showgrid: true,
      legend: {
        font: {
          color: '#B58900',
        },
      }
    };
      var data = [trace1];
      var $pie = document.getElementById('manuf-pie');
      Plotly.plot($pie, data, layout);
  });
}
  
  function histogramMeUp(square) {
  Plotly.d3.json('/itemattr/histogram/'+square, function (error, data) {
    if (error)
      return console.warn(error);
    // Create the Trace
    var trace1 = {
      x: data[0]["x"],
      y: data[0]["y"],
      type: "bar",
      marker: {
        color: '#6610f2',
        opacity: 0.99,
        line: {
          color: '#002B36',
          width: 3
        }
      }
    };
    // Create the data array for the plot
    var data = [trace1];
    var layout = {
      margin: {
        t: 4
      },
      padding: 1,
      type: "bar",
      responsive: true,
      plot_bgcolor: "#002B36",
      paper_bgcolor: "#002B36",
      xaxis: {
        tickfont: {
          size: 10,
          color: '#B58900',
        },
        showgrid: true,
        zeroline: false,
        showline: false,
        mirror: 'ticks',
        gridcolor: '#073642',
        gridwidth: 0.05,
        zerolinecolor: '#002B36',
        zerolinewidth: 0.25,
        linecolor: '#B58900',
        linewidth: 0.25,
      },
      yaxis: {
        tickfont: {
          size: 10,
          color: '#B58900',
        },
        showgrid: true,
        zeroline: false,
        showline: false,
        mirror: 'ticks',
        gridcolor: '#073642',
        gridwidth: 0.05,
        zerolinecolor: '#002B36',
        zerolinewidth: 0.25,
        linecolor: '#B58900',
        linewidth: 0.25,
      },
    };
    var $histogram = document.getElementById('histogram-bar-chart');
    Plotly.newPlot($histogram, data, layout);
  });
}

