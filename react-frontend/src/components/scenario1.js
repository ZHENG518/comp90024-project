import React, { Component } from "react";
import { Card, Row, Col } from "antd";
import { basic_states } from "../api";
import ReactEcharts from "echarts-for-react";
import "echarts-wordcloud";

export default class Scenario1 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            langugae_data: [],
            hashtag_data: [],
            slang_data: [],
            emoji_data: []
        }
    }

    componentDidMount() {
        basic_states().then((res) => {
            // console.log(res.data.slang_count)
            this.setState({
                langugae_data: res.data.language_count,
                hashtag_data: res.data.hashtag_count,
                slang_data: res.data.slang_count,
                emoji_data: res.data.emoji_count,
            })
        })
    }

  languageOption = () => {
    return {
      tooltip: {
        trigger: "item",
        formatter: "{a} <br/>{b} : {c} ({d}%)",
      },
      legend: {
        type:'scroll',
        orient: "vertical",
        left: 0,
        data: this.state.langugae_data.map(x => x.name),
      },

      series: [
        {
          name: "Language Count",
          type: "pie",
          radius: "55%",
          center: ["50%", "60%"],
          data:this.state.langugae_data,
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },
          },
        },
      ],
    };
  };
  wordOption = (wordData) => {
    let maskImage = new Image();
    // 此为词云图呈现形状的图片base64码，可选，可以自定义图片
    maskImage.src =
      "data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTYuMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjI1NnB4IiBoZWlnaHQ9IjI1NnB4IiB2aWV3Qm94PSIwIDAgNTQ4LjE3NiA1NDguMTc2IiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCA1NDguMTc2IDU0OC4xNzY7IiB4bWw6c3BhY2U9InByZXNlcnZlIj4KPGc+Cgk8cGF0aCBkPSJNNTI0LjE4MywyOTcuMDY1Yy0xNS45ODUtMTkuODkzLTM2LjI2NS0zMi42OTEtNjAuODE1LTM4LjM5OWM3LjgxLTExLjk5MywxMS43MDQtMjUuMTI2LDExLjcwNC0zOS4zOTkgICBjMC0yMC4xNzctNy4xMzktMzcuNDAxLTIxLjQwOS01MS42NzhjLTE0LjI3My0xNC4yNzItMzEuNDk4LTIxLjQxMS01MS42NzUtMjEuNDExYy0xOC4yNzEsMC0zNC4wNzEsNS45MDEtNDcuMzksMTcuNzAzICAgYy0xMS4yMjUtMjcuMDI4LTI5LjA3NS00OC45MTctNTMuNTI5LTY1LjY2N2MtMjQuNDYtMTYuNzQ2LTUxLjcyOC0yNS4xMjUtODEuODAyLTI1LjEyNWMtNDAuMzQ5LDAtNzQuODAyLDE0LjI3OS0xMDMuMzUzLDQyLjgzICAgYy0yOC41NTMsMjguNTQ0LTQyLjgyNSw2Mi45OTktNDIuODI1LDEwMy4zNTFjMCwyLjg1NiwwLjE5MSw2Ljk0NSwwLjU3MSwxMi4yNzVjLTIyLjA3OCwxMC4yNzktMzkuODc2LDI1LjgzOC01My4zODksNDYuNjg2ICAgQzYuNzU5LDI5OS4wNjcsMCwzMjIuMDU1LDAsMzQ3LjE4YzAsMzUuMjExLDEyLjUxNyw2NS4zMzMsMzcuNTQ0LDkwLjM1OWMyNS4wMjgsMjUuMDMzLDU1LjE1LDM3LjU0OCw5MC4zNjIsMzcuNTQ4aDMxMC42MzYgICBjMzAuMjU5LDAsNTYuMDk2LTEwLjcxNSw3Ny41MTItMzIuMTIxYzIxLjQxMy0yMS40MTIsMzIuMTIxLTQ3LjI0OSwzMi4xMjEtNzcuNTE1ICAgQzU0OC4xNzIsMzM5Ljc1Nyw1NDAuMTc0LDMxNi45NTIsNTI0LjE4MywyOTcuMDY1eiIgZmlsbD0iI0ZGRkZGRiIvPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+Cjwvc3ZnPgo=";
    // let wordData = this.state.hashtag_data;

    let option = {
      backgroundColor: "#fff",
      tooltip: {
        pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
      },
      series: [
        {
          type: "wordCloud",
          gridSize: 1,
          // Text size range which the value in data will be mapped to.
          // Default to have minimum 12px and maximum 60px size.
          sizeRange: [12, 55],
          // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45

          rotationRange: [-45, 0, 45, 90],
          maskImage: maskImage, // 呈现形状图片， 可选
          textStyle: {
            normal: {
              color: function () {
                return (
                  "rgb(" +
                  Math.round(Math.random() * 255) +
                  ", " +
                  Math.round(Math.random() * 255) +
                  ", " +
                  Math.round(Math.random() * 255) +
                  ")"
                );
              },
            },
          },
          // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
          // Default to be put in the center and has 75% x 80% size.
          left: "center",
          top: "center",
          right: null,
          bottom: null,
          width: "90%",
          height: "110%",
          data: wordData,
        },
      ],
    };
    return option;
  };

    render() {
      console.log(this.state.slang_data)
    return (
      <div>
        <h1 style={{fontSize:'30px'} }>Australian Tweet Content Statistics</h1>
        <Row gutter={[8, 8]}>
          <Col span={12}>
            <Card title="Language">
              <ReactEcharts option={this.languageOption()} />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="Hashtag Top 50">
              <ReactEcharts option={this.wordOption(this.state.hashtag_data)} />
            </Card>
          </Col>
        </Row>
        <Row gutter={[8, 8]}>
          <Col span={12}>
            <Card title="Internet Slang Top 100">
              <ReactEcharts option={this.wordOption(this.state.slang_data)} />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="Emoji Top 100">
              <ReactEcharts option={this.wordOption(this.state.emoji_data)} />
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}
