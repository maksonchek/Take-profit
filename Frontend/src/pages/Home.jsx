import React, { useState } from 'react'
import { Link, resolvePath } from 'react-router-dom'
import axios from "axios";
import { useNavigate } from 'react-router-dom';

const hostUrl = 'http://192.168.246.21:8080/api'

export function Home({ setGlobalLogin }) {

    const [login, setLogin] = useState('');

    const [password, setPassword] = useState('');

    const navigate = useNavigate();


    const Click = async () => {
        if (password && login) {
            try {
                const response = await axios.post('http://192.168.0.107:8080/register_user',
                    {
                        login: login,
                        password: password
                    },
                    {
                        headers: {
                            'Accept': 'application/json'
                        }
                    });

                setGlobalLogin(login);
                navigate('/bot')
            }
            catch (err) {
                alert('Возникла ошибка попробуйте снова через некоторое время')
                console.log(err)
            }
        }
        else {
            alert('Введите пароль и логин')
        }
    }
    return (
        <div className='homePage'>
            <div className='slogan'>
                <h1 className='bigText'>Начни Трейдить Прямо Сейчас</h1>
                <p className='mediumText'>«Волк с Уолл-стрит» (англ. The Wolf of Wall Street) — американская эпическая биографическая криминальная чёрная комедия режиссёра Мартина Скорсезе, основанная на одноимённых мемуарах Джордана Белфорта и вышедшая в мировой прокат 25 декабря 2013 года. Автором сценария выступил Теренс Уинтер. Главную роль исполнил Леонардо Ди Каприо, который выступил и продюсером картины. Эта роль принесла актёру четвёртую номинацию на «Оскар», третью номинацию на BAFTA и вторую премию «Золотой глобус». Это пятый совместный проект актёра со Скорсезе[3].   </p>
            </div>
            <div className='authorizationBox'>
                <label>Логин</label>
                <input type='text' className='input' onChange={(e) => setLogin(e.target.value)}></input>
                <label>Пароль</label>
                <input type='password' className='input' onChange={(e) => setPassword(e.target.value)}></input>
                <button className='enterButton' onClick={Click}>Войти</button>
            </div>
        </div >
    )
}

