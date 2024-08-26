import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLock } from '@fortawesome/free-solid-svg-icons';
import { Controller } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import PasswordInput from '../components/InputGroup/PasswordInput';
import TextInput from '../components/InputGroup/TextInput';
import Policy from './Policy';

const LoginForm = ({ handleForgotPassword, control, handleSubmit, onSubmitLogin }) => {
    const { t } = useTranslation();
    return (
        <div className="bg-[#f9f9f9] pt-[48px] pb-[92px]">
            <div className="bg-white min-h-[610px] mx-[16px] shadow-lg  py-[16px] px-[24px] md:w-[500px] md:m-auto xl:w-[500px] xl:m-auto">
                <div className="text-black text-[24px] mb-[4px]">{t('Đăng nhập')}</div>
                <div className="text-[14px] text-black mb-[8px]">
                    {t('Để đảm bảo an toàn, xin vui lòng đăng nhập để truy cập vào thông tin')}
                </div>
                <form onSubmit={handleSubmit(onSubmitLogin)}>
                    <div className="py-[12px]">
                        <Controller
                            name="username"
                            control={control}
                            render={({ field: { onChange } }) => (
                                <TextInput label={t('Tên đăng nhập')} onChange={onChange} />
                            )}
                        />
                    </div>
                    <div className="py-[12px]">
                        <Controller
                            name="password"
                            control={control}
                            render={({ field: { onChange } }) => (
                                <PasswordInput label={t('Mật khẩu')} onChange={onChange} />
                            )}
                        />
                    </div>

                    <input
                        type="submit"
                        value={t('Đăng nhập')}
                        className="p-3 w-full my-[32px] text-white rounded cursor-pointer text-center border border-solid border-primary bg-primary hover:opacity-80 "
                    />
                </form>

                <div className="flex justify-between items-center text-primary mb-[32px]">
                    <Link to="/register" className="hover:opacity-80 hover:underline">
                        {t('Tạo tài khoản')}
                    </Link>
                    <div
                        className="flex justify-start items-center cursor-pointer hover:opacity-80 hover:underline"
                        onClick={handleForgotPassword}
                    >
                        <FontAwesomeIcon icon={faLock} className="mr-[6px] text-sm" />
                        <p>{t('Quên mật khẩu')}?</p>
                    </div>
                </div>
                <div className="border-t border-solid border-gray-300">
                    <Policy />
                </div>
            </div>
        </div>
    );
};

LoginForm.propTypes = {
    handleForgotPassword: PropTypes.func.isRequired,
    control: PropTypes.any,
    handleSubmit: PropTypes.func,
    onSubmitLogin: PropTypes.func,
};

export default LoginForm;
