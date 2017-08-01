var font = new FontFaceObserver('Open Sans');
font.load().then(function () {
    document.documentElement.className += " app-fonts-loaded";
});


// Warning Duplicate IDs
var ids = {};
var found = false;
$('[id]').each(function() {
    if (this.id && ids[this.id]) {
        found = true;
        console.warn('Duplicate ID #'+this.id);
    }
    ids[this.id] = 1;
});
if (!found) console.log('No duplicate IDs found');

// $('.js-ticker').marquee({ speed: 5000 });
// Integrate carousel for news ticekr content
var $tickerBar = document.querySelectorAll('.js-ticker');
if ($tickerBar.length) {
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

// Interdependent selection boxes
var _interdependent_select_defaults = {
    selector: 'js-module-selector'
};
function interdependentSelect(_options) {
    var options = $.extend({}, _interdependent_select_defaults, _options);
    var $selectBoxes = $(options.selector),
        $filterActions = $(options.filterFormAction);
    $selectBoxes.each(function (){
        var $el = $(this);
        $el.on('change', function(e) {
            var $selectedValue = $(this).find(":selected").val(),
                $connectedSelect = $(this).data('target-list'),
                $selectorType = $(this).data('selector');
            if ($selectorType === 'master') {
                // Hide all visible selects on change
                var $visibleBoxes = $('.' + options.classVisible.split(' ', 1));
                console.log($visibleBoxes);
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
                console.log($themeSelectorId);
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

// Default interdependent select boxes used in module editor
var _selector_defaults = {
    selector: '.js-module-selector',
    classVisible: 'module__select--visible fadeInDown',
    classHidden: 'module__select--hidden fadeOutUp',
    themeSelectorBaseId: '#selector__core-theme--',
    filterFormAction: '.js-filter-action',
    filterFormActionHidden: 'filter__block--hidden',
    filterFormActionVisible: 'filter__block--visible'
};
interdependentSelect(_selector_defaults);

// Course filter select boxes
var _selector_filter = {
    selector: '.js-filter-box',
    classVisible: 'form-field__select--visible fadeIn',
    classHidden: 'form-field__select--hidden fadeOut',
    themeSelectorBaseId: '#selector__core-theme--',
    filterFormAction: '.js-filter-action',
    filterFormActionHidden: 'filter__block--hidden',
    filterFormActionVisible: 'filter__block--visible'
};
interdependentSelect(_selector_filter);

// var $moduleSelectorClass = '.js-module-selector';
// interdependentSelect($moduleSelectorClass);


var $ajaxContainer = $('#appui-container');
$('div[data-appui="ajaxified"]').each(function () {
    var $wrapper = $(this).parent(),
        $sourceUrl = $(this).data('appui-target');
    $(this).load($sourceUrl + '&ajax_load=1 #content-core >*');
});
$('a[data-appui="pjaxed"]').each(function () {
    var $targetUrl = $(this).attr('href'), $hideEl = $(this).data('appui-hide');
    $(this).on('click', function (e) {
        e.preventDefault();
        $(this).addClass('selected');
        $('#app-box-footer').removeClass('hide').addClass('show');
        $($hideEl).hide();
        $ajaxContainer.load($targetUrl + '?ajax_load=1 #content-core >*').fadeIn('slow');
    });
});
$('div[data-appui="eventbox"]').each(function () {
    var $sourceUrl = $(this).data('source'), $targetEl = $(this);
    $.getJSON($sourceUrl, function (data) {
        var divData = '';
        $.each(data.items, function (i, item) {
            divData += '<a class="app-card-item app-card__item" href="' + item.url + '">';
            divData += '<time class="app-card-date app-card__date">' + item.date + '</time>';
            divData += '<p>' + item.title + '</p>';
            divData += '</a>';
        });
        $targetEl.html(divData);
    });
});
$('a[data-appui="overslide"]').on({
    click: function (e) {
        e.preventDefault();
        var targetBlock = $(this).data('target');
        if ($(targetBlock).hasClass('fadeOutTop')) {
            $(targetBlock).removeClass('fadeOutTop').addClass('slideInRight').show();
        } else {
            $(targetBlock).addClass('slideInRight').show();
        }
    }
});
$('a[data-appui="overslide-close"]').on({
    click: function (e) {
        e.preventDefault();
        $(this).closest('.panelpage-slide').removeClass('slideInRight').addClass('fadeOutTop').hide();
    }
});
$('a[data-appui="contextmenu"]').on({
    click: function (e) {
        e.preventDefault();
        var $contextMenu = $(this).data('target');
        $($contextMenu).toggleClass('cbp-spmenu-open');
    }
});
$('a[data-appui="contextmenu-close"]').on({
    click: function (e) {
        e.preventDefault();
        $(this).closest('.cbp-spmenu').removeClass('cbp-spmenu-open');
    }
});
$('a[data-appui="modal"]').on({
    click: function (e) {
        e.preventDefault();
        var $modal = $(this).data('target');
        $modal.on('show.bs.modal', function () {
            var $modalBody = $(this).find('.modal-body');
            $modalBody.load(e.currentTarget.href);
        })
            .modal();
    }
});
$('a[data-appui="ajaxified"]').each(function () {
    var $targetUrl = $(this).data('source'),
        $container = $(this).data('target');
    $($container).load($targetUrl + '?ajax_load=1 #content-core >*')
        .fadeIn('slow');
});

$('div[data-appui="editable"]').on({
    mouseenter: function () {
        $(this).find('.contentpanel-editbar')
            .removeClass('fadeOutUp')
            .addClass('fadeInLeft')
            .show();
    },
    mouseleave: function () {
        $(this).find('.contentpanel-editbar')
            .removeClass('fadeInLeft')
            .addClass('fadeOutUp');
    }
});

// var $sortableSection = $('.ppe-section-sortable').sortable({
//     items: '.ppe-block-sortable',
//     handle: '.ppe-dragindicator'
// });

// if ($sortableSection.length) {
//     $sortableSection.on('sortupdate', function () {
//         var $ajaxTarget = $sortableSection.data('appui-ajax-uri'),
//             $data = $('#ppe-form-rearrange').serializeArray();
//         $.ajax({
//             url: $ajaxTarget,
//             data: $data,
//             context: document.body,
//             success: function (data) {
//                 if (data.success === true) {
//                     var $message = data.message,
//                         $htmlString = '<p class="text-warning">' + $message + '</p>';
//                     $('#ppe-statusinfo-content').append($htmlString).removeClass('hidden').slideDown('slow');
//                 } else {
//                     // This could be nicer in the future...
//                     console.log('Form could not be submitted. Bummer.');
//                 }
//             }
//         });
//     });
// }
// Anonymous only scripts (mainly used in login views)
if ($(".userrole-anonymous")[0]) {
    // Show password by default
    $('input[type="password"]').hideShowPassword(true, 'focus');
    //$('input[type="password"]').showPassword('focus', {});
    // Float labels (requires corresponding css)
    $('.app-signin-input').jvFloat();

};
