
/*
Integration for Google Maps in the django admin.

How it works:

You have an address field on the page.
Enter an address and an on change event will update the map
with the address. A marker will be placed at the address.
If the user needs to move the marker, they can and the geolocation
field will be updated.

Only one marker will remain present on the map at a time.

This script expects:

<input type="text" name="address" id="id_address" />
<input type="text" name="geolocation" id="id_geolocation" />

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>

*/
var map;

function googleMapAdmin() {

    var autocomplete;
    var geocoder = new google.maps.Geocoder();
    var marker;

    var geolocationId = 'id_geolocation';
    var addressId = 'id_address';

    var tmp = JSON.parse(document.getElementById('buildings-data').textContent);
    var dataBuildings = JSON.parse(tmp);

    var self = {
        initialize: function() {

            // Generate map
            var myOptions = {
              zoom: 10,
              mapTypeId: self.getMapType()
            };
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

            var urlParms = self.parseURLParams(window.location.search);
            self.centerWithAddress(urlParms["address"][0],marker=1);

            /*
            map.data.loadGeoJson('../static/santiago.geojson')
            map.data.setStyle({
              fillColor: 'green',
              strokeWeight: 1
            });
            */

            var lat = dataBuildings[0]["fields"]["lat"];
            var lon = dataBuildings[0]["fields"]["lon"];

            var marker = new google.maps.Marker({
              position: new google.maps.LatLng(lat,lon),
              title: "test",
              map: map
            });

            marker.addListener('click', function() {
              '<str:region>/<str:commune>/<str:street>/edificio/<int:id>/'
              region = dataBuildings[0]["fields"]["addressRegion"].toLowerCase();
              commune = dataBuildings[0]["fields"]["addressCommune"].toLowerCase();
              street = dataBuildings[0]["fields"]["addressStreet"];
              street = street.replace(/\s+/g, '-').toLowerCase();
              street = self.removeAccents(street);
              number = dataBuildings[0]["fields"]["addressNumber"];
              id = dataBuildings[0]["pk"];
              url = '/property/'+region+'/'+commune+'/'+street+'/'+number+'/edificio/'+id
              console.info(url);
              window.location.href = url
            });
        },


        removeAccents : function(s)
        {
          s = s.replace(/á/g, "i");
          s = s.replace(/é/g, "e");
          s = s.replace(/í/g, "i");
          s = s.replace(/ó/g, "o");
          s = s.replace(/ú/g, "u");
          s = s.replace(/ü/g, "ü");
          return s;
        },

        centerWithAddress : function(address) {
          geocoder.geocode({'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var latlng = results[0].geometry.location;
                var marker = new google.maps.Marker({
                  position: latlng,
                  title: "Center",
                  map: map
                })
                self.centerWithCoordinates(latlng)
            } else {
                alert("Geocode was not successful for the following reason: " + status);
            }
          });
        },


        centerWithCoordinates: function(latlng) {
            map.setCenter(latlng);
            map.setZoom(16);
            //self.setMarker(latlng);
            //self.updateGeolocation(latlng);
        },

        getMapType : function() {
            // https://developers.google.com/maps/documentation/javascript/maptypes
            var geolocation = document.getElementById(addressId);
            var allowedType = ['roadmap', 'satellite', 'hybrid', 'terrain'];
            var mapType = geolocation.getAttribute('data-map-type');
            var mapType = 'roadmap';

            if (mapType && -1 !== allowedType.indexOf(mapType)) {
                return mapType;
            }

            return google.maps.MapTypeId.HYBRID;
        },

        getExistingLocation: function() {
            var geolocation = ''
            if (geolocation) {
                return geolocation.split(',');
            }
        },

        setMarker: function(latlng) {
            if (marker) {
                self.updateMarker(latlng);
            } else {
                self.addMarker({'latlng': latlng, 'draggable': true});
            }
        },

        addMarker: function(Options) {
            marker = new google.maps.Marker({
                map: map,
                position: Options.latlng
            });

            var draggable = Options.draggable || false;
            if (draggable) {
                self.addMarkerDrag(marker);
            }
        },

        addMarkerDrag: function() {
            marker.setDraggable(true);
            google.maps.event.addListener(marker, 'dragend', function(new_location) {
                self.updateGeolocation(new_location.latLng);
            });
        },

        updateMarker: function(latlng) {
            marker.setPosition(latlng);
        },

        updateGeolocation: function(latlng) {
            //document.getElementById(geolocationId).value = latlng.lat() + "," + latlng.lng();
            //$("#" + geolocationId).trigger('change');
        },

        parseURLParams : function(url) {
          var queryStart = url.indexOf("?") + 1,
          queryEnd   = url.indexOf("#") + 1 || url.length + 1,
          query = url.slice(queryStart, queryEnd - 1),
          pairs = query.replace(/\+/g, " ").split("&"),
          parms = {}, i, n, v, nv;

          if (query === url || query === "") return;

          for (i = 0; i < pairs.length; i++) {
            nv = pairs[i].split("=", 2);
            n = decodeURIComponent(nv[0]);
            v = decodeURIComponent(nv[1]);
            if (!parms.hasOwnProperty(n)) parms[n] = [];
            parms[n].push(nv.length === 2 ? v : null);
          }
          return parms;
        }
    };

    return self;
}

$(document).ready(function() {
    var googlemap = googleMapAdmin();
    googlemap.initialize();
});
