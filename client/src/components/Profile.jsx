import React from 'react';
import jwt_decode from 'jwt-decode';
import { skills, addUpdateExistingSkill, addUpdateDesiredSkill, singleStudentExisting, courses, addCourseToStudent, removeCourseFromStudent, singleStudentDesired, singleStudentCourses } from '../lib/UserFunctions'

class Profile extends React.Component {
    constructor() {
        super()
        this.state = {
            id: '',
            firstName: '',
            lastName: '',
            email: '',
            existingMagicSkills: {},
            desiredMagicSkills: {},
            interestedCourses: [],
            chooseExisting: [],
            chooseAddUpdateExistingValue: '',
            chooseAddUpdateExistingScore: '',
            chooseDesired: [],
            chooseAddUpdateDesiredValue: '',
            chooseAddUpdateDesiredScore: '',
            chooseAddCourse: [],
            chooseAddInterestedCourseValue: '',
            chooseDeleteCourse: [],
            chooseDeleteInterestedCourseValue: []
        }

        this.handleAddUpdateExistingSkillChange = this.handleAddUpdateExistingSkillChange.bind(this)
        this.handleAddUpdateExistingSkillChangeScore = this.handleAddUpdateExistingSkillChangeScore.bind(this)
        this.handleAddUpdateExistingSkillSubmit = this.handleAddUpdateExistingSkillSubmit.bind(this)
        this.handleAddUpdateDesiredSkillChange = this.handleAddUpdateDesiredSkillChange.bind(this)
        this.handleAddUpdateDesiredSkillChangeScore = this.handleAddUpdateDesiredSkillChangeScore.bind(this)
        this.handleAddUpdateDesiredSkillSubmit = this.handleAddUpdateDesiredSkillSubmit.bind(this)
        this.handleAddInterestedCourseChange = this.handleAddInterestedCourseChange.bind(this)
        this.handleAddInterestedCourseSubmit = this.handleAddInterestedCourseSubmit.bind(this)
        this.handleDeleteInterestedCourseChange = this.handleDeleteInterestedCourseChange.bind(this)
        this.handleDeleteInterestedCourseSubmit = this.handleDeleteInterestedCourseSubmit.bind(this)
    }

    componentDidMount() {
        const token = localStorage.usertoken
        const decoded = jwt_decode(token)
        this.setState({
            id: decoded.identity.id,
            firstName: decoded.identity.first_name,
            lastName: decoded.identity.last_name,
            email: decoded.identity.email,
            chooseAddUpdateExistingValue: 'riddikulus',
            chooseAddUpdateExistingScore: '1',
            chooseAddUpdateDesiredValue: 'riddikulus',
            chooseAddUpdateDesiredScore: '5',
            chooseAddInterestedCourseValue: 'advanced arithmancy studies',
            chooseDeleteInterestedCourseValue: 'advanced arithmancy studies'
        })
        this.getSkills()
        this.getCourses()
        this.getExisting(decoded.identity.id)
        this.getDesired(decoded.identity.id)
        this.getStudentCourses(decoded.identity.id)
    }

    handleAddUpdateExistingSkillChange(event) {
        this.setState({ chooseAddUpdateExistingValue: event.target.value })
    }

    handleAddUpdateExistingSkillChangeScore(event) {
        this.setState({ chooseAddUpdateExistingScore: event.target.value })
    }

    handleAddUpdateExistingSkillSubmit(event) {
        event.preventDefault()
        addUpdateExistingSkill(this.state.id, this.state.chooseAddUpdateExistingValue, this.state.chooseAddUpdateExistingScore)
        this.setState({
            existingMagicSkills: { ...this.state.existingMagicSkills, [this.state.chooseAddUpdateExistingValue]: this.state.chooseAddUpdateExistingScore }
        })
    }

    handleAddUpdateDesiredSkillChange(event) {
        this.setState({ chooseAddUpdateDesiredValue: event.target.value })
    }

    handleAddUpdateDesiredSkillChangeScore(event) {
        this.setState({ chooseAddUpdateDesiredScore: event.target.value })
    }

    handleAddUpdateDesiredSkillSubmit(event) {
        event.preventDefault()
        addUpdateDesiredSkill(this.state.id, this.state.chooseAddUpdateDesiredValue, this.state.chooseAddUpdateDesiredScore)
        this.setState({
            desiredMagicSkills: { ...this.state.desiredMagicSkills, [this.state.chooseAddUpdateDesiredValue]: this.state.chooseAddUpdateDesiredScore }
        })
    }

    handleAddInterestedCourseChange(event) {
        this.setState({ chooseAddInterestedCourseValue: event.target.value })
    }

    handleDeleteInterestedCourseChange(event) {
        this.setState({ chooseDeleteInterestedCourseValue: event.target.value })
    }

    handleAddInterestedCourseSubmit(event) {
        event.preventDefault()
        if (this.state.interestedCourses.includes(this.state.chooseAddInterestedCourseValue)) {
            return false
        } else {
            addCourseToStudent(this.state.id, this.state.chooseAddInterestedCourseValue)
            this.setState({
                interestedCourses: [...this.state.interestedCourses, this.state.chooseAddInterestedCourseValue]
            })
        }
    }

    handleDeleteInterestedCourseSubmit(event) {
        event.preventDefault()
        if (this.state.interestedCourses.includes(this.state.chooseDeleteInterestedCourseValue)) {
            removeCourseFromStudent(this.state.id, this.state.chooseDeleteInterestedCourseValue)
            let list = [...this.state.interestedCourses]
            let index = list.indexOf(this.state.chooseDeleteInterestedCourseValue)
            list.splice(index, 1)
            this.setState({
                interestedCourses: list
            })
        } else {
            return false
        }
    }

    getSkills = async () => {
        const response = await skills()
        this.setState({
            chooseExisting: [...response.data],
            chooseDesired: [...response.data]
        })
    }

    getExisting = async (id) => {
        const response = await singleStudentExisting(id)
        this.setState({
            existingMagicSkills: { ...response.data }
        })
    }

    getDesired = async (id) => {
        const response = await singleStudentDesired(id)
        this.setState({
            desiredMagicSkills: { ...response.data }
        })
    }

    getStudentCourses = async (id) => {
        const response = await singleStudentCourses(id)
        console.log(response.data)
        this.setState({
            interestedCourses: [...response.data]
        })
    }

    getCourses = async () => {
        const response = await courses()
        this.setState({
            chooseAddCourse: [...response.data],
            chooseDeleteCourse: [...response.data]
        })
    }

    render() {
        return (
            <div className="container">
                <h1 className="text-center">Profile</h1>
                <table className="table col-md-6 mx-auto">
                    <tbody>
                        <tr>
                            <td>First Name</td>
                            <td>{this.state.firstName}</td>
                        </tr>
                        <tr>
                            <td>Last Name</td>
                            <td>{this.state.lastName}</td>
                        </tr>
                        <tr>
                            <td>Email</td>
                            <td>{this.state.email}</td>
                        </tr>
                        <tr>
                            <td>Existing Magic Skills</td>
                            <td>{Object.entries(this.state.existingMagicSkills).map(([key, value]) => <div>{key}: {value}</div>)}</td>
                        </tr>
                        <tr>
                            <td>Desired Magic Skills</td>
                            <td>{Object.entries(this.state.desiredMagicSkills).map(([key, value]) => <div>{key}: {value}</div>)}</td>
                        </tr>
                        <tr>
                            <td>Interested Courses</td>
                            <td>{this.state.interestedCourses.map(course => <div>{course}</div>)}</td>
                        </tr>
                    </tbody>
                </table>
                <div>
                    <h1>Add or Update an Existing Skill</h1>
                    <form onSubmit={this.handleAddUpdateExistingSkillSubmit}>
                        <select value={this.state.chooseAddUpdateExistingValue} onChange={this.handleAddUpdateExistingSkillChange}>
                            {this.state.chooseExisting.map((el, index) => <option key={index} value={el}>{el}</option>)}
                        </select>
                        <select value={this.state.chooseAddUpdateExistingScore} onChange={this.handleAddUpdateExistingSkillChangeScore}>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                        <input type="submit" value="Submit" />
                    </form>
                </div>
                <div>
                    <h1>Add or Update a Desired Skill</h1>
                    <form onSubmit={this.handleAddUpdateDesiredSkillSubmit}>
                        <select value={this.state.chooseAddUpdateDesiredValue} onChange={this.handleAddUpdateDesiredSkillChange}>
                            {this.state.chooseDesired.map((el, index) => <option key={index} value={el}>{el}</option>)}
                        </select>
                        <select value={this.state.chooseAddExistingScore} onChange={this.handleAddExistingSkillChangeScore}>
                            <option value="5">5</option>
                        </select>
                        <input type="submit" value="Submit" />
                    </form>
                </div>
                <div>
                    <h1>Add a Course</h1>
                    <form onSubmit={this.handleAddInterestedCourseSubmit}>
                        <select value={this.state.chooseAddInterestedCourseValue} onChange={this.handleAddInterestedCourseChange}>
                            {this.state.chooseAddCourse.map((el) => <option key={el._id.$oid} value={el.course_name}>{el.course_name}</option>)}
                        </select>
                        <input type="submit" value="Submit" />
                    </form>
                </div>
                <div>
                    <h1>Delete a Course</h1>
                    <form onSubmit={this.handleDeleteInterestedCourseSubmit}>
                        <select value={this.state.chooseDeleteInterestedCourseValue} onChange={this.handleDeleteInterestedCourseChange}>
                            {this.state.chooseDeleteCourse.map((el) => <option key={el._id.$oid} value={el.course_name}>{el.course_name}</option>)}
                        </select>
                        <input type="submit" value="Submit" />
                    </form>
                </div>
            </div>
        )
    }
}

export default Profile