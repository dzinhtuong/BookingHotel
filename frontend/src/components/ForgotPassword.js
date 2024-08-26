import PropTypes from 'prop-types';
import { useTranslation } from 'react-i18next';

import TextInput from '../components/InputGroup/TextInput';
import Button from './Button';

const ForgotPassword = ({ handleBackToLogin, handleChagneEmailInput, handleSubmitGetPassword }) => {
    const { t } = useTranslation();
    return (
        <div className="bg-[#f9f9f9] pt-[48px] pb-[92px]">
            <div className="bg-white mx-[16px] shadow-lg  py-[16px] px-[24px] md:w-[500px] md:m-auto xl:w-[500px] xl:m-auto">
                <div className="text-black text-[24px] mb-[4px]">{t('Quên mật khẩu')}</div>

                <div className="py-[12px]">
                    <TextInput label="Email" onChange={handleChagneEmailInput} />
                </div>
                <div className="py-[12px]">
                    {t(
                        'Xin vui lòng nhập email của bạn vào ô bên trên. Chúng tôi sẽ gởi cho bạn đường dẫn để xem hướng dẫn cụ thể.',
                    )}
                </div>
                <Button text={t('Lấy lại mật khẩu')} backgroundColor onClick={handleSubmitGetPassword} />

                <div
                    className="my-[32px] flex justify-center items-center text-primary cursor-pointer hover:opacity-80 hover:underline"
                    onClick={handleBackToLogin}
                >
                    {t('Quay lại đăng nhập')}
                </div>
            </div>
        </div>
    );
};

ForgotPassword.propTypes = {
    handleBackToLogin: PropTypes.func.isRequired,
    handleChagneEmailInput: PropTypes.func,
    handleSubmitGetPassword: PropTypes.func,
};

export default ForgotPassword;
