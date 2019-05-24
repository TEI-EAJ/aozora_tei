/* 
 * Mirador Drag and Drop Link Plugin
 * https://github.com/2sc1815j/mirador-dragndrop-link-plugin
 * 
 * Released under the MIT License
 * Copyright (c) 2018 2SC1815J
 * 
 * A Mirador plugin that adds the IIIF drag and drop link to every window.
 * The most of this source code is owed to "ManifestButton."
 */
/* 
 * Mirador plugins - ManifestButton
 * https://github.com/dbmdz/mirador-plugins/tree/master/ManifestButton
 * 
 * The MIT License (MIT)
 * Copyright (c) 2016 Digital Library/Munich Digitization Center at Bavarian State Library
 */
var DragndropLinkButton = {
    /* all of the needed locales */
    locales: {
        'en': {
            'button-tooltip': 'Drag and drop to another IIIF viewer'
        }
    },

    /* the template for the link button */
    buttonTemplate: Mirador.Handlebars.compile([
        '<a target="_blank" class="mirador-btn mirador-icon-drag-and-drop-link" role="button" title="{{t "button-tooltip"}}" aria-label="{{t "button-tooltip"}}">',
        '<i class="fa {{iconClass}} fa-lg fa-fw"></i>',
        '</a>',
    ].join('')),

    /* initializes the plugin */
    init: function(){
        i18next.on('initialized', function(){
            this.addLocalesToViewer();
        }.bind(this));
        this.injectWorkspaceEventHandler();
    },

    /* injects the button to the window menu */
    injectButtonToMenu: function(windowButtons, iconClass){
        $(windowButtons).prepend(this.buttonTemplate({
            'iconClass': iconClass || 'icon-IIIF-logo'
        }));
    },

    /* injects the needed workspace event handler */
    injectWorkspaceEventHandler: function(){
        var this_ = this;
        var origFunc = Mirador.Workspace.prototype.bindEvents;
        Mirador.Workspace.prototype.bindEvents = function(){
            origFunc.apply(this);
            this.eventEmitter.subscribe('WINDOW_ELEMENT_UPDATED', function(event, data){
                var windowButtons = data.element.find('.window-manifest-navigation');
                var options = this.state.getStateProperty('dragndropLinkButton');
                var iconClass = $.isPlainObject(options) ? options.iconClass : undefined;
                this_.injectButtonToMenu(windowButtons, iconClass);
            }.bind(this));
            this.eventEmitter.subscribe('windowUpdated', function(event, data){
                if(!data.loadedManifest){
                    return;
                }
                var slotElement = this.getSlotFromAddress(data.slotAddress).appendTo;
                /* IIIF Drag-and-drop */
                /* http://zimeon.github.io/iiif-dragndrop/ */
                var manifestUri = data.loadedManifest;
                var canvasUri = data.canvasID;
                var defaultTarget = manifestUri;
                var link = defaultTarget + '?manifest=' + manifestUri + '&canvas=' + canvasUri;
                $('.mirador-btn.mirador-icon-drag-and-drop-link', slotElement).attr('href', link);
            }.bind(this));
        };
    },

    /* adds the locales to the internationalization module of the viewer */
    addLocalesToViewer: function(){
        for(var language in this.locales){
            i18next.addResources(
                language, 'translation',
                this.locales[language]
            );
        }
    }
};

$(document).ready(function(){
    DragndropLinkButton.init();
});
