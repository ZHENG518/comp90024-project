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
    // get_sum = () => {
    //     basic_states().then(response => {
    //         console.log('成功了', response.data.total_counts)
    //     }).catch(error => {
    //         console.log('失败了', error)
    //     })
    // }
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
            <div className="home" style={style.bgd}>
                <h2>Now we have {this.state.num} tweets.</h2>
            </div>
        )
    }
}

