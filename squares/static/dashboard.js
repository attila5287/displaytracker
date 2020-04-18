startWearingPurpleNow();
gaugeMeUp(1);
bubbleMeup(1);
pieMeUp(1);
histogramMeUp(1);
infoBoardSquare(1);
infoBoardAvlbCount(1);
infoBoardAvlbPerc(1);
sunBurnMeUp();
infoBoardManuf(1);
infoBoardMostCommon(1);
ddSlickItemsOf(1);

var $squareSelect = document.getElementById("opts");

dashboardUpdateAll();

function dashboardUpdateAll() {
  $squareSelect.onchange = function () {
    chosenSquare = $squareSelect.value;
    
    gaugeMeUp(chosenSquare);
    bubbleMeup(chosenSquare);
    pieMeUp(chosenSquare);
    histogramMeUp(chosenSquare);
    infoBoardSquare(chosenSquare);
    infoBoardAvlbCount(chosenSquare);
    infoBoardAvlbPerc(chosenSquare);
    infoBoardManuf(chosenSquare);
    infoBoardMostCommon(chosenSquare);
    ddSlickItemsOf(chosenSquare);
  };
}

function startWearingPurpleNow() {
  d3.select('#infoBubble')
    .on("mouseenter", flashEmUp('#bubbleZone','#bubbleDesc'))
    .on("mouseleave", flashEmDown('#bubbleZone','#bubbleDesc'));
  d3.select('#infoGauge')
    .on("mouseenter", flashEmUp('#gaugeZone','#gaugeDesc'))
    .on("mouseleave", flashEmDown('#gaugeZone','#gaugeDesc'));
  d3.select('#infoPie')
    .on("mouseenter", flashEmUp('#pieZone','#pieDesc'))
    .on("mouseleave", flashEmDown('#pieZone','#pieDesc'));
  d3.select('#infoHist')
    .on("mouseenter", flashEmUp('#histZone','#histDesc'))
    .on("mouseleave", flashEmDown('#histZone','#histDesc'));
  d3.select('#infoSunburst')
    .on("mouseenter", flashEmUp('#sunburstZone','#sunburstDesc'))
    .on("mouseleave", flashEmDown('#sunburstZone','#sunburstDesc'));  
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
  Plotly.d3.json('/itemattr/bubble/' + square, function (error, data) {
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
        sizeref: 0.5,
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
  Plotly.d3.json('/itemattr/histogram/' + square, function (error, data) {
    if (error)
      return console.warn(error);
    // Create the Trace
    var trace1 = {
      x: data[0]["x"],
      y: data[0]["y"],
      type: "bar",
      orientation: "h",
      marker: {
        color: '#6610f2',
        opacity: 0.99,
        line: {
          color: '#002B36',
          width: 1
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
        gridcolor: '#073642',
        gridwidth: 0.05,
        zerolinecolor: '#002B36',
        zerolinewidth: 0.25,
        linecolor: '#B58900',
        linewidth: 0.25,
      },
      yaxis: {
        autorange:"reversed",
        tickfont: {
          size: 10,
          color: '#B58900',
          showgrid: true,
          zeroline: false,
          showline: false,
          gridcolor: '#073642',
          gridwidth: 0.05,
          zerolinecolor: '#002B36',
          zerolinewidth: 0.25,
          linecolor: '#B58900',
          linewidth: 0.25,
        },
      },
    };
    var $histogram = document.getElementById('histogram-bar-chart');
    Plotly.newPlot($histogram, data, layout);
  });
}

function infoBoardSquare(square) {
  var queryURL = "/fetch/square/info/" + square;
  d3.json(queryURL, function (error, response) {
    if (error)
      return console.warn(error);
    console.log(response);
    console.log("type", typeof (response));
    var square = response.data[0];
    d3.select('#squareID').text(square.id).attr("class", "text-primary").style("font-size", "1rem");
    d3.select('#squareName').text(square.name).attr("class", "text-light");
    d3.select('#rowCount').text(square.row_count).attr("class", "text-primary").style("font-size", "1rem");
    d3.select('#colCount').text(square.col_count).attr("class", "text-primary").style("font-size", "1rem");
    var squareArea = square.row_count * square.col_count;
    d3.select('#squareArea').text(squareArea).attr("class", "text-primary").style("font-size", "1rem");
  });
}

function infoBoardAvlbCount(square) {
  var queryURL = "/fetch/main/avlb/count/" + square;
  d3.json(queryURL, function (error, response) {
    if (error)
      return console.warn(error);
    console.log(response);
    console.log("type", typeof (response));
    d3.select('#avlbItemsCount').text(response).attr("class", "text-primary").style("font-size", "1rem");
  });
}

function infoBoardAvlbPerc(square) {
  var queryURL = "/fetch/main/avlb/perc/" + square;
  d3.json(queryURL, function (error, response) {
    if (error)
      return console.warn(error);

    console.log(response);

    console.log("type", typeof (response));

    d3.select('#avlbItemsPerc').text(response + "%").style("font-size", "1rem");
  });
}

function sunBurnMeUp() {
  var labels = ['square', 'unit', 'item-Main', 'item-Disply', 'item', 'item'];
  var parents = ['', 'square', 'unit', 'unit', 'item-Main', 'item-Disply'];
  var data = [{
    type: "sunburst",
    labels: labels,
    parents: parents,
    values: [54, 24, 12, 12, 6, 6],
    outsidetextfont: {
      size: 14,
      color: "#377eb8"
    },
    leaf: {
      opacity: 0.4
    },
    marker: {
      line: {
        width: 2
      }
    },
  }];
  var layout = {
    plot_bgcolor: "#002B36",
    paper_bgcolor: "#002B36",
    responsive: true,
    margin: {
      l: 0,
      r: 0,
      b: 0,
      t: 0
    },
    sunburstcolorway: [
      "#00cc9", '#B58900', "#636efa", "#EF553B",
      '#6610f2', '#6f42c1'
    ],
    extendsunburstcolorway: true
  };
  Plotly.newPlot('models-sunburst', data, layout);
}

function infoBoardManuf(square) {
  var queryURL = "/fetch/manuf/info/" + square;
  d3.json(queryURL, function (error, response) {
    if (error)
      return console.warn(error);
    console.log(response);
    console.log("type", typeof (response));
    var mainArray = response["main"];
    var dispArray = response["disp"];
    innerMain = '';
    for (let i = 0; i < mainArray.length; i++) {
      const pairJSON = mainArray[i];
      innerMain += pairJSON.manufacturer + ': ' + pairJSON.percentage + '%  ';
    }
    d3.select('#manufMain').text(innerMain);
    innerDisp = '';
    for (let i = 0; i < dispArray.length; i++) {
      const pairJSON = dispArray[i];
      innerDisp += pairJSON.manufacturer + ': ' + pairJSON.percentage + '%  ';
    }
    d3.select('#manufDisp').text(innerDisp);

  });
}

function infoBoardMostCommon(square) {
  var queryURL = "/itemattr/mostcommon/" + square;
  d3.json(queryURL, function (error, response) {
    if (error)
      return console.warn(error);
    console.log(response);
    console.log("type", typeof (response));
    var dispArray = response.disp;
    var mainArray = response.main;
    innerDisp = '';
    for (let i = 0; i < dispArray.length; i++) {
      const pairJSON = dispArray[i];
      innerDisp += pairJSON.count + " " + pairJSON.attribute + "; ";
    }
    d3.select('#dispMostCommon').text(innerDisp);
    innerMain = '';
    for (let i = 0; i < mainArray.length; i++) {
      const pairJSON = mainArray[i];
      console.log(pairJSON);
      innerMain += pairJSON.count + " " + pairJSON.attribute + "; ";
    }
    d3.select('#mainMostCommon').text(innerMain);
  });
}

function flashEmUp(zoneId, zoneDescId) {
  return function () {
    d3.select(zoneId)
      .attr('class', 'card shadow-after');
    d3.select(zoneDescId)
      .attr('class', 'text-light');
            
    
  };
}

function flashEmDown(zoneId, zoneDescId) {
  return function () {
    d3.select(zoneId)
      .attr('class', 'card bg-transparent shadow-before');
    d3.select(zoneDescId)
      .attr('class', 'text-secondary');    
  };
}

function ddSlickItemsOf(square) {
  var queryURL = "/fetch/ddslick/square/" + square;
  d3.json(queryURL, function (error, data) {
    if (error)
      return console.warn(error);  
    $('#itemSelect').ddslick('destroy');
    $('#itemSelect').ddslick({
      data: data['disp'],
      width: 200,
    });
  });
}

