// import { useState } from 'react'
import Header from "./components/Header.tsx"
import { Routes, Route } from 'react-router-dom';
import LandingPage from "./pages/LandingPage.tsx";
import DashboardPage from "./pages/Dashboard.tsx";
import UploadPage from "./pages/Upload.tsx";
import TrainingPage from "./pages/Training.tsx";
import TestingPage from "./pages/Testing.tsx";

import Container from "react-bootstrap/Container";
// import './App.css'

export default function App() {
    return (
        <>
            <Header />
            <Container fluid>
                <div className="content">
                    <Routes>
                        <Route path="/" element={<LandingPage />} />
                        <Route path="/dashboard" element={<DashboardPage />} />
                        <Route path="/upload" element={<UploadPage />} />
                        <Route path="/training" element={<TrainingPage />} />
                        <Route path="/testing" element={<TestingPage />} />
                    </Routes>
                </div>
            </Container>
        </>
    );
}
