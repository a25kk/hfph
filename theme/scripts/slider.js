define([
    "/scripts/utils.js",
    "/scripts/flickity.pkgd.js"
], function(utils, Flickity) {

    var slider = {};

    var _defaults = {
        sliderElement: '.js-slider',
        autoPlay: true,
        contain: true,
        wrapAround: true,
        imagesLoaded: true,
        cellSelector: '.c-slide',
        cellAlign: 'left'
    };

    function itemSlider(element, options) {
        var flickitySlider = new Flickity(element, options);
        element.classList.add('c-slider--active');
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
        console.log('Initialized Slider');
        let options = utils.extendDefaultOptions(_defaults, _options);
        return initializeSlider(options);
    };

    // return init;
    return slider;

});
