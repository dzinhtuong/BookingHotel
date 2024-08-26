import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import OutsideClickHandler from '../OutsideClickHandler/OutsideClickHandler';

const SearchInputText = ({ styles, destination, setDestination }) => {
    const { t } = useTranslation();
    const [isOpen, setIsOpen] = useState(false);

    const handleOutsideClick = () => {
        setIsOpen(false);
    };

    return (
        <div className="relative">
            <div className="relative w-full" onClick={() => setIsOpen(true)}>
                <input
                    type="text"
                    placeholder={t('Nhập điểm đến')}
                    className={`w-full bg-white rounded-lg border border-solid border-gray-300 cursor-pointer focus:outline-primary ${styles}`}
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                />
                <FontAwesomeIcon
                    icon={faSearch}
                    className="absolute top-0 left-[15px] bottom-0 my-auto text-gray-600 text-xl cursor-pointer"
                />
            </div>
            {isOpen && (
                <OutsideClickHandler onOutsideClick={handleOutsideClick}>
                    <div className="absolute top-[110%] left-0 right-0 bg-white rounded-lg px-6 py-3 shadow-custom-1 z-[999] ">
                        <div className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-3">
                            <div className="col-span-1 md:col-span-2 xl:col-span-2">
                                <div className="">{t('Các điểm đến ở Việt Nam')}</div>
                                <div className="grid grid-cols-1 md:grid-cols-2 md:gap-3 xl:grid-cols-2 xl:gap-3">
                                    <Destination
                                        text="Hồ Chí Minh"
                                        setDestination={setDestination}
                                        setIsOpen={setIsOpen}
                                    />
                                </div>
                            </div>
                            <div>
                                <div>{t('Các điểm đến quốc tế')}</div>
                                <div className="grid grid-cols-1 gap-3">
                                    <Destination
                                        text="Singapore"
                                        setDestination={setDestination}
                                        setIsOpen={setIsOpen}
                                    />
                                    <Destination text="Seoul" setDestination={setDestination} setIsOpen={setIsOpen} />
                                    <Destination
                                        text="Băng Cốc"
                                        setDestination={setDestination}
                                        setIsOpen={setIsOpen}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </OutsideClickHandler>
            )}
        </div>
    );
};

const Destination = ({ text, setDestination, setIsOpen }) => {
    const handleClick = () => {
        setDestination(text);
        setIsOpen(false);
    };
    return (
        <div
            className="font-semibold p-4 cursor-pointer hover:bg-[#eff4fe] hover:text-primary rounded-md"
            onClick={handleClick}
        >
            {text}
        </div>
    );
};

SearchInputText.propTypes = {
    styles: PropTypes.string,
    destination: PropTypes.string.isRequired,
    setDestination: PropTypes.func.isRequired,
};

export default SearchInputText;
