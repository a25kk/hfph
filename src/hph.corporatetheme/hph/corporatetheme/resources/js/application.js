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
        if ($('#tickerbar').length > 0) {
            $('div[data-appui="tickerfeed"]').each(function () {
                var sourceUrl = $(this).data('appui-source');
                $.getJSON(sourceUrl, function (data) {
                    $.each(data.items, function (i, item) {
                        $.gritter.add({
                            // (string | mandatory) the heading of the notification
                            title: '<i class="icon-info-sign"></i> Hinweis',
                            // (string | mandatory) the text inside the notification
                            text: item.title,
                            sticky: true,
                            time: 6000
                        });
                    });
                });
            });
        }
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
    }
    );
}(jQuery));