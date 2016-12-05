import React, { Component } from 'react';
import ReactTable from './ReactTable';
import { Button, FormGroup, Form, ControlLabel, FormControl } from 'react-bootstrap';

class TweetForm extends React.Component {
  constructor() {
    super();
    this.state = {
      tweets:[],
      keyword: ""
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.list();
  }

  handleChange(event) {
    this.setState({keyword: event.target.value});
  }

  handleSubmit(event) {
    this.search(this.state.keyword)
    event.preventDefault();
  }

  list(){
    var self = this;
    fetch(`api/tweets`, {
      accept: 'application/json',
      method: 'get'
    }).then(response => {
      var resp = response.json();
      console.log(resp);
      return resp;
    }).then(val => {self.setState({tweets : val});});
  }

  search(searchString){
    var self = this;
    fetch(`api/search/` + searchString, {
      accept: 'application/json',
      method: 'get'
    }).then(response => {
      var resp = response.json();
      console.log(resp);
      return resp;
    }).then(val => {self.setState({tweets : val});});
  }

 render() { return (
  <div>
    <div>
       <Form inline onSubmit={this.handleSubmit}>
        <FormGroup controlId="formInlineName">
          <ControlLabel>Keyword</ControlLabel>
          {' '}
          <FormControl type="text" placeholder="Keyword" value={this.state.keyword} onChange={this.handleChange}/>
        </FormGroup>
        {' '}

        <Button onClick = { () => this.search(this.state.keyword) }>
          Search
        </Button>
        <div>
          <ReactTable value={this.state.tweets} />
        </div>
      </Form>
   </div>
  </div>);
  }
}

export default TweetForm;
