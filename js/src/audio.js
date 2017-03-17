var widgets = require('jupyter-js-widgets');
var _ = require('underscore');


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var AudioModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
        _model_name : 'AudioModel',
        _view_name : 'AudioView',
        _model_module : 'jupyter-widget-audio',
        _view_module : 'jupyter-widget-audio',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        src:'',
    })
});


// Custom View. Renders the widget model.
var AudioView = widgets.DOMWidgetView.extend({
    render: function() {

        console.log('render');
        this.el.setAttribute('controls', 'controls');
        this.el.setAttribute('src', this.model.get('src'));//'http://www.kozco.com/tech/piano2.wav');

        var that=this;
        this.el.ontimeupdate =  function currentTimeChanged() {
            that.model.set('current_time', that.el.currentTime, {updated_view: that});
            that.touch();
        };
    },


    get tagName() {
        // We can't make this an attribute with a default value
        // since it would be set after it is needed in the
        // constructor.
        return 'audio';
    }

});


module.exports = {
    AudioModel : AudioModel,
    AudioView : AudioView
};
