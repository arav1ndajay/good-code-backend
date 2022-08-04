import MapView from "@arcgis/core/views/MapView";
import WebMap from "@arcgis/core/WebMap";
import { useEffect, useRef } from "react";
import "./map.css"

export default function MapDisplay() {

	const mapDiv = useRef(null);

	useEffect(() => {
	  if (mapDiv.current) {
		  console.log("hi")
	  //   const map = new Map({
	  //     basemap: "arcgis-topographic", // Basemap layer service
	  //   });
		const webmap = new WebMap({
		  portalItem: {
			id: "aa1d3f80270146208328cf66d022e09c"
		  }
		});
		const view = new MapView({
		  map: webmap,
		  center: [-118.805, 34.027], // Longitude, latitude
		  zoom: 13, // Zoom level
		  container: mapDiv.current, // Div element
		});
	  }
	}, []);
  
	return <div className="mapDiv" ref={mapDiv}></div>;
}