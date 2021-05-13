import React, { Component } from "react";
import {Redirect, Route, Switch} from 'react-router-dom'
import {Layout } from 'antd';
import LeftSider from "./left-sider";
import Home from './home'
import Scenario1 from './scenario1';
import Scenario2 from './scenario2';
import Scenario3 from './scenario3';

// import '../App.less'

const {Sider, Content } = Layout;


export default class MainContainer extends Component{
    render() {
        return(
            <Layout style={{height: '100%'}}>
                <Sider>
                    <LeftSider />
                </Sider>
            <Layout>
                    <Content style={{ backgroundColor: '#fff' }}>
                     <Switch>
                            <Redirect from='/' exact to='/home' />
                            <Route path='/home' component={Home} />
                            <Route path='/scenario1' component={Scenario1}/>
                            <Route path='/scenario2' component={Scenario2}/>
                            <Route path='/scenario3' component={Scenario3}/>
                     </Switch>
                    </Content>
            </Layout>
            </Layout>
        )
    }
}