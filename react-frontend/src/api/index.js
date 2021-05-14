import ajax from './ajax'
import axios from 'axios'


const BASE = process.env.BACKEND_IP || 'http://localhost';

export const base_ip = () => BASE

export const basic_states = () => ajax(BASE + ':5000/basic_stats')

export const language_data = () => ajax.get(BASE + ':5000/language_data')