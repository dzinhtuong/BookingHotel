import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleDown, faMinus, faPlus, faUser } from '@fortawesome/free-solid-svg-icons';
import PropTypes from 'prop-types';
import { useTranslation } from 'react-i18next';

import OutsideClickHandler from '../OutsideClickHandler/OutsideClickHandler';

const SearchOptions = (props) => {
    const { t } = useTranslation();
    const [isOpen, setIsOpen] = useState(false);

    const handleOutsideClick = () => {
        setIsOpen(false);
    };

    return (
        <>
            <div
                className="h-full flex justify-between items-center bg-white rounded-lg border border-solid border-gray-300 cursor-pointer"
                onClick={() => setIsOpen(true)}
            >
                <FontAwesomeIcon icon={faUser} className="p-6" />
                <div className="flex justify-between items-center flex-grow">
                    <div>
                        <div>
                            {props.countAdult} {t('Người lớn')}
                            {props.countChild > 0 && `, ${props.countChild} ${t('Trẻ em')}`}
                        </div>
                        <div>
                            {props.countRoom} {t('Phòng')}
                        </div>
                    </div>
                    <FontAwesomeIcon icon={faAngleDown} className="p-6" />
                </div>
            </div>
            {isOpen && (
                <OutsideClickHandler onOutsideClick={handleOutsideClick}>
                    <div className="absolute top-[110%] left-0 right-0 px-6 py-3 rounded-lg shadow-custom-1 bg-white z-[999]">
                        <Options text={t('Phòng')} count={props.countRoom} setCount={props.setCountRoom} />
                        <Options
                            text={t('Người lớn')}
                            subText={t('18 tuổi trở lên')}
                            count={props.countAdult}
                            setCount={props.setCountAdult}
                        />
                        <Options
                            text={t('Trẻ em')}
                            subText={t('0-17 tuổi')}
                            count={props.countChild}
                            setCount={props.setCountChild}
                        />
                    </div>
                </OutsideClickHandler>
            )}
        </>
    );
};

const Options = ({ text, subText, count, setCount }) => {
    const handleIncreaseCount = () => {
        setCount((count) => count + 1);
    };

    const handleDecreaseCount = () => {
        setCount((count) => (count === 0 ? count : count - 1));
    };

    return (
        <div className="grid grid-cols-2 font-medium my-[8px] select-none">
            <div className="">
                <div>{text}</div>
                {subText && <div className="text-[12px] text-[#6b7388] font-normal leading-6">{subText}</div>}
            </div>
            <div className="flex justify-between items-center pl-[24px]">
                <FontAwesomeIcon
                    icon={faMinus}
                    className="w-[21px] h-[21px] rounded-full border border-solid border-primary text-primary cursor-pointer"
                    onClick={handleDecreaseCount}
                />
                <div className="text-[16px]">{count}</div>
                <FontAwesomeIcon
                    icon={faPlus}
                    className="w-[21px] h-[21px] rounded-full border border-solid border-primary text-primary cursor-pointer"
                    onClick={handleIncreaseCount}
                />
            </div>
        </div>
    );
};

SearchOptions.propTypes = {
    countRoom: PropTypes.any.isRequired,
    setCountRoom: PropTypes.func.isRequired,
    countAdult: PropTypes.any.isRequired,
    setCountAdult: PropTypes.func.isRequired,
    countChild: PropTypes.any.isRequired,
    setCountChild: PropTypes.func.isRequired,
};

Options.propTypes = {
    text: PropTypes.string.isRequired,
    subText: PropTypes.string,
    count: PropTypes.any.isRequired,
    setCount: PropTypes.func.isRequired,
};

export default SearchOptions;
