import React, { Component } from "react";
import logo from '../assets/images/home.png'
import { basic_states } from "../api";
import './style.less'


const style = {
    bgd: {
        height: '100%',
        width: '100%',
        color: 'rgba(0,0,0,.25)',
        backgroundImage: `url(${logo})`,
        backgroundSize: '20%,20%',
    }
}

export default class Home extends Component{
    constructor(props) {
        super(props);
        this.state = {
            num: 0
        }
    }

    componentDidMount() {
        basic_states().then((res) => {
            // console.log(res.data.total_counts)
            this.setState({
                num:res.data.total_counts
            })
        })
    }


    render() {
        return (
            <div style={style.bgd}>
                <div className="title">
                    <h2>Now we have {this.state.num} tweets.</h2>
                </div>
            </div>
        )
    }
}

