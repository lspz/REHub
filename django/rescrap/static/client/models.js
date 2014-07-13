var Listing = Backbone.Model.extend({
  defaults: function(){
    return {
      id: null,
      address: '',
      url: '',
      img_path: '',
      price_raw: '',
      title_desc: '',
      short_desc: '',
      source: '',
      bedrooms: null,
      bathrooms: null,
      carparks: null
    }
  }
});

var Listings = Backbone.Collection.extend({
  model: Listing,

  initialize: function() {
    _.bindAll(this, 'url');

    this.suburbId = -1;
    this.pageNo = 0;
  },

  url: function() {
    return '/api/listings/' + this.suburbId + '/' + this.pageNo + '/' ;
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

