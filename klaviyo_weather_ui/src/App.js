import React, { Component } from 'react';

import './App.css';
import {SelectComponent,TextComponent} from './components/formComponents.js'
import Header from './components/header.js'
import { Container,Jumbotron,Col,Row, Button, Form,Alert} from 'reactstrap';
import {getCities,postUser} from './components/api.js'



class AlertComponent extends Component {
  render () {
    return(
      <div>
        <Alert color={this.props.color}>
        {this.props.value}
      </Alert>
      </div>
    )
  }
}


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email:"",
      errors: {},
      selectItems: [
      ],
      selectValue:"",
      alertText:"",
      alertColor:""
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.validateSubmit = this.validateSubmit.bind(this);
  }
  validateSubmit() {
    var errors = {}


    return errors;
  }

  handleSubmit(event) {
    event.preventDefault();
    var errors = this.validateSubmit();
    if(Object.keys(errors).length !== 0) {
      this.setState({
        errors: errors
      });
      return;
    }
    let email=this.state.email
    let selectValue=this.state.selectValue
    postUser(email,selectValue).then( (response) => {
      if(response.ok) {
        console.log(response.json())
          this.setState({alertColor:"success"})
          this.setState({alertText:"User has been Subscribed to Newsletter"})
      }
      else {
        this.setState({alertColor:"danger"})
        response.json().then(json=>{
          if("undefined"  !== typeof json['email']&&"undefined"  !== typeof json['cityId']) {

            this.setState({alertText:"Email: "+json['email'][0]+"\n Location: "+json['cityId'][0]})
          }
          else {
            if("undefined"  !== typeof json['email']) {

              this.setState({alertText:"Email: "+json['email'][0]})
            }
            else if("undefined"  !== typeof json['cityId']) {

              this.setState({alertText:"\n Location: "+json['cityId'][0]})
            }
            else {

              this.setState({alertText:"Server Error"})
            }
          }
        })
      }
    }).then((response) => {

        })
        .catch (function (error) {
            console.log('Request failed', error);
        });
  }
  handleChange(id,value) {
    let stateValue={};
    stateValue[id]=value;
    this.setState(stateValue);
  }

  componentWillMount() {
    getCities()
      .then( (response) => {
        console.log(response)
        this.setState({selectItems:response})
    }).catch(err => {
      console.log(err)})
  }

  render() {
    return (
      <div className="App">
        <Header/>
        <Container>
          <Jumbotron style={{backgroundColor: '#FFFFFF'}}>
            <AlertComponent value={this.state.alertText} color={this.state.alertColor}/>
            <Form onSubmit={this.handleSubmit}>
              <TextComponent holder="Enter email" value={this.state.email} id="email"
                label="Email" onChange={this.handleChange} errors={this.state.errors.email}/>
              <SelectComponent id="selectValue" value={this.state.selectValue} label="Location"
                  options={this.state.selectItems} onChange={this.handleChange}/>
              <Row>
                <Col/>
                <Col/>
                <Col/>
                <Col>
                  <p className="text-right"><Button color="primary" type="submit"
                    value="Subscribe">Subscribe</Button></p>
                </Col>
            </Row>
            </Form>
          </Jumbotron>
        </Container>
      </div>
    );
  }
}

export default App;
