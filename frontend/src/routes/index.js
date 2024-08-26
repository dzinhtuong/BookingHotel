import config from '../config';
import HomePage from '../pages/HomePage';
import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
import NotFoundPage from '../pages/NotFoundPage';


const publicRoutes = [
    { path: config.routes.homePage, component: HomePage },
    { path: config.routes.loginPage, component: LoginPage },
    { path: config.routes.registerPage, component: RegisterPage },
    { path: config.routes.notFoundPage, component: NotFoundPage },
]

const privateRoutes = [

]

export { publicRoutes, privateRoutes }