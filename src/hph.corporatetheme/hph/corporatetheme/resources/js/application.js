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
        //$('div[data-appui="tickerfeed"]').each(function () {
        //    var source_url = $(this).data('appui-source');
        //    var target_el = $(this).data('appui-placeholder');
        //    $.getJSON(source_url, function (data) {
        //        var div_data = '';
        //        $.each(data.items, function (i, item) {
        //            //alert('Item:' + item.title);
        //            div_data += '<div class="bulletin">';
        //            div_data += '<a href="' + item.url + '">' + item.title + '</a></div>';
        //        });
        //        $(target_el).html(div_data);
        //    });
        //    //var ticker = function() {
        //    //    setTimeout(function() {
        //    //        $(target_el).find('div:first').animate( {marginTop: '-4em'}, 500, function() {
        //    //            $(this).detach().appendTo(target_el).removeAttr('style');
        //    //        });
        //    //        ticker();
        //    //    }, 5000);
        //    //};
        //    //ticker();
        //});
    });
}(jQuery));
