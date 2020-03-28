var csvParse = function() {

    // put you document url here
    var sharedDocUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQmVcTUa06oJ97wiqrFruAvDsX89YzdZRRP_prnkPPky6oQxD-CCQ2NKrP3notA6gnhP3c-C_9qDX-y/pubhtml'

    // can also be only the ID
    // var sharedDocUrl = '1Rk9RMD6mcH-jPA321lFTKmZsHebIkeHx0tTU0TWQYE8'

    var targetDiv = 'csvDatas';

    // holds datas at a closure level
    // this then can be accessed by closure's functions
    var dataObj;

    function showInfo(data, tabletop) {
        dataObj    = data;
        var table  = generateTable();
        var target = document.getElementById(targetDiv);
        target.appendChild(table);
    }

    function generateTable(){
        var table = document.createElement("table");
        var head  = generateTableHeader();
        table.appendChild(head);
        var body  = generateTableBody();
        table.appendChild(body);
        return table;
    }

    function generateTableHeader(){
        var d         = dataObj[0];
        var tHead     = document.createElement("thead");
        var colHeader = [];
        $.each(d, function( index, value){
            console.log(index + ' : ' + value);
            colHeader.push(index);
        });
        var row = generateRow(colHeader, 'th');
        tHead.appendChild(row);
        return tHead;
    }

    // this can be factorized with generateTableHeader
    function generateTableBody(){
        var tBody = document.createElement("tbody");
        $.each(dataObj, function( index, value ){
            var rowVals = [];
            $.each(value, function(colnum, colval){
                rowVals.push(colval);
            });
            var row = generateRow(rowVals);
            tBody.appendChild(row);
        });
        return tBody;
    }

    function generateRow(headersArray, cellTag){
        cellTag = typeof cellTag !== 'undefined' ? cellTag : 'td';
        var row = document.createElement("tr");
        $.each(headersArray, function( index, value){
            if( value != "rowNumber"){
                var cell     = document.createElement(cellTag);
                var cellText = document.createTextNode(value);
                cell.appendChild(cellText);
                row.appendChild(cell);
            }
        });
        return row;
    }

    return {
        init: function() {

            if( $('#' + targetDiv).length ){
                Tabletop.init( { key: sharedDocUrl  ,
                         callback: showInfo,
                         simpleSheet: true } );
            }else{
                console.log('Not the good page to parse csv datas');
            }
        }
    };
}();

$( document ).ready(function() {
    csvParse.init();
});