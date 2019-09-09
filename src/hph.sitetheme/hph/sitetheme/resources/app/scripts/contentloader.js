define([
    "/scripts/utils.js"
], function(utils) {

    var contentLoader = {};

    var _defaults = {
        contentLoadElement: 'js-content-loader',
        contentLoaderSource: 'data-source-url',
        contentLoaderTargetElement: 'data-target-element'
    };

    function loadContent(_options, callback) {
        var options = $.extend({}, _defaults, _options);
        var eventBoxes = Array.prototype.slice.call(document.querySelectorAll(options.eventBoxIdentifier));
        eventBoxes.forEach(function(eventBox) {
            var sourceUrl = eventBox.dataset.source,
                targetEl = eventBox;
            var request = new XMLHttpRequest();
            request.open('GET', sourceUrl, true);

            request.onload = function(e) {
                if (request.status >= 200 && request.status < 400) {
                    // Success!
                    var response = request.responseText;
                    // callback(JSON.parse(response), element);
                    // TODO: add external content to target element
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

    function initializeContentLoader(options) {
        let loader = Array.prototype.slice.call(document.querySelectorAll(options.contentLoadElement));
        // Loader event listener
        loader.forEach(function(el) {
            el.addEventListener("click", function(event) {
                event.preventDefault();
                event.stopPropagation();
                loadContent(el, options);
            })
        });
    }

    contentLoader.init = function (_options) {
        // Initialize here
        let options = utils.extendDefaultOptions(_defaults, _options);
        return initializeContentLoader(options);
    };

    // return init;
    return contentLoader;

});
