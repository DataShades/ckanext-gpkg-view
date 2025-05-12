// ckan.module('gpkg-view', function ($, _) {
//     "use strict";
//     return {
//         options: {
//             table: '<div class="table-container"><table class="table table-striped table-bordered table-condensed"><tbody>{body}</tbody></table></div>',
//             row: '<tr><th>{key}</th><td>{value}</td></tr>',
//             style: {
//                 opacity: 0.7,
//                 fillOpacity: 0.1,
//                 weight: 2
//             },
//             i18n: {
//                 'error': _('An error occurred: %(text)s %(error)s'),
//                 'file_too_big': _('This file is too big to be previewed. Please download it locally.')
//             },
//             maxFileSize: null
//         },
//         initialize: function () {
//             this.el.empty();
//             if (this._isFileTooLarge()) {
//                 return this._showFileTooLargeError();
//             }
//             this._initializeMap();
//             this._loadGeoJsonData();
//         },
//         _isFileTooLarge: function () {
//             return this.options.maxFileSize !== null &&
//                 preload_resource.size &&
//                 preload_resource.size > this.options.maxFileSize;
//         },
//         _showFileTooLargeError: function () {
//             var msg = this.i18n('file_too_big');
//             this.el.append($("<div class='data-viewer-error'><p class='text-danger'>" + msg + "</p></div>"));
//         },
//         _initializeMap: function () {
//             var mapContainer = $("<div></div>")
//                 .attr("id", "map")
//                 .css({
//                     height: '500px',
//                     width: '100%'
//                 });

//             this.el.append(mapContainer);

//             // Wait for container to be added to DOM before initializing the map
//             setTimeout(() => {
//                 this.map = L.map('map', {
//                     attributionControl: false,
//                     // Add fadeAnimation false to prevent tile loading issues
//                     fadeAnimation: false
//                 });

//                 // Use the specified tile provider from configuration
//                 this.tileLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
//                     maxZoom: 20,
//                     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
//                     subdomains: 'abcd'
//                 }).addTo(this.map);

//                 // Force a map invalidation and redraw
//                 setTimeout(() => {
//                     this.map.invalidateSize();
//                 }, 100);

//                 // Set default view until data is loaded
//                 this.map.setView([0, 0], 2);

//                 L.Icon.Default.imagePath = this.options.site_url + 'images/';
//             }, 50);
//         },
//         _loadGeoJsonData: function () {
//             var self = this;
//             $.getJSON(preload_resource['url'])
//                 .done(function (data) {
//                     self.showPreview(data);
//                 })
//                 .fail(function (jqXHR, textStatus, errorThrown) {
//                     self.showError(jqXHR, textStatus, errorThrown);
//                 });
//         },
//         showError: function (jqXHR, textStatus, errorThrown) {
//             if (textStatus == 'error' && jqXHR.responseText.length) {
//                 this.el.html(jqXHR.responseText);
//             } else {
//                 this.el.html(this.i18n('error', { text: textStatus, error: errorThrown }));
//             }
//         },
//         showPreview: function (geojsonFeature) {
//             var self = this;

//             // Ensure map is fully initialized before adding data
//             if (!this.map) {
//                 setTimeout(() => {
//                     this.showPreview(geojsonFeature);
//                 }, 200);
//                 return;
//             }

//             // Clear any existing layers
//             this.map.eachLayer(function (layer) {
//                 if (layer instanceof L.GeoJSON) {
//                     self.map.removeLayer(layer);
//                 }
//             });

//             var gjLayer = L.geoJSON(geojsonFeature, {
//                 style: self.options.style,
//                 onEachFeature: this._createFeaturePopup.bind(this)
//             }).addTo(self.map);

//             // Only fit bounds if we have valid bounds
//             if (gjLayer.getBounds && gjLayer.getBounds().isValid()) {
//                 self.map.fitBounds(gjLayer.getBounds());

//                 // Force a redraw after bounds are set
//                 setTimeout(() => {
//                     self.map.invalidateSize();
//                 }, 100);
//             }
//         },
//         _createFeaturePopup: function (feature, layer) {
//             if (!feature.properties) return;
//             var body = '';
//             $.each(feature.properties, function (key, value) {
//                 if (value != null && typeof value === 'object') {
//                     value = JSON.stringify(value);
//                 }
//                 body += L.Util.template(this.options.row, { key: key, value: value });
//             }.bind(this));
//             var popupContent = L.Util.template(this.options.table, { body: body });
//             layer.bindPopup(popupContent);
//         }
//     };
// });

// geojson preview module
ckan.module('gpkg-view', function (jQuery, _) {
    return {
      options: {
        table: '<div class="table-container"><table class="table table-striped table-bordered table-condensed"><tbody>{body}</tbody></table></div>',
        row:'<tr><th>{key}</th><td>{value}</td></tr>',
        style: {
          opacity: 0.7,
          fillOpacity: 0.1,
          weight: 2
        },
        i18n: {
          'error': _('An error occurred: %(text)s %(error)s'),
          'file_too_big': _('This GeoJSON file is too big to be previewed. Please download it locally.')
        },
        maxFileSize: null
      },
      initialize: function () {
        var self = this;

        self.el.empty();

        if (this.options.max_file_size !== 'None' && preload_resource.size &&
          preload_resource.size > this.options.max_file_size) {
          var msg = this.i18n('file_too_big');
          self.el.append($("<div class='data-viewer-error'><p class='text-danger'>" + msg + "</p></div>"));
          return
        }

        self.el.append($("<div></div>").attr("id","map"));
        self.map = ckan.commonLeafletMap('map', this.options.map_config, {attributionControl: false});

        // hack to make leaflet use a particular location to look for images
        L.Icon.Default.imagePath = this.options.site_url + 'js/vendor/leaflet/images/';

        jQuery.getJSON(preload_resource['url']).done(
          function(data){
            self.showPreview(data);
          })
        .fail(
          function(jqXHR, textStatus, errorThrown) {
            self.showError(jqXHR, textStatus, errorThrown);
          }
        );

        // The standard CRS for GeoJSON according to RFC 7946 is
        // urn:ogc:def:crs:OGC::CRS84, but proj4s uses a different name
        // for it. See https://github.com/ckan/ckanext-geoview/issues/51
        proj4.defs['OGC:CRS84'] = proj4.defs['EPSG:4326'];
      },

      showError: function (jqXHR, textStatus, errorThrown) {
        if (textStatus == 'error' && jqXHR.responseText.length) {
          this.el.html(jqXHR.responseText);
        } else {
          this.el.html(this.i18n('error', {text: textStatus, error: errorThrown}));
        }
      },

      showPreview: function (geojsonFeature) {
        var self = this;
        var gjLayer = L.Proj.geoJson(geojsonFeature, {
          style: self.options.style,
          onEachFeature: function(feature, layer) {
            var body = '';
            if (feature.properties) {
              jQuery.each(feature.properties, function(key, value){
                if (value != null && typeof value === 'object') {
                  value = JSON.stringify(value);
                }
                body += L.Util.template(self.options.row, {key: key, value: value});
              });
              var popupContent = L.Util.template(self.options.table, {body: body});
              layer.bindPopup(popupContent);
            }
          }
        }).addTo(self.map);
        self.map.fitBounds(gjLayer.getBounds());
      }
    };
  });
