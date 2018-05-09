define(["jquery",
    ], function($) {

    var eventBox = {};

    var _defaults = {
        eventBoxIdentifier: '[data-appui="eventbox"]',
    };

    function eventLoader(_options, callback) {
        var options = $.extend({}, _defaults, _options);
        var eventBoxes = Array.prototype.slice.call(document.querySelectorAll(options.eventBoxIdentifier));
        eventBoxes.forEach(function(element) {
            var sourceUrl = element.dataset.source,
                targetEl = element;
            var request = new XMLHttpRequest();
            request.open('GET', sourceUrl, true);

            request.onload = function() {
                if (request.status >= 200 && request.status < 400) {
                    // Success!
                    var response = request.responseText,
                        returnData = JSON.parse(response);
                    console.log("Data: " + response);
                    if (returnData !== null) {
                        var content = '';
                        returnData.forEach(function(item) {
                            content += '<a class="app-card-item app-card__item"  href="' + item.url + '">';
                            content += '<time class="app-card-date app-card__date h5">' + item.date + '</time>';
                            content += '<p>' + item.title + '</p>';
                            content += '</a>';
                        });
                        element.innerHtml(content);
                    }
                    // callback(JSON.parse(response), element);
                } else {
                    // We reached our target server, but it returned an error
                    console.log('Events could not be retrieved.')
                }
            };

            request.onerror = function() {
                // There was a connection error of some sort
                console.log('Connection error while retrieving events.')
            };

            request.send();
        });
    }

    eventBox.my_method = function () {
        // do something
    }

    eventBox.init = function (_options) {
        // Initialize here
        var options = $.extend({}, _defaults, _options);
        return eventLoader(options, function(returnData, element) {
            console.log(typeof(returnData));
            if (returnData !== null) {
                var content = '';
                returnData.forEach(function(item) {
                    content += '<a class="app-card-item app-card__item"  href="' + item.url + '">';
                    content += '<time class="app-card-date app-card__date h5">' + item.date + '</time>';
                    content += '<p>' + item.title + '</p>';
                    content += '</a>';
                });
                element.innerHtml(content);
            }
        });
    };

    // return init;
    return eventBox;

});
