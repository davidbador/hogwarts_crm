import React, { useState } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import MainPage from './components/MainPage';
import Register from '/components/Register';
import Login from './components/Login';
import './App.css';

function App() {
  return (
    <NavBar>
      <div className="App">
        <NavBar />
        <Route exact path="/">
          <MainPage />
        </Route>
        <div className="container">
          <Route exact path="/register">
            <Register />
          </Route>
          <Route exact path="/login">
            <Login />
          </Route>
        </div>
      </div>
    </NavBar>
  );
}

export default App;
