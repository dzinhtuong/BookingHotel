import { useState } from 'react';
import { useForm } from 'react-hook-form';

import ForgotPassword from '../components/ForgotPassword';
import LoginForm from '../components/LoginForm';

const LoginPage = () => {
    const [show, setShow] = useState(true);
    const [email, setEmail] = useState('');

    const handleForgotPassword = () => {
        setShow(false);
    };
    const handleBackToLogin = () => {
        setShow(true);
    };
    //handle login
    const { control, handleSubmit } = useForm({
        defaultValues: {},
    });
    const onSubmitLogin = (data) => {
        console.log(data);
    };

    //handle forgot password
    const handleSubmitGetPassword = () => {
        console.log(email);
    };

    const handleChagneEmailInput = (e) => {
        setEmail(e.target.value)
    }
    return (
        <>
            {show ? (
                <LoginForm
                    handleForgotPassword={handleForgotPassword}
                    control={control}
                    handleSubmit={handleSubmit}
                    onSubmitLogin={onSubmitLogin}
                />
            ) : (
                <ForgotPassword
                    handleBackToLogin={handleBackToLogin}
                    handleChagneEmailInput={handleChagneEmailInput}
                    handleSubmitGetPassword={handleSubmitGetPassword}
                />
            )}
        </>
    );
};

export default LoginPage;
