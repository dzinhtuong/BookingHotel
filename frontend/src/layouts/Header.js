import { useState } from 'react';
import { faBars, faHotel } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next'

import Button from '../components/Button';
import OutsideClickHandler from '../components/OutsideClickHandler/OutsideClickHandler';
import LanguageSwitch from '../components/LanguageSwitch';


const Header = () => {
    const navigate = useNavigate();
    const [isOpen, setIsOpen] = useState(false);

    const { t } = useTranslation();

    const handleLogin = () => {
        navigate('/login');
        setIsOpen(false);
    };
    const handleRegister = () => {
        navigate('/register');
        setIsOpen(false);
    };
    const handleRegisterToRent = () => {};

    const handleOutsideClick = () => {
        setIsOpen(false);
    };


    return (
        <div className="w-full">
            <div className="m-auto w-full h-header px-4 bg-white flex justify-between items-center">
                <Link to="/" className="h-full flex justify-center items-center md:px-4">
                    <FontAwesomeIcon icon={faHotel} className="text-primary mr-4 text-[32px]" />
                    <div className="text-3xl font-semibold text-primary tracking-widest">Booking.</div>
                </Link>
                <div className="flex items-center">
                    <div className="hidden md:flex md:px-4">
                        <Button
                            text={t('Đăng ký cho thuê nhà')}
                            styles="mr-12"
                            backgroundColor
                            onClick={handleRegisterToRent}
                        />
                        <Button text={t("Đăng nhập")} styles="mr-3" onClick={handleLogin} />
                        <Button text={t("Tạo tài khoản")} border onClick={handleRegister} />
                    </div>
                    <LanguageSwitch />
                </div>
                <div className="relative block md:hidden xl:hidden">
                    <div
                        className=" cursor-pointer px-2 rounded text-primary text-[22px] hover:text-white hover:bg-primary "
                        onClick={() => setIsOpen(true)}
                    >
                        <FontAwesomeIcon icon={faBars} className="" />
                    </div>
                    {isOpen && (
                        <OutsideClickHandler onOutsideClick={handleOutsideClick}>
                            <div className="absolute top-[110%] right-0 w-[200px] p-3 rounded shadow-custom-1 bg-white z-[999] ">
                                <Button
                                    text={t("Đăng ký cho thuê nhà")}
                                    styles="mb-3"
                                    border
                                    onClick={handleRegisterToRent}
                                />
                                <Button text={t("Đăng nhập")} styles="mb-3" border onClick={handleLogin} />
                                <Button text={t("Tạo tài khoản")} border backgroundColor onClick={handleRegister} />
                            </div>
                        </OutsideClickHandler>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Header;
