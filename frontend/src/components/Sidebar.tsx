import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';

export default function Sidebar() {
    return (
        <Navbar bg="dark" expand="true" className="bg-body-tertiary">
            <Nav className="flex-column">
                <Nav.Link as={Link} to="/dashboard">
                    Dashboard
                </Nav.Link>
                <Nav.Link as={Link} to="/upload">
                    Upload
                </Nav.Link>
                <Nav.Link as={Link} to="/training">
                    Training
                </Nav.Link>
                <Nav.Link as={Link} to="/testing">
                    Testing
                </Nav.Link>
            </Nav>
        </Navbar>
    );
}
