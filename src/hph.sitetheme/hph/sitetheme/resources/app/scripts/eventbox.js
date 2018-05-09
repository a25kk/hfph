define(["jquery",
], function($) {

    var eventBox = {};

    var _defaults = {
        eventBoxIdentifier: '[data-appui="eventbox"]',
    };

    function eventLoader(_options, callback) {
        var options = $.extend({}, _defaults, _options);
        var eventBoxes = Array.prototype.slice.call(document.querySelectorAll(options.eventBoxIdentifier));
        eventBoxes.forEach(function(eventBox) {
            var sourceUrl = eventBox.dataset.source,
                targetEl = eventBox;
            targetEl.innerHtml = '<div class="app-card__section"></div>'
            var request = new XMLHttpRequest();
            request.open('GET', sourceUrl, true);

            request.onload = function(e) {
                if (request.status >= 200 && request.status < 400) {
                    // Success!
                    var response = request.responseText,
                        returnData = JSON.parse(response);
                    console.log("Data: " + returnData.items);
                    if (returnData.items && returnData.items.length) {
                        var content = '';
                        returnData.items.forEach(function(item) {
                            content += '<a class="app-card-item app-card__item"  href="' + item.url + '">';
                            content += '<time class="app-card-date app-card__date h5">' + item.date + '</time>';
                            content += '<p>' + item.title + '</p>';
                            content += '</a>';
                        });
                        console.log(e);
                        targetEl.innerHtml += content;
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
        return eventLoader(options);
    };

    // return init;
    return eventBox;

});
