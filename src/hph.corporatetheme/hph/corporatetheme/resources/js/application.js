/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false */
'use strict';

(function ($) {
    $(document).ready(function () {
        if ($('body').hasClass('lt-ie7')) {return; }
        // Application specific javascript code goes here
        if ($('.bs-docs-top').length > 0) {
            setTimeout(function () {
                $('.bs-docs-top').affix();
            }, 100);
        }
        $('.marquee').marquee({
            speed: 5000
        });
        var $ajaxContainer = $('#appui-container');
        $('a[data-appui="pjaxed"]').each(function () {
            var $targetUrl = $(this).attr('href'),
                $hideEl = $(this).data('appui-hide');
            $(this).on('click', function (e) {
                e.preventDefault();
                $(this).addClass('selected');
                $('#app-box-footer').removeClass('hide').addClass('show');
                $($hideEl).hide();
                $ajaxContainer.load($targetUrl + '?ajax_load=1 #content-core >*'
                    ).fadeIn('slow');
            });
        });
        $('div[data-appui="eventbox"]').each(function () {
            var $sourceUrl = $(this).data('source'),
                $targetEl = $(this);
            $.getJSON($sourceUrl, function (data) {
                var divData = '';
                $.each(data.items, function (i, item) {
                    //alert('Item:' + item.title);
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
                // $(this).parent().removeClass('bounceInLeft').addClass('bounceOutRight');
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
    }
    );
}(jQuery));