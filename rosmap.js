const icons = {
  school: "fa-school",
  company: "fa-building",
  "research institute": "fa-flask",
  "user group": "fa-users",
  individual: "fa-user-circle",
};
const colors = {
  school: "#62af44",
  company: "#4186f0",
  "research institute": "#db4436",
  "user group": "#232e4a",
  individual: "#ffdd5e",
};

function createInfoWindow(location) {
  const div = document.createElement("div");
  const head = document.createElement("h3");
  head.textContent = location.name;
  head.classList.add("infohead");
  div.appendChild(head);

  const head2 = document.createElement("h5");
  head2.textContent = location.type;
  head2.classList.add("infosubhead");
  div.appendChild(head2);

  if (location.address) {
    const add = document.createElement("div");
    add.classList.add("infoadd");
    add.textContent = location.address;
    div.appendChild(add);
  }

  if (location.description) {
    const desc = document.createElement("div");
    desc.classList.add("infodesc");
    desc.textContent = location.description;
    div.appendChild(desc);
  }

  if (location.link) {
    div.appendChild(document.createElement("br"));
    const link = document.createElement("a");
    link.href = location.link;

    const linkicon = document.createElement("i");
    linkicon.classList.add("fas");
    linkicon.classList.add("fa-external-link-alt");
    link.appendChild(linkicon);

    div.appendChild(link);
  }
  return div;
}

async function initialize() {
  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

  var map = new Map(document.getElementById("map-canvas"), { mapId: "rosmap", zoom: 2, center: { lat: 0, lng: 20 } });
  const infoWindow = new google.maps.InfoWindow({
    content: "",
    disableAutoPan: true,
  });
  var regions = ["america", "asia", "australia", "europe", "africa"];
  var regions_loaded = 0;
  const markers = [];
  for (var region of regions) {
    $.get("https://raw.githubusercontent.com/DLu/ros_map/main/data/" + region + ".yaml").done(function (data) {
      var locations = jsyaml.load(data);
      for (var location of locations) {
        const pin = { title: location.name, glyphColor: "white", scale: 1.5 };
        const icon = document.createElement("div");
        icon.classList.add("fas");
        icon.classList.add(icons[location.type] || "fa-globe");
        pin.background = colors[location.type] || "purple";
        pin["glyph"] = icon;

        const pinGlyph = new google.maps.marker.PinElement(pin);

        const marker = new google.maps.marker.AdvancedMarkerElement({
          map,
          position: { lat: location.lat, lng: location.long },
          content: pinGlyph.element,
        });
        marker.ros_data = location;
        marker.addListener("click", () => {
          infoWindow.setContent(createInfoWindow(marker.ros_data));
          infoWindow.open(map, marker);
        });
        markers.push(marker);
      }
      regions_loaded++;
      if (regions_loaded == regions.length) {
        const markerCluster = new markerClusterer.MarkerClusterer({ markers, map });
      }
    });
  }
}

initialize();
