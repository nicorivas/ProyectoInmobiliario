
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

function googleMapAutocomplete() {

    var autocomplete;
    var geocoder = new google.maps.Geocoder();
    var addressId = 'id_address';

    var self = {
        initialize: function() {
            var lat = 0;
            var lng = 0;
            var zoom = 2;

            // Autocomplete
            autocomplete = new google.maps.places.Autocomplete(
                /** @type {!HTMLInputElement} */(document.getElementById(addressId)),
                {types: ['geocode']});

            // this only triggers on enter, or if a suggested location is chosen
            // todo: if a user doesn't choose a suggestion and presses tab, the map doesn't update
            // autocomplete.addListener("place_changed", self.codeAddress);
        }
    };

    return self;
}

$(document).ready(function() {
    var googlemap = googleMapAutocomplete();
    googlemap.initialize();
});
