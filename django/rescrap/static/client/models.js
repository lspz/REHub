var Listing = Backbone.Model.extend({
  defaults: function(){
    return {
      id: -1,
      address: '',
      url: '',
      img_path: '',
      price_raw: '',
      title_desc: '',
      short_desc: ''
    }
  }
});

var Listings = Backbone.Collection.extend({
  model: Listing,

  initialize: function() {
    _.bindAll(this, 'url');

    this.suburbId = -1;
  },

  url: function() {
    return '/api/listings/' + this.suburbId + '/';
  }
});

var Suburb = Backbone.Model.extend({
  defaults: function(){
    return {
      id: -1,
      name: ''
      // state: '',
      // postcode: ''
    }
  }
});

var Suburbs = Backbone.Collection.extend({
  model: Suburb,
  url: '/api/suburbs/'
});

var Alert = Backbone.Model.extend({
  defaults: function(){
    return {msg: ''}
  }
});

var Alerts = Backbone.Collection.extend({
  model: Alert
});

