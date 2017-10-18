import React from 'react'
import { Collapse, Navbar, NavbarToggler, NavbarBrand, Nav, NavItem, NavLink} from 'reactstrap'

class Header extends React.Component {
  constructor(props) {
    super(props);
    this.toggle = this.toggle.bind(this);

    this.state = {
      isOpen: false,
    };
  }
  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
  render () {
    return (
        <div>
          <Navbar color="dark" dark expand>
              <NavbarToggler onClick={this.toggle} />
              <NavbarBrand href="https://www.klaviyo.com/" target="_blank">Klaviyo</NavbarBrand>
              <Collapse className="navbar-toggleable-md" isOpen={this.state.isOpen} navbar>
                <Nav className="mr-auto" navbar>
                  <NavItem>
                    <NavLink href="/">Home</NavLink>
                  </NavItem>
                </Nav>
              </Collapse>
          </Navbar>
      </div>


    );
  }
}

export default Header;
