import React from 'react'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react';
import axios from "axios";
import { HiBan } from "react-icons/hi";
import { HiCheckCircle } from "react-icons/hi";
import { HiOutlineInformationCircle } from "react-icons/hi";


export function Bot({ login }) {

    useEffect(() => {
        console.log(login)
    }, [])
    const [companyShares, setCompanyShares] = useState([
        { name: 'sber' },
        { name: 'tinkoff' }
    ]);

    const [capital, setCapital] = useState(null);

    const [active, setActive] = useState(true);

    const [procentOfPossibleLoss, setProcentOfPossibleLoss] = useState(null);

    const [daysOfTrade, setDaysOfTrade] = useState(null);

    const [algorithm, setAlgorithm] = useState('');

    const [botIsRunning, setBotIsRunning] = useState(false);

    const validation = (min, max, value) => {
        if (value && value >= min && value <= max) {
            return true
        }
        else {
            return false
        }
    }

    const acceptSettings = async () => {
        if (active) {
            try {
                if (validation(1, 1000, capital)
                    &&
                    validation(0, 100, procentOfPossibleLoss)
                    &&
                    (validation(0, 1000, daysOfTrade) || daysOfTrade === null)
                    &&
                    algorithm) {
                    const response = await axios.post('http://192.168.0.107:8080/' + login + '/trading', {
                        fond: capital,
                        percentOfPossibleLoss: procentOfPossibleLoss,
                        daysOfTrade: daysOfTrade || 0,
                        algorithmNum: algorithm
                    }, {
                        headers: {
                            'Accept': 'application/json'
                        }
                    });
                    setActive(false);
                }
                else if (!validation(1, 1000, capital)) {
                    alert('Укажите стартовый капитал')
                }
                else if (!validation(0, 100, procentOfPossibleLoss)) {
                    alert('Укажите процент допустимых потерь')
                }
                else if (!(validation(0, 1000, daysOfTrade)) && !(daysOfTrade === null)) {
                    alert('Укажите количество дней торговли')
                }
                else if (!algorithm) {
                    alert('Выберите алгортим для торговли')
                }
            }
            catch (err) {
                alert('Возникла ошибка попробуйте снова через некоторое время')
                console.log(err)
            }
        }
        else {
            setActive(true)
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

                    <label className='settingsLabel'> Капитал (Тыс. рублей)<HiOutlineInformationCircle className='icon' /></label>
                    <div className='input'>
                        <input disabled={!active} onChange={(e) => { setCapital(e.target.value) }} type='number' min='1' max='1000' className='settingsInput'></input>
                        {validation(1, 1000, capital) ? <HiCheckCircle color='green' className='icon' /> : <HiBan color='red' className='icon' />}
                    </div>
                </div>
                <div className="settingsInputDiv">
                    <label className='settingsLabel'>Процент допустимых потерь <HiOutlineInformationCircle className='icon' /></label>
                    <div className='input'>
                        <input disabled={!active} onChange={(e) => { setProcentOfPossibleLoss(e.target.value) }} min='0' max='100' type='number' className='settingsInput'></input>
                        {validation(0, 100, procentOfPossibleLoss) ? <HiCheckCircle color='green' className='icon' /> : <HiBan color='red' className='icon' />}
                    </div>
                </div>

                <div className="settingsInputDiv">
                    <label className='settingsLabel'>Срок торговли (Дней) <HiOutlineInformationCircle className='icon' /></label>
                    <div className='input' >
                        <input disabled={!active} onChange={(e) => { setDaysOfTrade(e.target.value) }} type='number' min='1' max='365' className='settingsInput'></input>
                        {(daysOfTrade === null || validation(0, 1000, daysOfTrade)) ? <HiCheckCircle color='green' className='icon' /> : <HiBan color='red' className='icon' />}
                    </div>
                </div>
                <div className='selectDiv'>
                    <select disabled={!active} className='select' onChange={(e) => setAlgorithm(e.target.value)}>
                        <option value={''}>--Выберите алгоритм для трейда--</option>
                        <option value={'ML'}>Machine Learning алгоритм</option>
                        <option value={'Math'}>Математический алгоритм</option>
                    </select>
                    <HiOutlineInformationCircle className='icon' />
                </div>

                <button className='startButton' onClick={acceptSettings}>
                    {active ? 'Применить настройки' : 'Изменить настройки'}
                </button>
                <button className='startButton'>{active ? 'Запустить бота' : 'Остановить бота'}</button>
            </div>
        </div >
    )
}

