var manuf_select = document.getElementById("manufacturer");
var item_select = document.getElementById("item");

manuf_select.onchange = function () {

    manufacturer = manuf_select.value;

    fetch('/manufacturer/' + manufacturer).then(function (response) {

    response.json().then(function (data) {
        var optionHTML = '';
        for (var item of data.items) {
        optionHTML +=
            '<option value=" ' +
            item.id + ' ">' +
            item.catalog_no + '-' +
            item.color_primary + '-' +
            item.color_secondary +
            '</option>';
        }

        item_select.innerHTML = optionHTML;
    })

    });
}
