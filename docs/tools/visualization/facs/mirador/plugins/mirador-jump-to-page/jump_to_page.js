(function() {
  var originalWindowInit = Mirador.Window.prototype.init;

  var template = Mirador.Handlebars.compile([
    '&nbsp;<select class="{{selectClassName}}">',
    '{{#canvases}}',
    '<option value="{{id}}">{{label}}</option>',
    '{{/canvases}}',
    '</select>&nbsp;'
  ].join(''));

  Mirador.Window.prototype.init = function(){
    var windowObj = this;

    originalWindowInit.apply(windowObj);

    var canvases = windowObj.imagesList.map(function(canvas){
      canvas.id = canvas['@id'];
      return canvas;
    });

    windowObj.element.find('.window-manifest-navigation').prepend(template({
      'selectClassName': 'page-select',
      'canvases': canvases
    }));

    windowObj.element.find('.page-select').on('change', function(event) {
      var canvasID = jQuery(this).val();
      windowObj.eventEmitter.publish('SET_CURRENT_CANVAS_ID.' + windowObj.id, canvasID);
    });
  };
})();
