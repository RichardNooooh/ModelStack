// import { Navbar, NavbarBrand, Nav, NavItem, Button } from 'reactstrap';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';

export default function Header() {
    return (
        <Navbar expand="lg" className="bg-body-tertiary shadow flex-wrap d-flex justify-content-center mb-4 border-bottom">
            <Navbar.Brand href="/" className="d-flex align-items-center mb-3 mb-md-0 me-md-auto">
                ModelStack
            </Navbar.Brand>
            <Nav>
                <Nav.Item>
                    <Button color="outline-primary">Login</Button>
                    <Button color="primary">Register</Button>
                </Nav.Item>
            </Nav>
        </Navbar>
    );
};
