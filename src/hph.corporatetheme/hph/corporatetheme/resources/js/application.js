/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false, window:false, location:false */

(function ($) {
    $(document).ready(function () {
        if (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7) {
            // it's not realistic to think we can deal with all the bugs
            // of IE 6 and lower. Fortunately, all this is just progressive
            // enhancement.
            return;
        }
        if ($(".bs-docs-top").length > 0) {
            setTimeout(function () {
                $('.bs-docs-top').affix();
            }, 100);
        }
        //$("#ticker-tabs").tabs('#bulletins > div', {
        //    effect: 'fade',
        //    fadeOutSpeed: 1000,
        //    rotate: true
        //}).slideshow({
        //    autoplay: true,
        //    interval: 6000,
        //    clickable: false
        //});
        $('#formfield-form-widgets-series input.checkbox-widget').on('click', function () {
            var input_id = this.id;
            if (input_id === 'form-widgets-series-5') {
                alert('We have the correct id');
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
        if ($("#tickerbar").length > 0) {
            $('div[data-appui="tickerfeed"]').each(function () {
                var source_url = $(this).data('appui-source');
                $.getJSON(source_url, function (data) {
                    $.each(data.items, function (i, item) {
                        var unique_id = $.gritter.add({
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
            var source_url = $(this).data('source');
            var target_el = $(this);
            $.getJSON(source_url, function (data) {
                var div_data = '';
                $.each(data.items, function (i, item) {
                    //alert('Item:' + item.title);
                    div_data += '<a class="app-box-item" href="' + item.url + '">';
                    div_data += '<time>' + item.date + '</time>';
                    div_data += '<span>' + item.title + '</span>';
                    div_data += '<span class="app-box-item-more text-right"><i class="icon-double-angle-right"></i></span>';
                    div_data += '</a>';
                });
                target_el.html(div_data);
            });
        });
    });
}(jQuery));
