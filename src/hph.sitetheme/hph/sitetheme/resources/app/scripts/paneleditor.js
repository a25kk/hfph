define([
    "/scripts/utils.js"
], function(utils) {

    var panelEditor = {};

    var _defaults = {
        widgetSelectForm: 'js-widget-select-form',
        dropDownToggleActive: 'js-dropdown-toggle--active',
        dropDownElement: '.js-dropdown',
        dropDownActiveMarker: 'o-dropdown--active'
    };

    function widgetSelector(element, options) {
        let selectForm = document.querySelectorAll(options.widgetSelectForm);
        [].forEach.call(selectForm, function(element) {

        };
    }

    function initializePanelEditor(options) {
        // Widget Selector
        widgetSelector(options);

    }

    panelEditor.init = function (_options) {
        // Initialize here
        let options = utils.extendDefaultOptions(_defaults, _options);
        return initializePanelEditor(options);
    };

    // return init;
    return panelEditor;

});
