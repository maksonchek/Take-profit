import React from 'react'
import { Link, resolvePath } from 'react-router-dom'
import axios from "axios";


const hostUrl = 'http://192.168.246.21:8080/api'

export function Home() {

    const fetchData = async () => {
        const response = await axios.get('http://192.168.0.101:8080', {
            headers: {
                'Accept': 'application/json'
            },
        });

        const message = response.data.some

        console.log(message)
    }


    return (
        <div>
            <button onClick={fetchData}>POST запрос</button>
        </div>
    )
}

