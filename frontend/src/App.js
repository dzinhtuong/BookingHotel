import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { publicRoutes } from './routes';
import './App.css';
import Layout from './layouts/Layout';

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    {publicRoutes.map((route, index) => {
                        const Page = route.component;

                        return <Route key={index} path={route.path} element={<Layout><Page /></Layout>} />;
                    })}
                </Routes>
            </div>
        </Router>
    );
}

export default App;
