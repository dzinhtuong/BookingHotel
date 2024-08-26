import { useEffect, useState } from 'react';
import { faGlobe } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useTranslation } from 'react-i18next';

import OutsideClickHandler from '../components/OutsideClickHandler/OutsideClickHandler';

const languageList = ['VN', 'EN', 'CN'];

const LanguageSwitch = () => {
    const { i18n } = useTranslation();
    const [isOpenLanguage, setIsOpenLanguage] = useState(false);
    const [currentLanguage, setCurrentLanguage] = useState('VN');
    const [remainingLanguges, setRemainingList] = useState(() => {
        return languageList.filter((lang) => lang !== currentLanguage);
    });

    useEffect(() => {
        setRemainingList(languageList.filter((lang) => lang !== currentLanguage));
    }, [currentLanguage]);

    const handleOutsideClickLanguage = () => {
        setIsOpenLanguage(false);
    };
    const handleChoseLanguage = (e) => {
        setCurrentLanguage(e.currentTarget.innerHTML);
        setIsOpenLanguage(false);
        i18n.changeLanguage(e.currentTarget.innerHTML.toLowerCase());
    };
    return (
        <div className="relative">
            <div
                className="flex justify-center items-center py-[8px] mx-[14px] cursor-pointer"
                onClick={() => setIsOpenLanguage(true)}
            >
                <div className="text-[16px] w-[25px] text-primary">{currentLanguage}</div>
                <FontAwesomeIcon icon={faGlobe} className="text-primary" />
            </div>
            {isOpenLanguage && (
                <OutsideClickHandler onOutsideClick={handleOutsideClickLanguage}>
                    <div className="absolute top-[110%] right-[14px] rounded-md shadow-custom-1 z-[999] bg-white px-[16px] py-[8px]">
                        {remainingLanguges &&
                            remainingLanguges.map((lang, index) => (
                                <div
                                    key={index}
                                    className="w-[50px] py-[4px] text-center text-[16px] cursor-pointer hover:bg-gray-300"
                                    onClick={handleChoseLanguage}
                                >
                                    {lang}
                                </div>
                            ))}
                    </div>
                </OutsideClickHandler>
            )}
        </div>
    );
};

export default LanguageSwitch;
