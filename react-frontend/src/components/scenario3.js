import React, { Component, useState, useCallback, useEffect } from "react";
import { Card, Row, Col } from "antd";
import ReactMapGL, { Source, Layer } from "react-map-gl";
import ReactEcharts from "echarts-for-react";
import { covid_cases } from "../api";
const backend_ip = process.env.BACKEND_IP || 'http://172.26.134.60:80';
function Map(pro) {
  const [allData, setAllData] = useState(null);
  useEffect(() => {
    /* global fetch */
    fetch(backend_ip + "/covid_data")
      .then((resp) => resp.json())
      .then((json) => setAllData(json.data));
  }, []);

  //   console.log(allData);

  const layerStyle = {
    id: "data",
    type: "fill",
    paint: {
      "fill-color": {
        property: "score",
        stops: [
          [-0.01, "#c0392b"],
          [-0.005, "#e67e22"],
          [-0.001, "#f1c40f"],
          [0, "#2ecc71"],
        ],
      },
      "fill-opacity": 0.7,
    },
  };

  const [viewport, setViewport] = React.useState({
    longitude: 151.792493,
    latitude: -33.12181,
    zoom: 4,
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
      width="40vw"
      height="70vh"
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
          <div>City: {hoverInfo.feature.properties.city_name}</div>
          <div>
            Tweets Sentiment Average Score: {hoverInfo.feature.properties.score}
          </div>
          <div>Positive Tweets Count: {hoverInfo.feature.properties.pos}</div>
          <div>Negative Tweets Count: {hoverInfo.feature.properties.neg}</div>
          <div>Neutral Tweets Count: {hoverInfo.feature.properties.neu}</div>
        </div>
      )}
    </ReactMapGL>
  );
}

const MapHook = Map;

export default class Scenario3 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      case_data: [],
    };
  }

  componentDidMount() {
    covid_cases().then((res) => {
      this.setState({
        case_data: res.data.covid_cases,
      });
    });
  }

  casesOption = () => {
    return {
      xAxis: {
        type: "category",
        data: [
          "NSW\n(Sydney &\n Canberra)",
          "VIC\n(Melbourne)",
          "QLD\n(Brisbane)",
        ],
        axisLabel: {
          //坐标轴刻度标签的相关设置。
          interval: 0,
          rotate: "45",
        },
      },
      yAxis: {
        type: "value",
      },

      series: [
        {
          type: "bar",
          data: this.state.case_data,
          itemStyle: {
            normal: {
              label: {
                show: true, //开启显示
                position: "top", //在上方显示
                textStyle: {
                  //数值样式
                  color: "black",
                  fontSize: 16,
                },
              },
            },
          },
        },
      ],
    };
  };

  render() {
    return (
      <div>
        <Row gutter={[8, 8]}>
          <Col span={12}>
            <Card title="COVID-19 Tweets Sentiment Analysis">
              <MapHook />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="COVID-19 Cases （as of May 16, 2021）">
              <ReactEcharts option={this.casesOption()} />
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}
