import React from 'react'
import { Link } from 'react-router-dom'

export function Header() {
    return (
        <nav className='nav'>
            <Link className='site-title link' to={'/'}>Команда "Take_Profit" 📈</Link>
            <ul>
                <li>
                    <Link className='link' to={'/guide'}>Описание работы алгоритма</Link>
                </li>

                <li>
                    <Link className='link' to={'/bot'}>Бот</Link>
                </li>


                <li>
                    <Link className='link' to={'/statistics'}>Статистика</Link>
                </li>
            </ul>
        </nav>
    )
}

