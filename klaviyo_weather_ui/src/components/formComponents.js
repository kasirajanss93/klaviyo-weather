import React from 'react'
import { Col, FormGroup, Label, Input,Alert} from 'reactstrap';

export class TextComponent extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange=this.handleChange.bind(this);
  }
  handleChange(event) {
    this.props.onChange(event.target.id,event.target.value);
  }

  render () {

    if("undefined"  === typeof this.props.errors) {
      return(
        <FormGroup row>
          <Label for={this.props.id} sm={2}>{this.props.label}</Label>
          <Col sm={10}>
            <Input type="text" name={this.props.id} id={this.props.id} placeholder={this.props.holder} value={this.props.value} onChange={this.handleChange}/>
            </Col>
        </FormGroup>
      )
    }
    return(
      <FormGroup row>
        <Label for={this.props.id} sm={2}>{this.props.label}</Label>
        <Col sm={10}>
          <Input type="text" name={this.props.id} id={this.props.id} placeholder={this.props.holder} value={this.props.value} onChange={this.handleChange}/>
          <Alert color="danger">
            {this.props.errors}
          </Alert>
          </Col>
      </FormGroup>
    )

  }
}

export class SelectComponent extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange=this.handleChange.bind(this);
  }

  handleChange(event) {
    this.props.onChange(this.props.id,event.target.value)
  }
  render () {
    return(
      <FormGroup row>
        <Label for={this.props.id} sm={2}>{this.props.label}</Label>
         <Col sm={10}>
          <Input type="select" name={this.props.id} id={this.props.id} value={this.props.value} onChange={this.handleChange}>
            <option id="" value=""></option>
            {this.props.options.map(option =>
              <option key={option.id} id={option.id} value={option.id}>{option.name+", "+option.state}</option>)}
          </Input>
        </Col>
      </FormGroup>
    )

  }
}
