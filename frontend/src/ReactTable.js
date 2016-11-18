import React, { Component } from 'react';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import 'react-bootstrap-table/dist/react-bootstrap-table-all.min.css'

var sentimentType = {
    positive: "positive",
    negative: "negative",
    neutral: "neutral"
};

function format(cell, row){
  return '<i class="glyphicon glyphicon-usd"></i> ' + cell;
}

class ReactTable extends Component {

   render() {
        return (
        <BootstrapTable
        	data={this.props.value}
        	striped={true}
        	hover={true}
        	condensed={false}
        	pagination={true}
        	search={false}>
          <TableHeaderColumn dataField="sentiment" width="180" filter={{type: "SelectFilter", options: sentimentType}}

           isKey={true} dataAlign="left" dataSort={true}>Sentiment

           </TableHeaderColumn>
          <TableHeaderColumn dataField="tweet" dataSort={true} dataAlign="center">Tweet</TableHeaderColumn>
          {/* <TableHeaderColumn dataField="price" dataAlign="center"
          dataFormat={format}>Product Price</TableHeaderColumn> -*/}
        </BootstrapTable>
      );
    }
}


export default ReactTable;
