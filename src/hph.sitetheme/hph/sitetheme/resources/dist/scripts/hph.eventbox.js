define(["jquery",
    ], function($) {

    var eventLoader = {
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
    }

    var initialize = function(options) {
        return eventLoader;
    }

    return {
        init: initialize
    };
});
