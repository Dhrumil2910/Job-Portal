$.ajaxCall = function(url, method, data, handleData) {
    var settings = {
        "async": true,
        "crossDomain": false,
        "url": url,
        "method": method,
        "contentType": "application/json",
        "data": data,
        xhrFields: {
            withCredentials: true
        },
        success: function(response) {
            handleData({"status": true, "output": response});
        },
        error: function(response) {
            handleData({"status": false, "output": response});
        }
    };
    
    $.ajax(settings);
}


$.ajaxCallaf = function(url, method, data, handleData) {
    var settings = {
        "async": false,
        "crossDomain": false,
        "url": url,
        "method": method,
        "contentType": "application/json",
        "data": data,
        xhrFields: {
            withCredentials: true
        },
        success: function(response) {
            handleData({"status": true, "output": response});
        },
        error: function(response) {
            handleData({"status": false, "output": response});
        }
    };
    
    $.ajax(settings);
}

// convert to CSV

function convertToCSV(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    var str = '';

    for (var i = 0; i < array.length; i++) {
        var line = '';
        for (var index in array[i]) {
            if (line != '') line += ','

            line += array[i][index];
        }

        str += line + '\r\n';
    }

    return str;
}


// export File
function exportCSVFile(headers, items, fileTitle) {
    if (headers) {
        items.unshift(headers);
    }

    // Convert Object to JSON
    var jsonObject = JSON.stringify(items);

    var csv = this.convertToCSV(jsonObject);

    var exportedFilenmae = fileTitle + '.csv' || 'export.csv';

    var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, exportedFilenmae);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", exportedFilenmae);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}