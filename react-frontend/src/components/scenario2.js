import React, { Component, useState, useCallback, useEffect } from "react";
import { Card, Row, Col } from "antd";
import ReactMapGL, { Source, Layer } from "react-map-gl";
// import * as geojson from './SA3-language.json'
import "./style.less";

const backend_ip = process.env.BACKEND_IP || 'http://172.26.134.60:80';


function Map(pro) {

  const [allData, setAllData] = useState(null);
  useEffect(() => {
    /* global fetch */
    fetch(
      backend_ip+'/language_data'
    )
      .then(resp => resp.json())
      .then(json => setAllData(json.data));
  }, []);

  // console.log(allData)


  const langugae = pro.language
  const layerStyle = {
    id: "data",
    type: "fill",
    paint: {
      "fill-color": {
        property: langugae + "_persons_percentage",
        stops: [
          [0.001, "#bdc3c7"],
          [0.003, "#34495e"],
          [0.005, "#95a5a6"],
          [0.008, "#7f8c8d"],
          [0.01, "#3498db"],
          [0.015, "#2980b9"],
          [0.02, "#2ecc71"],
          [0.025, "#27ae60"],
          [0.03, "#f1c40f"],
          [0.035, "#f39c12"],
          [0.04, "#e67e22"],
          [0.045, "#d35400"],
          [0.05, "#e74c3c"],
          [0.055, "#c0392b"],
        ],
      },
      "fill-opacity": 0.7,
    },
  };

  const [viewport, setViewport] = React.useState({
    longitude: 144.963058,
    latitude: -37.813629,
    zoom: 7,
  });
  const [hoverInfo, setHoverInfo] = useState(null);

  const onHover = useCallback((event) => {
    const {
      features,
      srcEvent: { offsetX, offsetY },
    } = event;
    const hoveredFeature = features && features[0];
    setHoverInfo(
      hoveredFeature
        ? {
            feature: hoveredFeature,
            x: offsetX,
            y: offsetY,
          }
        : null
    );
  }, []);

  return (

    <ReactMapGL
      {...viewport}
      width="49vw"
      height="50vh"
      onViewportChange={setViewport}
      mapboxApiAccessToken="pk.eyJ1IjoiemhlbmcwNTE4IiwiYSI6ImNrb2pxYXZnczAweHIycG5wNjgyZjI4b3UifQ.BP0kV8Ah-cy3FlKcr1z6SQ"
      onHover={onHover}
      interactiveLayerIds={["data"]}
    >
      <Source id="my-data" type="geojson" data={allData}>
        <Layer {...layerStyle} />
      </Source>
      {hoverInfo && (
        <div
          className="tooltip"
          style={{ left: hoverInfo.x, top: hoverInfo.y }}
        >
          <div>Area: {hoverInfo.feature.properties.name}</div>
          <div>Persons: {hoverInfo.feature.properties[pro.language + "_persons"]}</div>
          <div>Tweets: {hoverInfo.feature.properties[pro.language + "_tweets"]}</div>
          <div>Person percentage: {hoverInfo.feature.properties[pro.language + "_persons_percentage"]}</div>
          <div>Tweets percentage: {hoverInfo.feature.properties[pro.language+"_tweets_percentage"]}</div>
        </div>
      )}
    </ReactMapGL>
  );
}

const MapHook = Map;

export default class Scenario2 extends Component {
  render() {
    return (
      <div>
        <h1 style={{fontSize:'30px'} }>Language Usage in Melbourne Regions</h1>
        <Row gutter={[8, 8]}>
          <Col span={12}>
          <Card title="Speaking English Only">
            <MapHook language="English" />
            </Card>
          </Col>
          <Col span={12}>
          <Card title="Korean">
            <MapHook language="Korean" />
            </Card>
            </Col>
        </Row>
        <Row gutter={[8, 8]}>
        <Col span={12}>
          <Card title="Spanish">
            <MapHook language="Spanish" />
            </Card>
          </Col>
          <Col span={12}>
          <Card title="Japanese">
            <MapHook language="Japanese" />
            </Card>
            </Col>
        </Row>
      </div>
    );
  }
}
