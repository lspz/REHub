var ListingView = Backbone.View.extend({
  tagName: 'div',
  className: 'panel panel-primary list-item',

  template: _.template($('#listingTemplate').html()),

  render: function() {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  }
});

var ListingsView = Backbone.View.extend({
  el: $('#listings'),

  initialize: function() {
    //_.bindAll(this, 'render');//, 'addListing', 'resetListings');

    this.model.on('add', this.addListing, this);
    this.model.on('reset', this.resetListings, this);

  },

  resetListings: function(){
    this.$el.empty();
  },

  addListing: function(listing){
    console.log('adding: ' + listing.get('address'));
    var view = new ListingView({model: listing});
    this.$el.append(view.render().el);   
  }
});

var AlertView = Backbone.View.extend({
  tagName: 'div',
  className: 'alert alert-info',

  render: function() {
    this.$el.html(this.model.get('msg'));
    return this;
  }
});

var AlertsView = Backbone.View.extend({
  el: $('#alerts'),

  initialize: function() {
    this.model.on('add', this.addAlert, this);
    this.model.on('reset', this.resetAlerts, this);
  },

  resetAlerts: function(){
    this.$el.empty();
  },

  addAlert: function(model){
    var view = new AlertView({model: model});
    this.$el.append(view.render().el);   
  }
});

var AppView = Backbone.View.extend({
  el: 'body',

  events : {
    "click button#btnRefresh" : "refreshClicked"
  },

  initialize: function(){
    _.bindAll(this, 'populateSuburbs', 'refreshClicked', 'getSelectedSuburbIds');

    this.suburbs = new Suburbs();
    this.listings = new Listings();
    this.alerts = new Alerts();

    this.listingsView = new ListingsView({model: this.listings}); 
    this.alertsView = new AlertsView({model: this.alerts});
  },

  populateSuburbs: function(){
    var suburbArray = [];

    this.suburbs.each(function(suburb) {
      suburbArray.push(suburb.get('name'));
    });

    $('#suburbTags').tokenfield({
      typeahead: {
        name: 'tags',
        local: suburbArray
      }
    }); 
  },

  render: function(){
    this.suburbs.fetch({reset:true, success: this.populateSuburbs})

    // No need to show anything initialy
    // this.listingsView.render();
    // this.errorsView.render();
    return this;  
  },

  refreshClicked : function(event){
    // TODO: support multiple ID's
    this.alerts.reset();
    var noListingFoundMsg = 'Your search returned no result';

    // var suburbsSel = $('#suburbTags').tokenfield('getTokensList');

    // var suburbsList = this.suburbs.where({name: suburbsSel});

    var suburbIds = this.getSelectedSuburbIds();
    if (suburbIds == ''){
      this.alerts.add({msg: noListingFoundMsg});
      return;
    }

    var context = this;
    this.listings.suburbId = suburbIds;
    this.listings.reset();
    this.listings.fetch({
      add: true,
      success: function() {
        if (context.listings.length == 0){
          this.alerts.add({msg: noListingFoundMsg});
        }
      }
    });
  },

  getSelectedSuburbIds: function(){
    var suburbsSel = $('#suburbTags').tokenfield('getTokensList');
    var suburbsArray = suburbsSel.split(',');
    var result = ''
    var suburbs = this.suburbs;
    $.each(suburbsArray, function(index, value){
      suburb = suburbs.findWhere({name: value});  
      if (suburb) {
        if (result != ''){
          result = result + '-';
        } 
        result = result + suburb.id;
      }
    });
    console.log(result);
    return result;
  }

});

    // // Setup dummy data
    // var listing1 = new Listing();    
    // listing1.set('suburbId', 0);
    // listing1.set('address', '1 dummy st');
    // listing1.set('title', 'This is awesome - $400000');
    // listing1.set('desc', 'house blah');
    // this.listings.add(listing1);

    // var listing2 = new Listing();    
    // listing2.set('suburbId', 1);
    // listing2.set('address', '2 dummy st');
    // listing2.set('title', 'This is awesome - $400000');
    // listing2.set('desc', 'house blah');
    // this.listings.add(listing2);

    // var listing3 = new Listing();    
    // listing3.set('suburbId', 1);
    // listing3.set('address', '3 dummy st');
    // listing3.set('title', 'This is awesome - $400000');
    // listing3.set('desc', 'house blah');
    // this.listings.add(listing3);

    // var listing4 = new Listing();    
    // listing4.set('suburbId', 2);
    // listing4.set('address', '4 dummy st');
    // listing4.set('title', 'This is awesome - $400000');
    // listing4.set('desc', 'house blah');
    // this.listings.add(listing4);