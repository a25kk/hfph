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
        var $mq = $('.marquee').marquee();
        $('#formfield-form-widgets-series input.checkbox-widget').on('click', function () {
            var inputId = this.id;
            if (inputId === 'form-widgets-series-5') {
                if ($(this).is(':checked')) {
                    $('#form-widgets-medium-1').attr('checked', true);
                }
            }
            else {
                if ($(this).is(':checked')) {
                    $('#form-widgets-medium-0').attr('checked', true);
                }
            }
        });
        $('div[data-appui="eventbox"]').each(function () {
            var sourceUrl = $(this).data('source');
            var targetEl = $(this);
            $.getJSON(sourceUrl, function (data) {
                var divData = '';
                $.each(data.items, function (i, item) {
                    //alert('Item:' + item.title);
                    divData += '<a class="app-box-item" href="' + item.url + '">';
                    divData += '<time class="app-box-date h5">' + item.date + '</time>';
                    divData += '<span>' + item.title + '</span>';
                    divData += '<span class="app-box-item-more text-right"><i class="icon-double-angle-right"></i></span>';
                    divData += '</a>';
                });
                targetEl.html(divData);
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