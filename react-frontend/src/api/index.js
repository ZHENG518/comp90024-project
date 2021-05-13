import ajax from './ajax'
import axios from 'axios'


const BASE='http://localhost:5000'

export const base_ip = () => BASE

export const basic_states = () => ajax(BASE + '/basic_stats')

export const language_data = () => ajax.get(BASE + '/language_data')