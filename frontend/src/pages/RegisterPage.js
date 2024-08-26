import { useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import PasswordInput from '../components/InputGroup/PasswordInput';
import TextInput from '../components/InputGroup/TextInput';
import Button from '../components/Button';
import ErrorInput from '../components/ErrorInput';
import Policy from '../components/Policy';

const RegisterPage = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const handleSwitchToLogin = () => {
        navigate('/login');
    };

    const {
        watch,
        control,
        handleSubmit,
        formState: { errors },
    } = useForm({
        defaultValues: {},
    });
    const onSubmitForm = (data) => {
        console.log(data);
    };
    return (
        <div className="bg-[#f9f9f9] pt-[48px] pb-[92px]">
            <div className="bg-white min-h-[610px] mx-[16px] shadow-lg  py-[16px] px-[24px] md:w-[500px] md:m-auto xl:w-[500px] xl:m-auto">
                <div className="text-black text-[24px] mb-[8px]">{t('Đăng ký')}</div>
                <form onSubmit={handleSubmit(onSubmitForm)}>
                    <div className="py-[12px]">
                        <Controller
                            name="username"
                            control={control}
                            rules={{
                                required: true,
                                pattern: {
                                    value: /^[\w.-]*$/,
                                },
                            }}
                            render={({ field: { onChange } }) => (
                                <TextInput label={t("Tên đăng nhập")} onChange={onChange} />
                            )}
                        />
                        {errors?.username && <ErrorInput message={t("Tên đăng nhập không hợp lệ")} />}
                    </div>
                    <div className="py-[12px]">
                        <Controller
                            name="email"
                            control={control}
                            rules={{
                                required: true,
                                pattern: {
                                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                                },
                            }}
                            render={({ field: { onChange } }) => <TextInput label="Email" onChange={onChange} />}
                        />
                        {errors?.email && <ErrorInput message={t("Email không hợp lệ")} />}
                    </div>
                    <div className="py-[12px]">
                        <Controller
                            name="password"
                            control={control}
                            rules={{ required: true, minLength: 6 }}
                            render={({ field: { onChange } }) => <PasswordInput label={t("Mật khẩu")} onChange={onChange} />}
                        />
                        {errors?.password && <ErrorInput message={t("Mật khẩu phải có ít nhất 6 ký tự")} />}
                    </div>
                    <div className="py-[12px]">
                        <Controller
                            name="confirmPassword"
                            control={control}
                            rules={{
                                required: true,
                                validate: (val) => {
                                    if (watch('password') !== val) {
                                        return 'Your passwords do no match';
                                    }
                                },
                            }}
                            render={({ field: { onChange } }) => (
                                <PasswordInput label={t("Xác nhận mật khẩu")} onChange={onChange} />
                            )}
                        />
                        {errors?.confirmPassword && <ErrorInput message={t("Mật khẩu không khớp")} />}
                    </div>
                    <input
                        type="submit"
                        value={t("Đăng ký")}
                        className="p-3 w-full my-[32px] text-white rounded cursor-pointer text-center border border-solid border-primary bg-primary hover:opacity-80 "
                    />
                </form>
                <div className="border-t border-solid border-gray-300">
                    <Button
                        text={t("Bạn đã có tài khoản? Đăng nhập")}
                        border
                        styles="my-[32px]"
                        onClick={handleSwitchToLogin}
                    />
                    <Policy />
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;
