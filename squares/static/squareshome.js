/* eslint-disable no-trailing-spaces */
/* eslint-disable no-console */
/* eslint-disable linebreak-style */
/* eslint-disable no-shadow */
/* eslint-disable linebreak-style */
/* eslint-disable no-undef */
/* eslint-disable linebreak-style */
/* eslint-disable no-use-before-define */

for (let index = 0; index < 10; index += 1) {
  initMouseOver(index);
}

updateByDefault();


function initMouseOver(squareID) {  
  d3.select(`#squareButton0${squareID}`)
  .on('mouseenter', gridViewUp(squareID))
  .on('mouseleave', gridViewDown());
  
}

function gridViewDown() {
  return function () {
    d3.selectAll('.card-deck').remove();
    console.log(`---- grid View DOWN ----`);
  };
}

function gridViewUp(squareID) {
  return function () {
    d3.selectAll('.card-deck').remove();
    gridView(squareID);
    console.log(` ---- grid View UP ----${squareID}----`);
  };
}

const $squareSel3ct = document.getElementById('opts');

$squareSel3ct.onchange = function () {
  d3.selectAll('.card-deck').remove();
  const square = $squareSel3ct.value;
  gridView(square);
  infoBoardSquare(square);
  infoBoardAvlbCount(square);
  infoBoardAvlbPerc(square);
  infoBoardManuf(square);
  infoBoardMostCommon(square);
};

function updateByDefault() {
  gridView(1);
  infoBoardSquare(1);
  infoBoardAvlbCount(1);
  infoBoardAvlbPerc(1);
  infoBoardManuf(1);
  infoBoardMostCommon(1);
}

function infoBoardSquare(square) {
  const queryURL = `/fetch/square/info/${square}`;
  d3.json(queryURL, (error, response) => {
    if (error) {
      return console.warn(error);
    }
    var squareJSON = response.data[0];
    d3.select('#squareID').text(squareJSON.id).attr('class', 'text-primary').style('font-size', '1rem');
    d3.select('#squareName').text(squareJSON.name).attr('class', 'text-light');
    d3.select('#rowCount').text(squareJSON.row_count).attr('class', 'text-primary').style('font-size', '1rem');
    d3.select('#colCount').text(squareJSON.col_count).attr('class', 'text-primary').style('font-size', '1rem');
    const squareArea = squareJSON.row_count * squareJSON.col_count;
    d3.select('#squareArea').text(squareArea).attr('class', 'text-primary').style('font-size', '1rem');
  });
}

function infoBoardAvlbCount(square) {
  const queryURL = `/fetch/main/avlb/count/${square}`;
  d3.json(queryURL, (error, response) => {
    if (error) {
      return console.warn(error);
    }
    d3.select('#avlbItemsCount').text(response).attr('class', 'text-primary').style('font-size', '1rem');
  });
}

function infoBoardAvlbPerc(square) {
  const queryURL = `/fetch/main/avlb/perc/${square}`;
  d3.json(queryURL, (error, response) => {
    if (error) {
      return console.warn(error);
    }

    d3.select('#avlbItemsPerc').text(`${response}%`).style('font-size', '1rem');
  });
}

function infoBoardManuf(square) {
  const queryURL = `/fetch/manuf/info/${square}`;
  d3.json(queryURL, (error, response) => {
    if (error) {
      return console.warn(error);
    }
    const mainArray = response.main;
    const dispArray = response.disp;
    innerMain = '';
    for (let i = 0; i < mainArray.length; i += 1) {
      const pairJSON = mainArray[i];
      innerMain += `${pairJSON.manufacturer}: ${pairJSON.percentage}%  `;
    }
    d3.select('#manufMain').text(innerMain);
    innerDisp = '';
    for (let i = 0; i < dispArray.length; i += 1) {
      const pairJSON = dispArray[i];
      innerDisp += `${pairJSON.manufacturer}: ${pairJSON.percentage}%  `;
    }
    d3.select('#manufDisp').text(innerDisp);
  });
}

function infoBoardMostCommon(square) {
  const queryURL = `/itemattr/mostcommon/${square}`;
  d3.json(queryURL, (error, response) => {
    if (error) {
      return console.warn(error);
    }
    const dispArray = response.disp;
    const mainArray = response.main;
    innerDisp = '';
    for (let i = 0; i < dispArray.length; i += 1) {
      const pairJSON = dispArray[i];
      innerDisp += `${pairJSON.count} ${pairJSON.attribute}`;
    }
    d3.select('#dispMostCommon').text(innerDisp);
    innerMain = '';
    for (let i = 0; i < mainArray.length; i += 1) {
      const pairJSON = mainArray[i];
      innerMain += `${pairJSON.count} ${pairJSON.attribute}`;

    }
    d3.select('#mainMostCommon').text(innerMain);

  });
}


function gridView(square) {
  const squareURL = `/fetch/square/info/${square}`;
  d3.json(squareURL, (response) => {
    const squareJSON = response.data[0];
    const queryURL = `/fetch/d3/grid/${square}`;
    const $grid = d3.select('.grid');

    d3.json(queryURL, (data) => {
      for (let index = 0; index < squareJSON.row_count; index += 1) {
        const row = data[index];
        const $cardDeck = $grid.append('div').attr('class', 'card-deck mt-2 px-0');
        for (let i = 0; i < row.length; i += 1) {
          const JSONobj = row[i];
          
          const $card = $cardDeck.append('div')
            .attr('class', 'card bg-dark border-success shadow-gold text-center mx-1 my-2').style('border-radius','16px').style('border-width','2px');

          const newHeader = $card.append('div').attr('class', 'card-header text-success py-1').text(JSONobj.unique_tag);

          newHeader.append('i').attr('class', 'fa fa-tag ml-2');
          

          const newImg = $card.append('img').attr('class', 'card-img-top bg-white border-none mt-2').style('border-radius', '4px').attr('src', JSONobj.imageSrc);

          const $cardBody = $card.append('div').attr('class', 'card-body text-center p-0');

          const $containerFluid = $cardBody.append('div').attr('class', 'container-fluid');

          const newButton = $containerFluid.append('a').attr('class', 'btn btn-dark btn-block btn-grid border-success text-light px-2 py-0').append('em').text(JSONobj.catalog_no);

          const newBodyTitle = $cardBody.append('h6').attr('class', 'card-title text-secondary text-title mb-0 mt-0').append('small').append('em').text(JSONobj.colors);

          const newFooter = $card.append('div').attr('class', 'card-footer border-success text-success py-1').append('small').append('em').text(JSONobj.manufacturer);

          newFooter.append('i').attr('class', 'fas fa-barcode ml-2');
        }
      }
    });
  });
}                   

