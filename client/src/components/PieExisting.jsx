import React from 'react';
import { Pie } from 'react-chartjs-2';
import { studentsPieExisting } from '../lib/UserFunctions';

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
        this.getPieExisting()
    }

    getPieExisting = async () => {
        const response = await studentsPieExisting()
        let existingData = this.state.datasets
        existingData[0].data = Object.values(response.data)
        this.setState({
            labels: Object.keys(response.data),
            datasets: existingData
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
                            text: "Existing Magic Skills",
                            fontSize: 20,
                            fontColor: 'white',
                            fontFamily: 'Metal Mania',
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