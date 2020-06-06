import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { studentsDateCount } from '../lib/UserFunctions';

const Date = () => {
    const [selectedDate, setSelectedDate] = useState(null)
    const [sendDate, setSendDate] = useState('Select a date')

    const send = async (event, selectedDate) => {
        event.preventDefault()
        selectedDate.setHours(selectedDate.getHours() + 3)
        let newDate = selectedDate.toISOString().substr(0, 10)
        console.log(newDate)
        let dateList = newDate.split('-')
        let year = dateList[0]
        let month = dateList[1]
        let day = dateList[2]
        const response = await studentsDateCount(year, month, day)
        setSendDate(response.data)
    }

    return (
        <div className="date">
            <form onSubmit={event => send(event, selectedDate)}>
                <DatePicker selected={selectedDate} onChange={date => setSelectedDate(date)}
                    dateFormat='yyyy/MM/dd' isClearable showYearDropdown scrollableMonthYearDropdown />
                <input type="submit" value="Submit" />
            </form>
            <div className="dateAmount">Number of students enrolled on this day: {sendDate}</div>
        </div>
    )
}

export default Date