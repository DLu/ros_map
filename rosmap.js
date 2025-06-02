const icons = {
  school: "fa-school",
  company: "fa-building",
  "research institute": "fa-flask",
  "user group": "fa-users",
  individual: "fa-user-circle",
  other: "fa-globe",
};
const colors = {
  school: "#62af44",
  company: "#4186f0",
  "research institute": "#db4436",
  "user group": "#232e4a",
  individual: "#ffdd5e",
  other: "purple",
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

function createIcon(the_type) {
  var icon_key;
  if (icons[the_type]) {
    icon_key = the_type;
  } else {
    icon_key = "other";
  }

  var icon = document.createElement("i");
  icon.classList.add("fas");
  icon.classList.add(icons[icon_key]);
  icon.style.backgroundColor = colors[icon_key];
  return icon;
}

function initialize() {
  var map = L.map("map-canvas").setView([0, 20], 2);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  var regions = ["america", "asia", "australia", "europe", "africa"];
  var markers = L.markerClusterGroup({ maxClusterRadius: 30 });
  for (var region of regions) {
    $.get("https://raw.githubusercontent.com/DLu/ros_map/main/data/" + region + ".yaml").done(function (data) {
      var locations = jsyaml.load(data);
      for (var location of locations) {
        var icon_html = createIcon(location.type);
        icon_html.classList.add("rosmap_icon");

        var icon = L.divIcon({ html: icon_html });
        var marker = L.marker([location.lat, location.long], { icon: icon, title: location.name, alt: location.type });
        marker.bindPopup(createInfoWindow(location)).openPopup();
        markers.addLayer(marker);
      }

      map.addLayer(markers);
    });
  }

  var legend = document.getElementById("legend");
  for (const key in icons) {
    var item = document.createElement("li");
    legend.appendChild(item);
    var icon = createIcon(key);
    item.appendChild(icon);
    var text = document.createTextNode(" - " + key);
    item.appendChild(text);
  }
}
