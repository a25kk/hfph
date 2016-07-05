requirejs(['require',
'/++theme++hph.sitetheme/dist/scripts/jquery.marquee.min.js',
'/++theme++hph.sitetheme/dist/scripts/html.sortable.min.js',
'/++theme++hph.sitetheme/dist/scripts/medium-editor.js',
'/++theme++hph.sitetheme/dist/scripts/fontfaceobserver.standalone.js',
'/++theme++hph.sitetheme/dist/scripts/hideShowPassword.js',
'/++theme++hph.sitetheme/dist/scripts/jvfloat.js',
'/++theme++hph.sitetheme/dist/scripts/respimage.js',
'/++theme++hph.sitetheme/dist/scripts/ls.parent-fit.js',
'/++theme++hph.sitetheme/dist/scripts/lazysizes-umd.js',],
 function(require) {
'use strict';
var font = new FontFaceObserver('Open Sans');
font.load().then(function () {
    document.documentElement.className += " app-fonts-loaded";
});
$('.js-ticker').marquee({ speed: 5000 });
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
            divData += '<a class="app-box-item" href="' + item.url + '">';
            divData += '<time class="app-box-date h5">' + item.date + '</time>';
            divData += '<span>' + item.title + '</span>';
            divData += '<span class="app-box-item-more text-right"><i class="icon-double-angle-right"></i></span>';
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
var $sortableSection = $('.ppe-section-sortable').sortable({
    items: '.ppe-block-sortable',
    handle: '.ppe-dragindicator'
});
if ($sortableSection.length) {
    $sortableSection.on('sortupdate', function () {
        var $ajaxTarget = $sortableSection.data('appui-ajax-uri'),
            $data = $('#ppe-form-rearrange').serializeArray();
        $.ajax({
            url: $ajaxTarget,
            data: $data,
            context: document.body,
            success: function (data) {
                if (data.success === true) {
                    var $message = data.message,
                        $htmlString = '<p class="text-warning">' + $message + '</p>';
                    $('#ppe-statusinfo-content').append($htmlString).removeClass('hidden').slideDown('slow');
                } else {
                    // This could be nicer in the future...
                    console.log('Form could not be submitted. Bummer.');
                }
            }
        });
    });
}
// Anonymous only scripts (mainly used in login views)
if ($(".userrole-anonymous")[0]) {
    // Show password by default
    $('input[type="password"]').hideShowPassword(true, 'focus');
    //$('input[type="password"]').showPassword('focus', {});
    // Float labels (requires corresponding css)
    $('.app-signin-input').jvFloat();

};
});