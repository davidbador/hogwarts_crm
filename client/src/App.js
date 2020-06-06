import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import MainPage from './components/MainPage';
import NavBar from './components/NavBar';
import Profile from './components/Profile';
import Register from './components/Register';
import Login from './components/Login';
import Students from './components/Students';
import AddNewStudent from './components/AddNewStudent';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  return (
    <Router>
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
          <Route exact path="/profile">
            <Profile />
          </Route>
          <Route exact path="/students">
            <Students />
          </Route>
          <Route exact path="/add_student">
            <AddNewStudent />
          </Route>
          <Route exact path="/dashboard">
            <Dashboard />
          </Route>
        </div>
      </div>
    </Router>
  );
}

export default App;
