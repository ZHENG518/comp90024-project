import ajax from './ajax'
import axios from 'axios'


const BASE = process.env.BACKEND_IP || 'http://localhost:5000';

export const basic_states = () => ajax(BASE + '/basic_stats')
export const covid_cases = () => ajax(BASE + '/covid_cases')