if (typeof a25 == "undefined") var a25 = {};

a25.carousel = (function($, undefined) {
    "use strict";

    var _defaults = {
        tickerBarClass: ".app-ticker",
    };

    function init(_options) {
        tickerBar(_options);
    }

    function tickerBar(_options) {
        var options = $.extend({}, _defaults, _options);
        var $tickerBar = document.querySelector(options.tickerBarClass);
        if ($tickerBar !== null) {
            var tickerflkty = new Flickity('.js-ticker', {
                autoPlay: 5000,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellSelector: '.app-marquee__item',
                cellAlign: 'left',
                selectedAttraction: 0.025,
                friction: 0.28,
                prevNextButtons: false
            });
        }
    }

    return {
        init: init
    };
})(jQuery);

jQuery(function() {
    a25.carousel.init();
});
