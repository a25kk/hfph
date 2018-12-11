define(["jquery",
], function($) {

    var dropDown = {};

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

    function dropDownHandler(element, options) {
        element.classList.add('o-dropdown--active');
    }

    function initializeDropDown(options) {
        // Nav bar toggle
        var sliderInstances = Array.prototype.slice.call(document.querySelectorAll(options.sliderElement));
        sliderInstances.forEach(function(el) {
            el.addEventListener("click", function(event) {
                event.preventDefault();
                dropDownHandler(el, options);
            })

        });
    }

    dropDown.init = function (_options) {
        // Initialize here
        var options = extend_defaults(_defaults, _options);
        return initializeDropDown(options);
    };

    // return init;
    return dropDown;

});
