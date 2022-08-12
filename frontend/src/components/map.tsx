import MapView from "@arcgis/core/views/MapView";
import WebMap from "@arcgis/core/WebMap";
import Map from "@arcgis/core/Map";
import GraphicsLayer from "@arcgis/core/layers/GraphicsLayer";
import Graphic from "@arcgis/core/Graphic";
import config from "@arcgis/core/config";
import { useEffect, useRef } from "react";
import "./map.css";
import PopupTemplate from "@arcgis/core/PopupTemplate";

export default function MapDisplay({
  x,
  y,
  details,
}: {
  x: number;
  y: number;
  details: any;
}) {
  const mapDiv = useRef(null);

  useEffect(() => {
    if (mapDiv.current && x && y) {
      config.apiKey =
        "AAPKaee665f65cd24efc9f4e2036818356c0Vim76E6gUKO-BqPBIVJNsskiAqcKj4lcBf3avKDgPLwaQ174UXdiMvpY5FG6kiBv";
      console.log(x, y);
      const map = new Map({
        basemap: "arcgis-imagery", // Basemap layer service
      });
      //   const webmap = new WebMap({
      //     portalItem: {
      //       id: "aa1d3f80270146208328cf66d022e09c",
      //     },
      //   });
      const view = new MapView({
        map: map,
        center: [x, y], // Longitude, latitude
        zoom: 13, // Zoom level
        container: mapDiv.current, // Div element
      });

      const graphicLayer = new GraphicsLayer();
      map.add(graphicLayer);

      const point = {
        type: "point",
        longitude: x,
        latitude: y,
      };

      const simpleMarkerSymbol = {
        type: "simple-marker",
        color: [9, 105, 218], // Orange
        outline: {
          color: [255, 255, 255], // White
          width: 1,
        },
      };

      const pointGraphic = new Graphic({
        // @ts-ignore
        geometry: point,
        symbol: simpleMarkerSymbol,
      });
      graphicLayer.add(pointGraphic);

      pointGraphic.attributes = details;

      console.log(
        Object.keys(details).map((key) => {
          return {
            fieldName: key,
            label: key,
            isEditable: false,
            tooltip: "",
            visible: true,
            format: null,
            stringFieldOption: "text-box",
          };
        })
      );

      pointGraphic.popupTemplate = new PopupTemplate({
		title: "Details",
        content: [
          {
            type: "fields",
            fieldInfos: Object.keys(details).map((key) => {
              return {
                fieldName: key,
                label: key,
                isEditable: false,
                tooltip: "",
                visible: true,
                format: null,
                stringFieldOption: "text-box",
              };
            }),
          },
        ],
      });
    }
  }, []);

  return <div id="mapDiv" ref={mapDiv}></div>;
}
