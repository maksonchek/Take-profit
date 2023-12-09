import React from 'react'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react';

import { HiBan } from "react-icons/hi";
import { HiCheckCircle } from "react-icons/hi";
export function Bot() {

    const [companyShares, setCompanyShares] = useState([
        { name: 'sber' },
        { name: 'tinkoff' }
    ]);

    const [capital, setCapital] = useState(null);

    const [active, setActive] = useState(true);

    const [procentOfPossibleLoss, setProcentOfPossibleLoss] = useState(null);

    const [daysOfTrade, setDaysOfTrade] = useState(null);

    const validation = (min, max, value) => {
        if (value && value >= min && value <= max) {
            return true
        }
        else {
            return false
        }
    }

    return (
        <div className='botPage'>
            <div className='investMenu'>
                <ul className='companySharesList'>
                    {companyShares.map(share => <li>{share.name}</li>)}
                </ul>
            </div>
            <div className='botSettings'>
                <div className="settingsInputDiv">
                    <div className='settingsLabel'>
                        <p>Капитал</p>
                        <p>(Тыс. рублей)</p>
                    </div>
                    <div className='input'>
                        <input disabled={!active} onChange={(e) => { setCapital(e.target.value) }} type='number' min='1' max='1000' className='settingsInput'></input>
                        {validation(1, 1000, capital) ? <HiCheckCircle color='green' className='icon' /> : <HiBan color='red' className='icon' />}
                    </div>
                </div>
                <div className="settingsInputDiv">
                    <label className='settingsLabel'>Процент допустимых потерь</label>
                    <div className='input'>
                        <input disabled={!active} onChange={(e) => { setProcentOfPossibleLoss(e.target.value) }} min='0' max='100' type='number' className='settingsInput'></input>
                        {validation(0, 100, procentOfPossibleLoss) ? <HiCheckCircle color='green' className='icon' /> : <HiBan color='red' className='icon' />}
                    </div>
                </div>

                <div className="settingsInputDiv">
                    <label className='settingsLabel'>Срок торговли (Дней)</label>
                    <div className='input' >
                        <input disabled={!active} onChange={(e) => { setDaysOfTrade(e.target.value) }} type='number' min='1' max='365' className='settingsInput'></input>
                        {validation(0, 100, daysOfTrade) ? <HiCheckCircle color='green' className='icon' /> : <HiBan color='red' className='icon' />}
                    </div>
                </div>

                <button className='startButton'>Применить настройки</button>
            </div>
        </div >
    )
}

