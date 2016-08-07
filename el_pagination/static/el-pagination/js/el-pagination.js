'use strict';

(function ($) {

    // Fix JS String.trim() function is unavailable in IE<9 #45
    if (typeof(String.prototype.trim) === "undefined") {
         String.prototype.trim = function() {
             return String(this).replace(/^\s+|\s+$/g, '');
         };
    }

    $.fn.endlessPaginate = function(options) {
        var defaults = {
            // Twitter-style pagination container selector.
            containerSelector: '.endless_container',
            // Twitter-style pagination loading selector.
            loadingSelector: '.endless_loading',
            // Twitter-style pagination link selector.
            moreSelector: 'a.endless_more',
            // Digg-style pagination page template selector.
            pageSelector: '.endless_page_template',
            // Digg-style pagination link selector.
            pagesSelector: 'a.endless_page_link',
            // Callback called when the user clicks to get another page.
            onClick: function() {},
            // Callback called when the new page is correctly displayed.
            onCompleted: function() {},
            // Set this to true to use the paginate-on-scroll feature.
            paginateOnScroll: false,
            // If paginate-on-scroll is on, this margin will be used.
            paginateOnScrollMargin : 1,
            // If paginate-on-scroll is on, it is possible to define chunks.
            paginateOnScrollChunkSize: 0
        },
            settings = $.extend(defaults, options);

        var getContext = function(link) {
            return {
                key: link.attr('rel').split(' ')[0],
                url: link.attr('href')
            };
        };

        return this.each(function() {
            var element = $(this),
                loadedPages = 1;

            // Twitter-style pagination.
            element.on('click', settings.moreSelector, function() {
                var link = $(this),
                    html_link = link.get(0),
                    container = link.closest(settings.containerSelector),
                    loading = container.find(settings.loadingSelector);
                // Avoid multiple Ajax calls.
                if (loading.is(':visible')) {
                    return false;
                }
                link.hide();
                loading.show();
                var context = getContext(link);
                // Fire onClick callback.
                if (settings.onClick.apply(html_link, [context]) !== false) {
                    var data = 'querystring_key=' + context.key;
                    // Send the Ajax request.
                    $.get(context.url, data, function(fragment) {
                        container.before(fragment);
                        container.remove();
                        // Increase the number of loaded pages.
                        loadedPages += 1;
                        // Fire onCompleted callback.
                        settings.onCompleted.apply(
                            html_link, [context, fragment.trim()]);
                    });
                }
                return false;
            });

            // On scroll pagination.
            if (settings.paginateOnScroll) {
                var win = $(window),
                    doc = $(document);
                doc.scroll(function(){
                    if (doc.height() - win.height() -
                        win.scrollTop() <= settings.paginateOnScrollMargin) {
                        // Do not paginate on scroll if chunks are used and
                        // the current chunk is complete.
                        var chunckSize = settings.paginateOnScrollChunkSize;
                        if (!chunckSize || loadedPages % chunckSize) {
                            element.find(settings.moreSelector).click();
                        } else {
                            element.find(settings.moreSelector).addClass('endless_chunk_complete');
                        }
                    }
                });
            }

            // Digg-style pagination.
            element.on('click', settings.pagesSelector, function() {
                var link = $(this),
                    html_link = link.get(0),
                    context = getContext(link);
                // Fire onClick callback.
                if (settings.onClick.apply(html_link, [context]) !== false) {
                    var page_template = link.closest(settings.pageSelector),
                        data = 'querystring_key=' + context.key;
                    // Send the Ajax request.
                    page_template.load(context.url, data, function(fragment) {
                        // Fire onCompleted callback.
                        settings.onCompleted.apply(
                            html_link, [context, fragment.trim()]);
                    });
                }
                return false;
            });
        });
    };

    $.endlessPaginate = function(options) {
        return $('body').endlessPaginate(options);
    };

})(jQuery);
