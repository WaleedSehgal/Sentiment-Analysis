import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import TweetForm from './TweetForm';
//import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
//import 'dist/react-bootstrap-table-all.min.css'
//import './Table.js'


class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>Tweet Sentiment Analysis</h2>
        </div>
        <p className="App-intro">
          <br/>
        </p>
        <TweetForm />
      </div>
    );
  }


}

export default App;
