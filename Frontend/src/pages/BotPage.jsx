import React from 'react'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react';

export function Bot() {

    const [companyShares, setCompanyShares] = useState([
        { name: 'sber' },
        { name: 'tinkoff' }
    ]);

    return (
        <div className='botPage'>
            <div className='investMenu'>
                <ul className='companySharesList'>
                    {companyShares.map(share => <li>{share.name}</li>)}
                </ul>
            </div>
            <div className='botSettings'>
                <div className="settingsInputDiv">
                    <p>Капитал</p>
                    <input className='settingsInput'></input>
                </div>
                <div className="settingsInputDiv">
                    <p>Процент допустимых потерь</p>
                    <input className='settingsInput'></input>
                </div>

                <div className="settingsInputDiv">
                    <p>Срок торговли</p>
                    <input className='settingsInput'></input>
                </div>

                <button className='startButton'>Начать торги</button>
            </div>
        </div>
    )
}

