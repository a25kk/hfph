define(["jquery",
], function($) {

    var slider = {};

    var _defaults = {
        sliderElement: 'js-gallery',
        autoPlay: true,
        contain: true,
        wrapAround: true,
        imagesLoaded: true,
        cellSelector: '.app-gallery-cell',
        cellAlign: 'left'
    };

    function extend_defaults(){
        for(var i=1; i<arguments.length; i++)
            for(var key in arguments[i])
                if(arguments[i].hasOwnProperty(key)) {
                    if (typeof arguments[0][key] === 'object'
                        && typeof arguments[i][key] === 'object')
                        extend(arguments[0][key], arguments[i][key]);
                    else
                        arguments[0][key] = arguments[i][key];
                }
        return arguments[0];
    }

    function itemSlider(element, options) {
        var flickitySlider = new Flickity(element, options);
        element.classList.add('app-banner--loaded');
    }

    function initializeSlider(options) {
        // Nav bar toggle
        var sliderInstances = Array.prototype.slice.call(document.querySelectorAll(options.sliderElement));
        sliderInstances.forEach(function(el) {
            itemSlider(el, options);
        });
    }

    slider.init = function (_options) {
        // Initialize here
        var options = extend_defaults(_defaults, _options);
        return initializeSlider(options);
    };

    // return init;
    return slider;

});
