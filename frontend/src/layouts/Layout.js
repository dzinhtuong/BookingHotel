import Footer from '../layouts/Footer';
import Header from '../layouts/Header';

const Layout = ({children}) => {
    return <div>
        <Header />
        <div>{children}</div>
        <Footer />
    </div>;
};

export default Layout;
