(function($) {
    "use strict";
    $.breakingNews = function(element, options) {

        var defaults = {
            effect      : 'scroll',
            direction   : 'ltr',
            height      : 40,
            fontSize    : "default",
            themeColor  : "default",
            background  : "default",
            borderWidth : 1,
            radius      : 2,
            source      : "html",
            rss2jsonApiKey: '',
            play        : true,
            delayTimer  : 4000,
            scrollSpeed : 2,
            stopOnHover : true,
            position    : 'auto',
            zIndex      : 99999
        }

        var ticker = this;
        ticker.settings = {};
        ticker._element = $(element);

        //var ticker._element = $(element);
        //var element = element;
        
        ticker._label = ticker._element.children(".bn-label"),
        ticker._news = ticker._element.children(".bn-news"),
        ticker._ul = ticker._news.children("ul"),
        ticker._li = ticker._ul.children("li"),
        ticker._controls = ticker._element.children(".bn-controls"),
        ticker._prev = ticker._controls.find(".bn-prev").parent(),
        ticker._action = ticker._controls.find(".bn-action").parent(),
        ticker._next = ticker._controls.find(".bn-next").parent();

        ticker._pause = false;
        ticker._controlsIsActive = true;
        ticker._totalNews = ticker._ul.children("li").length;
        ticker._activeNews = 0;
        ticker._interval = false;
        ticker._frameId = null;

        /****************************************************/
        /**PRIVATE METHODS***********************************/
        /****************************************************/
        var initializeSettings = function() {
            if (ticker.settings.position === 'fixed-top')
                ticker._element.addClass('bn-fixed-top').css({'z-index': ticker.settings.zIndex});
            else if (ticker.settings.position === 'fixed-bottom')
                ticker._element.addClass('bn-fixed-bottom').css({'z-index': ticker.settings.zIndex});

            if (ticker.settings.fontSize != 'default')
            {
                ticker._element.css({
                    'font-size'     : ticker.settings.fontSize
                });
            }

            if (ticker.settings.themeColor != 'default')
            {
                ticker._element.css({
                    'border-color'  : ticker.settings.themeColor,
                    'color'         : ticker.settings.themeColor
                });

                ticker._label.css({
                    'background'    : ticker.settings.themeColor
                });
            }

            if (ticker.settings.background != 'default')
            {
                ticker._element.css({
                    'background'    : ticker.settings.background
                });
            }

            ticker._element.css({
                'height'        : ticker.settings.height,
                'line-height'   : (ticker.settings.height-(ticker.settings.borderWidth*2))+'px',
                'border-radius' : ticker.settings.radius,
                'border-width'  : ticker.settings.borderWidth
            });

            
            ticker._li.find('.bn-seperator').css({
                'height': ticker.settings.height-(ticker.settings.borderWidth*2)
            });
                    
        }

        var setContainerWidth = function(){
            if (ticker._label.length > 0){
                if (ticker.settings.direction == 'rtl')
                    ticker._news.css({"right":ticker._label.outerWidth()});
                else
                    ticker._news.css({"left":ticker._label.outerWidth()});
            }

            if (ticker._controls.length > 0){
                var controlsWidth = ticker._controls.outerWidth();
                if (ticker.settings.direction == 'rtl')
                    ticker._news.css({"left":controlsWidth});
                else
                    ticker._news.css({"right":controlsWidth});
            }    

            if (ticker.settings.effect === 'scroll')
            {
                var totalW = 0;
                ticker._li.each(function(){
                    totalW += $(this).outerWidth();
                });
                totalW += 50;
                ticker._ul.css({'width':totalW});
            }
        }

        var loadDataWithRSS2JSON = function(){
            var xhr = new XMLHttpRequest();

            xhr.onreadystatechange = function(){
                if (xhr.readyState==4 && xhr.status==200)
                {
                    var obj = JSON.parse(xhr.responseText);
                    var items = '';
                    var showingField = '';
                    switch (ticker.settings.source.showingField){
                        case 'title':
                            showingField = 'title';
                            break;
                        case 'description':
                            showingField = 'description';
                            break;
                        case 'link':
                            showingField = 'link';
                            break;
                        default:
                            showingField = 'title';
                    }
                    var seperator = '';
                    if (typeof ticker.settings.source.seperator != 'undefined' && typeof ticker.settings.source.seperator !== undefined)
                        seperator = ticker.settings.source.seperator;


                    for (var i = 0; i < obj.items.length; i++){
                        if (ticker.settings.source.linkEnabled)
                            items += '<li><a target="'+ticker.settings.source.target+'" href="'+obj.items[i].link+'">'+seperator+obj.items[i][showingField]+'</a></li>';
                        else
                            items += '<li><a>'+seperator+obj.items[i][showingField]+'</a></li>';
                    }
                    ticker._ul.empty().append(items);
                    ticker._li = ticker._ul.children("li");
                    ticker._totalNews = ticker._ul.children("li").length;
                    setContainerWidth();
                    if (ticker.settings.effect != 'scroll')
                        showThis();

                    ticker._li.find('.bn-seperator').css({
                        'height': ticker.settings.height-(ticker.settings.borderWidth*2)
                    });

                    playHandler();
                }
            };
            xhr.open(
                'GET',
                'https://api.rss2json.com/v1/api.json?rss_url='+ticker.settings.source.url+'&count='+ticker.settings.source.limit+'&api_key='+ticker.settings.source.rss2jsonApiKey,
                true
            );
            xhr.send();
        }

        var loadDataWithYQL = function(){
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open('GET', 'https://query.yahooapis.com/v1/public/yql?q='+encodeURIComponent('select * from rss where url="'+ticker.settings.source.url+'" limit '+ticker.settings.source.limit)+'&format=json', true);
            xmlhttp.onreadystatechange = function() {
                if (xmlhttp.readyState == 4) {
                    if(xmlhttp.status == 200) {
                        var obj = JSON.parse(xmlhttp.responseText);
                        var items = '';
                        var showingField = '';
                        switch (ticker.settings.source.showingField){
                            case 'title':
                                showingField = 'title';
                                break;
                            case 'description':
                                showingField = 'description';
                                break;
                            case 'link':
                                showingField = 'link';
                                break;
                            default:
                                showingField = 'title';
                        }
                        var seperator = '';
                        if (ticker.settings.source.seperator != 'undefined' && ticker.settings.source.seperator !== undefined)
                            seperator = ticker.settings.source.seperator;

                        for (var i = 0; i < obj.query.results.item.length; i++){
                            if (ticker.settings.source.linkEnabled)
                                items += '<li><a target="'+ticker.settings.source.target+'" href="'+obj.query.results.item[i].link+'">'+seperator+obj.query.results.item[i][showingField]+'</a></li>';
                            else
                                items += '<li><a>'+seperator+obj.query.results.item[i][showingField]+'</a></li>';
                        }
                        ticker._ul.empty().append(items);
                        ticker._li = ticker._ul.children("li");
                        ticker._totalNews = ticker._ul.children("li").length;
                        setContainerWidth();
                        if (ticker.settings.effect != 'scroll')
                            showThis();

                        ticker._li.find('.bn-seperator').css({
                            'height': ticker.settings.height-(ticker.settings.borderWidth*2)
                        });

                        playHandler();
                    }
                    else
                        ticker._ul.empty().append('<li><span class="bn-loader-text">'+ticker.settings.source.errorMsg+'</span></li>');
                }
            };
            xmlhttp.send(null);
        }

        var loadJSON = function(){
            $.getJSON( ticker.settings.source.url, function( data ) {
                var items = '';

                var showingField = '';
                if (ticker.settings.source.showingField === 'undefined')
                    showingField = 'title';
                else
                    showingField = ticker.settings.source.showingField;

                var seperator = '';
                    if (typeof ticker.settings.source.seperator != 'undefined' && typeof ticker.settings.source.seperator !== undefined)
                        seperator = ticker.settings.source.seperator;

                for (var i = 0; i < data.length; i++){
                    if (i >= ticker.settings.source.limit)
                        break;

                    if (ticker.settings.source.linkEnabled)
                        items += ( '<li><a target="'+ticker.settings.source.target+'" href="'+data[i].link+'">'+seperator+data[i][showingField]+'</a></li>' );
                    else
                        items += ( '<li><a>'+seperator+data[i][showingField]+'</a></li>' );
                    if (data[i][showingField] === 'undefined')
                        console.log('"'+showingField+'" does not exist in this json.')
                }

                ticker._ul.empty().append(items);
                ticker._li = ticker._ul.children("li");
                ticker._totalNews = ticker._ul.children("li").length;
                setContainerWidth();
                if (ticker.settings.effect != 'scroll')
                    showThis();

                ticker._li.find('.bn-seperator').css({
                    'height': ticker.settings.height-(ticker.settings.borderWidth*2)
                });
                
                playHandler();
            });
        }

        var startScrollAnimationLTR = function(){
            var _ulPosition = parseFloat(ticker._ul.css('marginLeft'));
            _ulPosition -= ticker.settings.scrollSpeed/2;
            ticker._ul.css({'marginLeft': _ulPosition });

            if (_ulPosition <= -ticker._ul.find('li:first-child').outerWidth())
            {
                ticker._ul.find('li:first-child').insertAfter(ticker._ul.find('li:last-child'));
                ticker._ul.css({'marginLeft': 0 });
            }
            if (ticker._pause === false){
                ticker._frameId = requestAnimationFrame(startScrollAnimationLTR);
                (window.requestAnimationFrame && ticker._frameId) || setTimeout(startScrollAnimationLTR, 16);
            }
        }

        var startScrollAnimationRTL = function(){
            var _ulPosition = parseFloat(ticker._ul.css('marginRight'));
            _ulPosition -= ticker.settings.scrollSpeed/2;
            ticker._ul.css({'marginRight': _ulPosition });

            if (_ulPosition <= -ticker._ul.find('li:first-child').outerWidth())
            {
                ticker._ul.find('li:first-child').insertAfter(ticker._ul.find('li:last-child'));
                ticker._ul.css({'marginRight': 0 });
            }
            if (ticker._pause === false)
                ticker._frameId = requestAnimationFrame(startScrollAnimationRTL);
                (window.requestAnimationFrame && ticker._frameId) || setTimeout(startScrollAnimationRTL, 16);
        }

        var scrollPlaying = function(){
            if (ticker.settings.direction === 'rtl')
            {
                if (ticker._ul.width() > ticker._news.width())
                    startScrollAnimationRTL();
                else
                	ticker._ul.css({'marginRight': 0 });
            }
            else
                if (ticker._ul.width() > ticker._news.width())
                    startScrollAnimationLTR();
                else
                	ticker._ul.css({'marginLeft': 0 });
        }
        
        var scrollGoNextLTR = function(){            
            ticker._ul.stop().animate({
                marginLeft : - ticker._ul.find('li:first-child').outerWidth()
            },300, function(){
                ticker._ul.find('li:first-child').insertAfter(ticker._ul.find('li:last-child'));
                ticker._ul.css({'marginLeft': 0 });
                ticker._controlsIsActive = true;
            });
        }

        var scrollGoNextRTL = function(){
            ticker._ul.stop().animate({
                marginRight : - ticker._ul.find('li:first-child').outerWidth()
            },300, function(){
                ticker._ul.find('li:first-child').insertAfter(ticker._ul.find('li:last-child'));
                ticker._ul.css({'marginRight': 0 });
                ticker._controlsIsActive = true;
            });
        }

        var scrollGoPrevLTR = function(){
            var _ulPosition = parseInt(ticker._ul.css('marginLeft'),10);
            if (_ulPosition >= 0)
            {
                ticker._ul.css({'margin-left' : -ticker._ul.find('li:last-child').outerWidth()});
                ticker._ul.find('li:last-child').insertBefore(ticker._ul.find('li:first-child'));                
            }

            ticker._ul.stop().animate({
                marginLeft : 0
            },300, function(){
                ticker._controlsIsActive = true;
            });
        }

        var scrollGoPrevRTL = function(){
            var _ulPosition = parseInt(ticker._ul.css('marginRight'),10);
            if (_ulPosition >= 0)
            {
                ticker._ul.css({'margin-right' : -ticker._ul.find('li:last-child').outerWidth()});
                ticker._ul.find('li:last-child').insertBefore(ticker._ul.find('li:first-child'));
            }

            ticker._ul.stop().animate({
                marginRight : 0
            },300, function(){
                ticker._controlsIsActive = true;
            });
        }

        var scrollNext = function(){
            if (ticker.settings.direction === 'rtl')
                scrollGoNextRTL();
            else
                scrollGoNextLTR();
        }

        var scrollPrev = function(){
            if (ticker.settings.direction === 'rtl')
                scrollGoPrevRTL();
            else
                scrollGoPrevLTR();
        }

        var effectTypography = function(){
            ticker._ul.find('li').hide();
            ticker._ul.find('li').eq(ticker._activeNews).width(30).show();
            ticker._ul.find('li').eq(ticker._activeNews).animate({
                width: '100%',
                opacity : 1
            },1500);
        }

        var effectFade = function(){
            ticker._ul.find('li').hide();
            ticker._ul.find('li').eq(ticker._activeNews).fadeIn();
        }

        var effectSlideDown = function(){
            if (ticker._totalNews <= 1)
            {
                 ticker._ul.find('li').animate({
                    'top':30,
                    'opacity':0
                },300, function(){
                    $(this).css({
                        'top': -30,
                        'opacity' : 0,
                        'display': 'block'
                    })
                    $(this).animate({
                        'top': 0,
                        'opacity' : 1
                    },300);
                });
            }   
            else
            {   
                ticker._ul.find('li:visible').animate({
                    'top':30,
                    'opacity':0
                },300, function(){
                    $(this).hide();
                });

                ticker._ul.find('li').eq(ticker._activeNews).css({
                    'top': -30,
                    'opacity' : 0
                }).show();

                ticker._ul.find('li').eq(ticker._activeNews).animate({
                    'top': 0,
                    'opacity' : 1
                },300);
            }
        }

        var effectSlideUp = function(){
            if (ticker._totalNews <= 1)
            {
                 ticker._ul.find('li').animate({
                    'top':-30,
                    'opacity':0
                },300, function(){
                    $(this).css({
                        'top': 30,
                        'opacity' : 0,
                        'display': 'block'
                    })
                    $(this).animate({
                        'top': 0,
                        'opacity' : 1
                    },300);
                });
            }   
            else
            {   
                ticker._ul.find('li:visible').animate({
                    'top':-30,
                    'opacity':0
                },300, function(){
                    $(this).hide();
                });

                ticker._ul.find('li').eq(ticker._activeNews).css({
                    'top': 30,
                    'opacity' : 0
                }).show();

                ticker._ul.find('li').eq(ticker._activeNews).animate({
                    'top': 0,
                    'opacity' : 1
                },300);
            }
        }

        var effectSlideLeft = function(){  
            if (ticker._totalNews <= 1)
            {
                 ticker._ul.find('li').animate({
                    'left':'50%',
                    'opacity':0
                },300, function(){
                    $(this).css({
                        'left': -50,
                        'opacity' : 0,
                        'display': 'block'
                    })
                    $(this).animate({
                        'left': 0,
                        'opacity' : 1
                    },300);
                });
            }   
            else
            {       
                ticker._ul.find('li:visible').animate({
                    'left':'50%',
                    'opacity':0
                },300, function(){
                    $(this).hide();
                });

                ticker._ul.find('li').eq(ticker._activeNews).css({
                    'left': -50,
                    'opacity' : 0
                }).show();

                ticker._ul.find('li').eq(ticker._activeNews).animate({
                    'left': 0,
                    'opacity' : 1
                },300);
            }
        }

        var effectSlideRight = function(){
            if (ticker._totalNews <= 1)
            {
                 ticker._ul.find('li').animate({
                    'left':'-50%',
                    'opacity':0
                },300, function(){
                    $(this).css({
                        'left': '50%',
                        'opacity' : 0,
                        'display': 'block'
                    })
                    $(this).animate({
                        'left': 0,
                        'opacity' : 1
                    },300);
                });
            }   
            else
            {   
                ticker._ul.find('li:visible').animate({
                    'left':'-50%',
                    'opacity':0
                },300, function(){
                    $(this).hide();
                });

                ticker._ul.find('li').eq(ticker._activeNews).css({
                    'left': '50%',
                    'opacity' : 0
                }).show();

                ticker._ul.find('li').eq(ticker._activeNews).animate({
                    'left': 0,
                    'opacity' : 1
                },300);
            }
        }


        var showThis = function(){            
            ticker._controlsIsActive = true;

            switch (ticker.settings.effect){
                case 'typography':
                    effectTypography();
                    break;
                case 'fade':
                    effectFade();
                    break;
                case 'slide-down':
                    effectSlideDown();
                    break;
                case 'slide-up':
                    effectSlideUp();
                    break;
                case 'slide-left':
                    effectSlideLeft();
                    break;
                case 'slide-right':
                    effectSlideRight();
                    break;
                default:
                    ticker._ul.find('li').hide();
                    ticker._ul.find('li').eq(ticker._activeNews).show();
            }
            
        }

        var nextHandler = function(){
            switch (ticker.settings.effect){
                case 'scroll':
                    scrollNext();
                    break;
                default:
                    ticker._activeNews++;
                    if (ticker._activeNews >= ticker._totalNews)
                        ticker._activeNews = 0;

                    showThis();
                    
            }
        }

        var prevHandler = function(){
            switch (ticker.settings.effect){
                case 'scroll':
                    scrollPrev();
                    break;
                default:
                    ticker._activeNews--;
                    if (ticker._activeNews < 0)
                        ticker._activeNews = ticker._totalNews-1;
                    
                    showThis();
            }
        }

        var playHandler = function(){
            ticker._pause = false;
            if (ticker.settings.play)
            {
                switch (ticker.settings.effect){
                    case 'scroll':
                        scrollPlaying();
                        break;
                    default:
                        ticker.pause();
                        ticker._interval = setInterval(function(){
                            ticker.next();
                        },ticker.settings.delayTimer);
                }
            }
        }

        var resizeEvent = function(){
            if (ticker._element.width() < 480){
                ticker._label.hide();
                if (ticker.settings.direction == 'rtl')
                    ticker._news.css({"right":0});
                else
                    ticker._news.css({"left":0});
            }
            else{
                ticker._label.show();
                if (ticker.settings.direction == 'rtl')
                    ticker._news.css({"right":ticker._label.outerWidth()});
                else
                    ticker._news.css({"left":ticker._label.outerWidth()});
            }
        }

        /****************************************************/
        /**PUBLIC METHODS************************************/
        /****************************************************/
        ticker.init = function() {
            ticker.settings = $.extend({}, defaults, options);

            //ticker._element.append('<div class="bn-breaking-loading"></div>');
            //window.onload = function(){

            	//ticker._element.find('.bn-breaking-loading').hide();

	            //set ticker positions
	            initializeSettings();

	            //adding effect type class
	            ticker._element.addClass('bn-effect-'+ticker.settings.effect+' bn-direction-'+ticker.settings.direction);
	            
	            setContainerWidth();

	            //if external data, load first
	            if (typeof ticker.settings.source === 'object'){
	                switch (ticker.settings.source.type){
	                    case 'rss':
	                        if (ticker.settings.source.usingApi === 'rss2json'){
	                            loadDataWithRSS2JSON();
	                            if (ticker.settings.source.refreshTime > 0){
	                                setInterval(function(){
	                                    ticker._activeNews = 0;
	                                    ticker.pause();
	                                    ticker._ul.empty().append('<li style="display:block; padding-left:10px;"><span class="bn-loader-text">......</span></li>');
	                                    setTimeout(function(){
	                                        loadDataWithRSS2JSON();
	                                    },1000);                                    
	                                },ticker.settings.source.refreshTime*1000*60);
	                            }
	                        }
	                        else
	                            loadDataWithYQL();
	                        break;
	                    case 'json':
	                        loadJSON();
	                        if (ticker.settings.source.refreshTime > 0){
	                                setInterval(function(){
	                                    ticker._activeNews = 0;
	                                    ticker.pause();
	                                    ticker._ul.empty().append('<li style="display:block; padding-left:10px;"><span class="bn-loader-text">......</span></li>');
	                                    setTimeout(function(){
	                                        loadJSON();
	                                    },1000);                                    
	                                },ticker.settings.source.refreshTime*1000*60);
	                            }
	                        break;
	                    default:
	                        console.log('Please check your "source" object parameter. Incorrect Value');
	                }
	            }
	            else if (ticker.settings.source === 'html'){
	                if (ticker.settings.effect != 'scroll')
	                    showThis();

	                playHandler();
	            }
	            else{
	                 console.log('Please check your "source" parameter. Incorrect Value');
	            }

	            //set playing status class
	            if (!ticker.settings.play)
	                ticker._action.find('span').removeClass('bn-pause').addClass('bn-play');
	            else
	                ticker._action.find('span').removeClass('bn-play').addClass('bn-pause');


	            ticker._element.on('mouseleave', function(e){                
	                var activePosition = $(document.elementFromPoint(e.clientX, e.clientY)).parents('.bn-breaking-news')[0];
	                if ($(this)[0] === activePosition) {
	                    return;
	                }
	                

	                if (ticker.settings.stopOnHover === true)
	                {
	                    if (ticker.settings.play === true)
	                        ticker.play();
	                }
	                else
	                {
	                    if (ticker.settings.play === true && ticker._pause === true)
	                        ticker.play();
	                }                

	            });

	            ticker._element.on('mouseenter', function(){
	                if (ticker.settings.stopOnHover === true)
	                    ticker.pause();
	            });

	            ticker._next.on('click', function(){
	                if (ticker._controlsIsActive){
	                    ticker._controlsIsActive = false;
	                    ticker.pause();
	                    ticker.next();
	                }                
	            });

	            ticker._prev.on('click', function(){
	                if (ticker._controlsIsActive){
	                    ticker._controlsIsActive = false;
	                    ticker.pause();
	                    ticker.prev();
	                } 
	            });

	            ticker._action.on('click', function(){
	                if (ticker._controlsIsActive){
	                    if (ticker._action.find('span').hasClass('bn-pause'))
	                    {
	                        ticker._action.find('span').removeClass('bn-pause').addClass('bn-play');
	                        ticker.stop();
	                    }
	                    else
	                    {
	                        ticker.settings.play = true;
	                        ticker._action.find('span').removeClass('bn-play').addClass('bn-pause');
	                        //ticker._pause = false;
	                    }
	                } 
	            });

	            resizeEvent();
	        //}

            $(window).on('resize', function(){
                resizeEvent();
                ticker.pause();
                ticker.play();
            });

        }

        ticker.pause = function() {
            ticker._pause = true;
            clearInterval(ticker._interval);
            cancelAnimationFrame(ticker._frameId);
        }

        ticker.stop = function() {
            ticker._pause = true;
            ticker.settings.play = false;
        }

        ticker.play = function() {
            playHandler();
        }

        ticker.next = function() {
            nextHandler();
        }

        ticker.prev = function() {
            prevHandler();
        }
        /****************************************************/
        /****************************************************/
        /****************************************************/
        ticker.init();

    }

    $.fn.breakingNews = function(options) {

        return this.each(function() {
            if (undefined == $(this).data('breakingNews')) {
                var ticker = new $.breakingNews(this, options);
                $(this).data('breakingNews', ticker);
            }
        });

    }

})(jQuery);
