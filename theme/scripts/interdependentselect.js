define(["jquery",
], function($) {

    var selectComponent = {};

    var _defaults = {
        selector: 'js-module-selector'
    };

    function interdependentSelect(_options) {
        var options = $.extend({}, _defaults, _options);
        var $selectBoxes = $(options.selector),
            $filterActions = $(options.filterFormAction);
        $selectBoxes.each(function (){
            var $el = $(this);
            $el.on('change', function(e) {
                console.log('Element changed');
                var $selectedValue = $(this).find(":selected").val(),
                    $connectedSelect = $(this).data('target-list'),
                    $selectorType = $(this).data('selector');
                if ($selectorType === 'master') {
                    // Hide all visible selects on change
                    var $visibleBoxes = $('.' + options.classVisible.split(' ', 1));
                    $visibleBoxes.addClass(options.classHidden);
                    $visibleBoxes.removeClass(options.classVisible);
                    if ($selectedValue !== 'ba') {
                        var $targetSelectorId = $connectedSelect + '--master';
                    } else {
                        var $targetSelectorId = $connectedSelect + '--bachelor';
                    }
                } else {
                    var $targetSelectorId = $connectedSelect;
                }
                var $targetSelector = $($targetSelectorId);
                $targetSelector.removeClass(options.classHidden);
                $targetSelector.addClass(options.classVisible);
                // Handle additional course theme select boxes
                if ($selectedValue !== 'ba') {
                    var $themeSelectorId = options.themeSelectorBaseId + $selectedValue,
                        $themeSelector = $($themeSelectorId);
                    $themeSelector.addClass(options.classVisible);
                    $themeSelector.removeClass(options.classHidden);
                }
                // Show actions after successful selection
                $filterActions.each(function() {
                    var $el = $(this);
                    $el.removeClass(options.filterFormActionHidden);
                    $el.addClass(options.filterFormActionVisible);
                });
            })
        });
    }

    selectComponent.init = function (_options) {
        // Initialize here
        var options = $.extend({}, _defaults, _options);
        return interdependentSelect(options);
    };

    // return init;
    return selectComponent;

});
