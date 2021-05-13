import React, { Component } from "react"
import { Menu, Switch } from 'antd'
import {PieChartOutlined,CommentOutlined,BarChartOutlined, HomeOutlined} from '@ant-design/icons'
import { Link, withRouter } from 'react-router-dom'
import './style.less'
import logo from '../assets/images/twitter.png'

const SubMenu = Menu.SubMenu;


class LeftSider extends Component{
    render() {
        const path = this.props.location.pathname
        return (
        <div className="left-sider">
            <Link to='/' className='left-sider-header'>
                    <img src={logo} alt="" />
                    <h1> Tweet Analytics</h1>
                </Link>
        
        <Menu
            mode="inline"
            theme="dark"
            selectedKeys={[path]}
        >
        <Menu.Item key="/home" icon={<HomeOutlined />}>
            <Link to='/home'>
                <span>Home</span>
            </Link>
          </Menu.Item>
          <Menu.Item key="/scenario1" icon={<PieChartOutlined />}>
            <Link to='/scenario1'>
                <span>Scenario 1</span>
            </Link>
          </Menu.Item>
          <Menu.Item key="/scenario2" icon={<CommentOutlined />}>
            <Link to='/scenario2'>
                <span>Scenario 2</span>
            </Link>
          </Menu.Item>
          <Menu.Item key="/scenario3" icon={<BarChartOutlined />}>
            <Link to='/scenario3'>
                <span>Scenario 3</span>
            </Link>
          </Menu.Item>
        </Menu>
        </div>
        )
    }
}

export default withRouter(LeftSider)