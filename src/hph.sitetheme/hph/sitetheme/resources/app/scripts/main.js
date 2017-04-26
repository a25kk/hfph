'use strict';
(function ($) {
    $(document).ready(function () {
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
                    divData += '<a class="app-card-item app-card__item"  href="' + item.url + '">';
                    divData += '<time class="app-card-date app-card__date h5">' + item.date + '</time>';
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
            // Anonymous only scripts (mainly used in login views)
            if ($(".userrole-anonymous")[0]){
                $('input[type="password"]').showPassword('focus', {
                });
                $('.app-signin-input').jvFloat();
                var $mcNote = $('#app-signin-suggestion');
                Mailcheck.defaultDomains.push('eda.kreativkombinat.de')
                $('#ac-name').on('blur', function (event) {
                    console.log("event ", event);
                    console.log("this ", $(this));
                    $(this).mailcheck({
                        // domains: domains,                       // optional
                        // topLevelDomains: topLevelDomains,       // optional
                        suggested: function (element, suggestion) {
                            // callback code
                            console.log("suggestion ", suggestion.full);
                            $mcNote.removeClass('hidden').addClass('fadeInDown');
                            $mcNote.html("Meinten Sie <i>" + suggestion.full + "</i>?");
                            $mcNote.on('click', function (evt) {
                                evt.preventDefault();
                                $('#ac-name').val(suggestion.full);
                                $mcNote.removeClass('fadeInDown').addClass('fadeOutUp').delay(2000).addClass('hidden');
                            });
                        },
                        empty: function (element) {
                            // callback code
                            $mcNote.html('').addClass('hidden');
                        }
                    });
                });
                // Setup media query for enabling dynamic layouts only on
                // larger screen sizes
                var mq = window.matchMedia("(min-width: 480px)");
                if (mq.matches) {
                    // Enable e.g. masonry scripts based on available screen size
                }
            };
        }
    );
}(jQuery));
