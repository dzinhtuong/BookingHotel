import { useState } from 'react';
import PropTypes from 'prop-types';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const PasswordInput = ({ label, onChange }) => {
    const [type, setType] = useState('password');
    const handleShowPassword = () => {
        setType('text');
    };
    const handleHidePassword = () => {
        setType('password');
    };
    return (
        <>
            <label className="block mb-2 font-medium text-gray-900">{label}</label>
            <div className="relative">
                <input
                    type={type}
                    className=" bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:outline-primary block w-full p-[12px]"
                    placeholder={label}
                    onChange={onChange}
                />
                {type === 'password' && (
                    <div className="w-[18px] h-[18px] absolute top-0 bottom-0 my-auto right-[10px] cursor-pointer flex justify-center items-center">
                        <FontAwesomeIcon
                            icon={faEyeSlash}
                            className="text-[10px] text-gray-500 "
                            onClick={handleShowPassword}
                        />
                    </div>
                )}
                {type === 'text' && (
                    <div className="w-[18px] h-[18px] absolute top-0 bottom-0 my-auto right-[10px] cursor-pointer flex justify-center items-center">
                        <FontAwesomeIcon
                            icon={faEye}
                            className="text-[10px] text-gray-500"
                            onClick={handleHidePassword}
                        />
                    </div>
                )}
            </div>
        </>
    );
};

PasswordInput.propTypes = {
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func,
};

export default PasswordInput;
