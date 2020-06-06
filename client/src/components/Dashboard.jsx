import React from 'react';
import Date from './Date';
import PieExisting from './PieExisting';
import PieDesired from './PieDesired';
import DeleteStudent from './DeleteStudent';
import '../App.css';

const Dashboard = () => {
    return (
        <div>
            <Date />
            <PieExisting />
            <PieDesired />
            <DeleteStudent />
        </div>
    )
}

export default Dashboard