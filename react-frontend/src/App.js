import React, { Component } from "react";
import {BrowserRouter, Route, Switch} from 'react-router-dom'
import './App.less';
import MainContainer from "./components/MainContainer";

export default class App extends Component{
    render() {
        return (
            <BrowserRouter>
            <Switch> {/*只匹配其中一个*/}
              <Route path='/' component={MainContainer}></Route>
            </Switch>
            </BrowserRouter>
        )
    }
}
