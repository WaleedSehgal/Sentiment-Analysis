import React, { Component } from 'react';
import ReactTable from './ReactTable';
import { Button, FormGroup, Form, ControlLabel, FormControl } from 'react-bootstrap';


var tweets = [{
      sentiment: "positive",
      tweet: "Item name 1 Item name 1 Item name 1 Item name 1 Item name 1 Item name 1 Item name 1 Item name 1",
      price: 100
  },{
      sentiment: "negative",
      tweet: "Item name 2",
      price: 100
  },{
        sentiment: "neutral",
        tweet: "Item name 5",
        price: 200
    }];

class TweetForm extends React.Component {
 render() { return (
   <div>
<div>
   <Form inline>
    <FormGroup controlId="formInlineName">
      <ControlLabel>Keyword</ControlLabel>
      {' '}
      <FormControl type="text" placeholder="Keyword" />
    </FormGroup>
    {' '}

    <Button type="submit">
      Search
    </Button>
    <div>
      <ReactTable value={tweets} />
    </div>
  </Form>
  </div>

  </div>);
  }
}

export default TweetForm;
