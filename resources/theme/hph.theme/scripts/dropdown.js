define([
    "jquery",
    "/scripts/utils.js"
], function($, utils) {

    var dropDown = {};

    var _defaults = {
        dropDownToggle: '.js-dropdown-toggle',
        dropDownToggleActive: 'js-dropdown-toggle--active',
        dropDownElement: '.js-dropdown',
        dropDownActiveMarker: 'o-dropdown--active'
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
        element.classList.toggle(options.dropDownToggleActive);
        var dropDownIdentifier = element.dataset.dropdown,
            dropDown = document.getElementById(dropDownIdentifier);
        dropDown.classList.toggle(options.dropDownActiveMarker);
    }

    function initializeDropDown(options) {
        // Nav bar toggle
        var dropDownToggle = Array.prototype.slice.call(document.querySelectorAll(options.dropDownToggle)),
            dropDownElement = Array.prototype.slice.call(document.querySelectorAll(options.dropDownElement));
        dropDownToggle.forEach(function(el) {
            el.addEventListener("click", function(event) {
                event.preventDefault();
                dropDownHandler(el, options);
            })
        });
        dropDownElement.forEach(function(el) {
            console.log('Add click outside handler');
            // utils.handleClickOutside(el, options.dropDownActiveMarker);
        })
    }

    dropDown.init = function (_options) {
        // Initialize here
        var options = utils.extendDefaultOptions(_defaults, _options);
        return initializeDropDown(options);
    };

    // return init;
    return dropDown;

});
