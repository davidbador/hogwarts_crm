import React from 'react';
import { Pie } from 'react-chartjs-2';
import { studentsPieDesired } from '../lib/UserFunctions';
import { withRouter } from 'react-router-dom';

class PieExisting extends React.Component {
    constructor() {
        super();
        this.state = {
            labels: [],
            datasets: [
                {
                    label: "Rainfall",
                    backgroundColor: [
                        "red",
                        "blue",
                        "green",
                        "yellow",
                        "purple",
                        "orange",
                        "indigo",
                        "pink",
                        "grey",
                        "black"
                    ],
                    data: [],
                },
            ],
        };
    }

    componentDidMount() {
        this.getPieDesired()
    }

    getPieDesired = async () => {
        const response = await studentsPieDesired()
        let desiredData = this.state.datasets
        desiredData[0].data = Object.values(response.data)
        this.setState({
            labels: Object.keys(response.data),
            datasets: desiredData
        })
    }

    render() {
        return (
            <div className="container pie">
                <Pie
                    data={this.state}
                    options={{
                        title: {
                            display: true,
                            text: "Desired Magic Skills",
                            fontSize: 20,
                            fontColor: 'white',
                            fontFamily: 'Metal Mania'
                        },
                        legend: {
                            display: false,
                        },
                    }}
                />
            </div>
        );
    }
}

export default PieExisting