gridView(1);

var $squareSel3ct = document.getElementById("opts");

$squareSel3ct.onchange = function () {
  d3.selectAll(".card-deck").remove();

  var square = $squareSel3ct.value;
  gridView(square);

};

function gridView(square) {
  var squareURL = "/fetch/square/info/" + square;
  d3.json(squareURL, function (error, response) {
    if (error)
      return console.warn(error);
    var square = response.data[0];
    var rowCount = square.row_count;
    var squar3 = $squareSel3ct.value;
    var queryURL = "/fetch/d3/grid/" + squar3;
    var $grid = d3.select(".grid");
    d3.json(queryURL, function (error, data) {
      if (error)
        return console.warn(error);
      for (let index = 0; index < rowCount; index++) {
        const row = data[index];
        var cardDeck = $grid.append("div").attr('class', 'card-deck');
        for (let index = 0; index < row.length; index++) {
          const JSONobj = row[index];
          console.log(index);
          var $card = cardDeck.append("div")
            .attr("class", "card square-section bg-transparent border-secondary text-center mx-1 mb-2");
          var newHeader = $card.append("div").attr("class", "card-header py-0").text(JSONobj.unique_tag);
          newHeader.append('i').attr('class', 'fa fa-tag ml-2');
          var newImg = $card.append("img").attr("class", "card-img-top bg-white").attr("src", JSONobj.imageSrc);
          var $cardBody = $card.append("div").attr("class", "card-body bottom-align-text bg-white p-0");
          var newBodyTitle = $cardBody.append("h5").attr("class", "card-title text-dark m-0").text(JSONobj.catalog_no);
          var newBodyText = $cardBody.append("p").attr("class", "card-text text-dark text-title m-0").text(JSONobj.colors);
          var newFooter = $card.append("div").attr("class", "card-footer text-muted py-0").text(JSONobj.manufacturer);
          newFooter.append('i').attr('class', 'fas fa-barcode ml-2');
        }
      }
    });
  });
}
